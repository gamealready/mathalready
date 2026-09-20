<?php
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $email = filter_var(trim($_POST["email"]), FILTER_SANITIZE_EMAIL);
    
    if (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        echo "Invalid email.";
        exit;
    }

    // Save email to subscribers list
    $file = __DIR__ . "/subscribers.txt";
    $emails = file_exists($file) ? file($file, FILE_IGNORE_NEW_LINES | FILE_SKIP_EMPTY_LINES) : [];
    if (!in_array($email, $emails)) {
        file_put_contents($file, $email . "\n", FILE_APPEND | LOCK_EX);
    }

    // Notify Bob and Gary
    $to = "emmapaige314@gmail.com";
    $cc = "garypai314@gmail.com";
    $subject = "New MathAlready Signup: " . $email;
    $message = "New email signup on MathAlready.com\n\nEmail: " . $email . "\nTime: " . date("Y-m-d H:i:s") . " UTC";
    $headers = "From: ma@mathalready.com\r\n";
    $headers .= "Cc: " . $cc . "\r\n";
    $headers .= "Reply-To: " . $email . "\r\n";

    mail($to, $subject, $message, $headers);
    header("Location: thankyou.html");
}
?>
