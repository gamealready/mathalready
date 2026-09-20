<?php
/**
 * MathAlready Daily Question Mailer
 * Upload to: /send_daily_question.php (web root)
 * Run via hPanel cron: php /home/u788309981/public_html/send_daily_question.php
 * Schedule: 0 13 * * *  (9 AM ET = 1 PM UTC)
 *
 * Block direct web access — CLI only.
 */
if (php_sapi_name() !== 'cli') {
    http_response_code(403);
    exit('Forbidden');
}

// ---------- CONFIG ----------
define('SUBSCRIBERS_FILE', __DIR__ . '/subscribers.txt');
define('LOG_FILE',         __DIR__ . '/mailer.log');
define('FROM_NAME', 'MathAlready Daily');
define('FROM_ADDR', 'emmapaige314@gmail.com');
define('REPLY_TO',  'ma@mathalready.com');
define('SITE_BASE', 'https://www.mathalready.com');

// Only questions with parseable text + answer choices (not image-only pages)
$QUESTION_LIST = array_merge(
    // 2016: all 25
    array_map(fn($q) => [2016, $q], range(1, 25)),
    // 2017: all 25
    array_map(fn($q) => [2017, $q], range(1, 25)),
    // 2018: Q1-11 and Q25 only (Q12-24 are image-only)
    array_map(fn($q) => [2018, $q], array_merge(range(1, 11), [25])),
    // 2024: only questions with text
    array_map(fn($q) => [2024, $q], [2,3,5,6,7,11,13,14,15,16,17,18,19,20,22,23,24,25]),
    // 2025: all 25
    array_map(fn($q) => [2025, $q], range(1, 25)),
    // 2026: all 25
    array_map(fn($q) => [2026, $q], range(1, 25))
); // 130 total // 130 total
// Total: 25 + 25 + 12 + 18 + 25 = 105 questions

// ---------- HELPERS ----------

function logMsg($msg) {
    $ts   = gmdate('Y-m-d H:i:s') . ' UTC';
    $line = "[$ts] $msg\n";
    echo $line;
    file_put_contents(LOG_FILE, $line, FILE_APPEND);
}

function pickTodaysQuestion($list) {
    $epoch = new DateTime('2026-05-10', new DateTimeZone('America/New_York'));
    $today = new DateTime('today',      new DateTimeZone('America/New_York'));
    $days  = (int)$epoch->diff($today)->days;
    return $list[$days % count($list)];
}

/**
 * Convert math shorthand in answer strings to readable text.
 * e.g. frac{3}{7} -> 3/7, sqrt(2) -> √2, pi -> π, cdot -> ·
 */
function formatAnswer($raw) {
    $s = trim($raw, " \t\n\r\0\x0B'\"");

    // frac{a}{b} -> a/b
    $s = preg_replace_callback(
        '/frac\{([^}]+)\}\{([^}]+)\}/',
        fn($m) => $m[1] . '/' . $m[2],
        $s
    );

    // sqrt(x) or sqrt{x} -> √x
    $s = preg_replace('/sqrt\(([^)]+)\)/', '√($1)', $s);
    $s = preg_replace('/sqrt\{([^}]+)\}/', '√($1)', $s);

    // Symbols
    $s = str_replace(['\\pi', 'pi'], 'π', $s);
    $s = str_replace(['\\cdot', 'cdot', '*'], '×', $s);
    $s = str_replace(['\\times', 'times'], '×', $s);
    $s = str_replace(['\\%'], '%', $s);

    // Remove remaining backslashes
    $s = str_replace('\\', '', $s);

    return $s;
}

function fetchPage($url) {
    $ctx = stream_context_create(['http' => [
        'timeout'         => 15,
        'follow_location' => 1,
        'user_agent'      => 'Mozilla/5.0',
    ]]);
    return @file_get_contents($url, false, $ctx);
}

function parseQuestion($html) {
    // 1. Answer values from JS array
    preg_match('/var allAnswers=\[([^\]]+)\]/', $html, $am);
    $rawAnswers = [];
    if ($am) {
        // Split on comma not inside braces/parens
        preg_match_all('/"([^"]*)"/', $am[1], $vals);
        $rawAnswers = $vals[1];
    }
    $answers = array_map('formatAnswer', $rawAnswers);

    // 2. Correct index
    preg_match('/var correctIdx=(\d+)/', $html, $cm);
    $correctIdx = isset($cm[1]) ? (int)$cm[1] : 0;

    // 3. Question text: extract from <p><b>...</b></p> after setUpAnswers()
    //    Use the first <p><b>...</b></p> inside the article form area
    preg_match('/setUpAnswers\(\).*?<p><b>(.*?)<\/b><\/p>/s', $html, $qm);
    $questionText = '';
    if ($qm) {
        // Strip any remaining HTML tags (e.g. <br>, <i>) but preserve text
        $questionText = strip_tags($qm[1]);
        $questionText = html_entity_decode($questionText, ENT_QUOTES | ENT_HTML5, 'UTF-8');
        $questionText = preg_replace('/\s+/', ' ', trim($questionText));
    }

    // 4. Check if there's a diagram image
    // Extract diagram URL if present
    $diagramUrl = '';
    if (preg_match('/<img src="(images\/AMC8_[^"]+_diagram\.png)"/', $html, $dm)) {
        $diagramUrl = 'https://www.mathalready.com/' . $dm[1];
    }
    $hasDiagram = $diagramUrl !== '';

    $labels  = ['A','B','C','D','E'];
    $choices = [];
    foreach ($answers as $i => $val) {
        if (isset($labels[$i])) {
            $choices[] = [$labels[$i], $val];
        }
    }
    $correctLabel = $labels[$correctIdx] ?? '?';

    return [$questionText, $choices, $correctLabel, $diagramUrl];
}

function buildEmail($year, $num, $questionText, $choices, $correctLabel, $diagramUrl, $pageUrl) {
    $today = date('F j, Y');

    $choicesHtml = '';
    $choicesText = '';
    foreach ($choices as [$label, $val]) {
        $choicesHtml .= "      <p style='margin:6px 0'>($label)&nbsp; " . htmlspecialchars($val) . "</p>\n";
        $choicesText .= "  ($label) $val\n";
    }

    $diagramNote = $diagramUrl
        ? "<div style='text-align:center;margin:16px 0'><img src='$diagramUrl' alt='Problem diagram' style='max-width:100%;height:auto;border:1px solid #eee;border-radius:4px'></div>"
        : '';
    $diagramNoteText = $diagramUrl
        ? "[See diagram at: $pageUrl]\n\n"
        : '';

    $html = <<<HTML
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;padding:20px;color:#222">
  <div style="background:#003366;padding:16px 20px;border-radius:6px 6px 0 0">
    <h1 style="color:#fff;margin:0;font-size:22px">MathAlready Daily Question</h1>
    <p style="color:#aac8ff;margin:4px 0 0">$today</p>
  </div>
  <div style="border:1px solid #ccc;border-top:none;padding:20px;border-radius:0 0 6px 6px">
    <p style="font-size:13px;color:#666;margin-top:0">AMC 8 $year &mdash; Problem $num</p>
    <p style="font-size:17px;line-height:1.6"><strong>$questionText</strong></p>
    $diagramNote
    <div style="margin:16px 0;padding:12px;background:#f9f9f9;border-radius:4px">
$choicesHtml
    </div>
    <p style="margin-top:24px">
      <a href="$pageUrl" style="background:#003366;color:#fff;padding:10px 18px;border-radius:4px;text-decoration:none;font-size:14px">
        Solve &amp; See Answer on MathAlready &rarr;
      </a>
    </p>
    <hr style="margin-top:30px;border:none;border-top:1px solid #eee">
    <p style="font-size:11px;color:#999">
      You are receiving this because you subscribed at mathalready.com.<br>
      To unsubscribe, reply with "unsubscribe" in the subject.
    </p>
  </div>
</body>
</html>
HTML;

    $text = "MathAlready Daily Question — $today\n\n"
          . "AMC 8 $year - Problem $num\n\n"
          . "$questionText\n\n"
          . $diagramNoteText
          . $choicesText
          . "\nAnswer: ($correctLabel)\n\n"
          . "Solve online: $pageUrl\n\n"
          . "---\nTo unsubscribe, reply with \"unsubscribe\" in the subject.\n";

    return [$html, $text];
}

function sendEmail($to, $subject, $htmlBody, $textBody) {
    $boundary = md5(uniqid());
    $headers  = implode("\r\n", [
        'From: ' . FROM_NAME . ' <' . FROM_ADDR . '>',
        'Reply-To: ' . REPLY_TO,
        'MIME-Version: 1.0',
        "Content-Type: multipart/alternative; boundary=\"$boundary\"",
    ]);

    $body  = "--$boundary\r\n";
    $body .= "Content-Type: text/plain; charset=UTF-8\r\n\r\n";
    $body .= $textBody . "\r\n";
    $body .= "--$boundary\r\n";
    $body .= "Content-Type: text/html; charset=UTF-8\r\n\r\n";
    $body .= $htmlBody . "\r\n";
    $body .= "--$boundary--\r\n";

    $ok = mail($to, $subject, $body, $headers, '-f' . FROM_ADDR);
    if (!$ok) {
        throw new Exception("mail() returned false for $to");
    }
}

// ---------- MAIN ----------

logMsg("=== Daily Question Mailer starting ===");
logMsg("Question pool: " . count($QUESTION_LIST) . " questions");

[$year, $num] = pickTodaysQuestion($QUESTION_LIST);
logMsg("Today's question: AMC 8 $year Problem $num");

$pageUrl   = SITE_BASE . "/AMC8_{$year}_{$num}.html";
$html_page = fetchPage($pageUrl);
if (!$html_page) {
    logMsg("ERROR: Could not fetch question page: $pageUrl");
    exit(1);
}

[$questionText, $choices, $correctLabel, $diagramUrl] = parseQuestion($html_page);

if (!$questionText) {
    logMsg("ERROR: Could not parse question text from $pageUrl");
    exit(1);
}
if (count($choices) !== 5) {
    logMsg("ERROR: Expected 5 answer choices, got " . count($choices) . " for $pageUrl");
    exit(1);
}

logMsg("Question: " . substr($questionText, 0, 100) . "...");
logMsg("Choices: " . implode(', ', array_map(fn($c) => "({$c[0]}) {$c[1]}", $choices)));
logMsg("Answer: ($correctLabel)" . ($diagramUrl ? " [diagram: $diagramUrl]" : ""));

// Load subscribers
$subscribers = [];
if (file_exists(SUBSCRIBERS_FILE)) {
    foreach (file(SUBSCRIBERS_FILE, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) as $line) {
        $email = trim($line);
        if ($email && strpos($email, '@') !== false) {
            $subscribers[] = $email;
        }
    }
}
logMsg("Subscribers: " . count($subscribers));

if (empty($subscribers)) {
    logMsg("No subscribers. Exiting.");
    exit(0);
}

$today   = date('F j, Y');
$subject = "AMC 8 Daily Question — $today";
[$htmlBody, $textBody] = buildEmail($year, $num, $questionText, $choices, $correctLabel, $diagramUrl, $pageUrl);

$sent = 0; $failed = 0;
foreach ($subscribers as $email) {
    try {
        sendEmail($email, $subject, $htmlBody, $textBody);
        logMsg("Sent to $email");
        $sent++;
    } catch (Exception $e) {
        logMsg("Failed $email: " . $e->getMessage());
        $failed++;
    }
}

logMsg("Done. Sent: $sent, Failed: $failed");
