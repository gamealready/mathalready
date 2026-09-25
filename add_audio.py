#!/usr/bin/env python3
"""Add Read Aloud button to AMC8_2018 HTML files using Web Speech API."""

import re, os

# Full readable question texts for all 25 AMC 8 2018 problems
AUDIO_TEXTS = {
    1: ("An amusement park has a collection of scale models, with a ratio of 1 to 20, "
        "of buildings and other sights from around the country. "
        "The height of the United States Capitol is 289 feet. "
        "What is the height in feet of its replica to the nearest whole number? "
        "The answer choices are: A, 14. B, 15. C, 16. D, 18. E, 20."),

    2: ("What is the value of the product: "
        "1 plus 1 over 1, times 1 plus 1 over 2, times 1 plus 1 over 3, "
        "times 1 plus 1 over 4, times 1 plus 1 over 5, times 1 plus 1 over 6? "
        "The answer choices are: A, 7 over 6. B, 4 over 3. C, 7 over 2. D, 7. E, 8."),

    3: ("Students Arn, Bob, Cyd, Dan, Eve, and Fon are arranged in that order in a circle. "
        "They start counting: Arn first, then Bob, and so forth. "
        "When the number contains a 7 as a digit, such as 47, or is a multiple of 7, "
        "that person leaves the circle and the counting continues. "
        "Who is the last one present in the circle? "
        "The answer choices are: A, Arn. B, Bob. C, Cyd. D, Dan. E, Eve."),

    4: ("The twelve-sided figure shown has been drawn on 1 centimeter by 1 centimeter graph paper. "
        "What is the area of the figure in square centimeters? "
        "The answer choices are: A, 12. B, 12.5. C, 13. D, 13.5. E, 14."),

    5: ("What is the value of 1 minus 2 plus 3 minus 4, continuing this alternating pattern, "
        "plus 2017 minus 2018? "
        "The answer choices are: A, negative 1010. B, negative 1009. C, 1008. D, 1009. E, 1010."),

    6: ("On a trip to the beach, Anh traveled 50 miles on the highway and 10 miles on a coastal access road. "
        "He drove three times as fast on the highway as on the coastal road. "
        "If Anh spent 30 minutes driving on the coastal road, "
        "how many minutes did his entire trip take? "
        "The answer choices are: A, 50. B, 70. C, 80. D, 90. E, 100."),

    7: ("The 5-digit number 2, 0, 1, 8, U is divisible by 9. "
        "What is the remainder when this number is divided by 8? "
        "The answer choices are: A, 1. B, 3. C, 5. D, 6. E, 7."),

    8: ("Mr. Garcia asked the members of his health class how many days last week "
        "they exercised for at least 30 minutes. The results are summarized in a bar graph. "
        "What was the mean number of days of exercise last week, "
        "rounded to the nearest hundredth, reported by the students in his class? "
        "The answer choices are: A, 3.50. B, 3.57. C, 4.36. D, 4.50. E, 5.00."),

    9: ("Tyler is tiling the floor of his 12-foot by 16-foot living room. "
        "He plans to place one-foot by one-foot square tiles to form a border along the edges of the room "
        "and to fill in the rest of the floor with two-foot by two-foot square tiles. "
        "How many tiles will he use? "
        "The answer choices are: A, 48. B, 87. C, 89. D, 96. E, 120."),

    10: ("The harmonic mean of a set of non-zero numbers is the reciprocal of the average of the reciprocals of the numbers. "
         "What is the harmonic mean of 1, 2, and 4? "
         "The answer choices are: "
         "A, 3 over 7. B, 7 over 12. C, 12 over 7. D, 7 over 4. E, 7 over 3."),

    11: ("Abby, Bridget, and four of their classmates will be seated in two rows of three for a group picture. "
         "If the seating positions are assigned randomly, "
         "what is the probability that Abby and Bridget are adjacent to each other in the same row or the same column? "
         "The answer choices are: "
         "A, 1 over 3. B, 2 over 5. C, 7 over 15. D, 1 over 2. E, 2 over 3."),

    12: ("The clock in Sri's car, which is not accurate, gains time at a constant rate. "
         "One day as he begins shopping, he notes that his car clock and his watch, which is accurate, "
         "both say 12:00 noon. When he is done shopping, his watch says 12:30 and his car clock says 12:35. "
         "Later that day, Sri loses his watch. He looks at his car clock and it says 7:00. "
         "What is the actual time? "
         "The answer choices are: A, 5:50. B, 6:00. C, 6:10. D, 6:30. E, 6:50."),

    13: ("Laila took five math tests, each worth a maximum of 100 points. "
         "Laila's score on each test was an integer between 0 and 100, inclusive. "
         "Laila received the same score on the first four tests, and she received a higher score on the last test. "
         "Her average score on the five tests was 82. "
         "How many values are possible for Laila's score on the last test? "
         "The answer choices are: A, 4. B, 8. C, 9. D, 10. E, 18."),

    14: ("Let N be the greatest five-digit number whose digits have a product of 120. "
         "What is the sum of the digits of N? "
         "The answer choices are: A, 15. B, 16. C, 17. D, 23. E, 15."),

    15: ("In the diagram, a diameter of each of the two smaller circles is a radius of the larger circle. "
         "If the two smaller circles have a combined area of 1 square unit, "
         "what is the area of the shaded region in square units? "
         "The answer choices are: A, one-half. B, 1. C, 3 over 2. D, 2. E, 5 over 2."),

    16: ("Professor Chang has nine different language books lined up on a bookshelf: "
         "2 Arabic, 3 German, and 4 Spanish. "
         "How many ways are there to arrange the nine books on the shelf "
         "keeping the Arabic books together and keeping the Spanish books together? "
         "The answer choices are: A, 1152. B, 2016. C, 2304. D, 1152. E, 5765760."),

    17: ("Bella begins to walk from her house toward her friend Ella's house. "
         "At the same time, Ella begins to ride her bicycle toward Bella's house. "
         "They each maintain a constant speed, and Ella rides 5 times as fast as Bella walks. "
         "The distance between their houses is 10,560 feet, "
         "and Bella covers 2.5 feet with each step. "
         "How many steps will Bella take by the time she meets Ella? "
         "The answer choices are: A, 704. B, 845. C, 1056. D, 1760. E, 3520."),

    18: ("How many positive factors does the number 2 cubed times 3 to the 4th "
         "times 5 squared times 7 to the 6th have? "
         "The answer choices are: A, 15. B, 35. C, 120. D, 256. E, 420."),

    19: ("In a sign pyramid, a cell gets a plus sign if the two cells below it have the same sign, "
         "and it gets a minus sign if the two cells below it have different signs. "
         "The diagram illustrates a sign pyramid with four levels. "
         "How many possible ways are there to fill the four cells in the bottom row "
         "to produce a plus sign at the top of the pyramid? "
         "The answer choices are: A, 2. B, 4. C, 6. D, 8. E, 16."),

    20: ("In triangle ABC, a point E is on AB with AE equals 1 and EB equals 2. "
         "Point D is on AC so that DE is parallel to BC, "
         "and point F is on BC so that EF is parallel to AC. "
         "What is the ratio of the area of quadrilateral CDEF to the area of triangle ABC? "
         "The answer choices are: A, 1 over 3. B, 4 over 9. C, 1 over 2. D, 5 over 9. E, 2 over 3."),

    21: ("How many positive three-digit integers have a remainder of 2 when divided by 6, "
         "a remainder of 5 when divided by 9, and a remainder of 7 when divided by 11? "
         "The answer choices are: A, 1. B, 2. C, 3. D, 4. E, 5."),

    22: ("Point E is the midpoint of side CD in square ABCD, "
         "and segment BE meets diagonal AC at point F. "
         "The area of quadrilateral AFED is 45 square units. "
         "What is the area of square ABCD? "
         "The answer choices are: A, 100. B, 108. C, 120. D, 144. E, 196."),

    23: ("From a regular octagon, a triangle is formed by connecting three randomly chosen vertices of the octagon. "
         "What is the probability that at least one of the sides of the triangle "
         "is also a side of the octagon? "
         "The answer choices are: A, 2 over 7. B, 5 over 42. C, 11 over 14. D, 5 over 7. E, 6 over 7."),

    24: ("In cube ABCDEFGH with opposite vertices C and E, "
         "J and I are the midpoints of segments FB and HD, respectively. "
         "Let R be the ratio of the area of the cross-section EJCI "
         "to the area of one of the faces of the cube. "
         "What is R squared? "
         "The answer choices are: A, 5 over 4. B, 4 over 3. C, 3 over 2. D, 2. E, 5 over 2."),

    25: ("How many perfect cubes lie between 2 to the 8th power and 2 to the 18th power, inclusive? "
         "The answer choices are: A, 4. B, 9. C, 10. D, 57. E, 58."),
}

BUTTON_HTML = '''      <div style="margin:10px 0 14px 0;">
        <button onclick="mathReadAloud(this.getAttribute('data-text'))" 
                data-text="{text}"
                style="background:#2d6aa0;color:#fff;border:none;padding:8px 18px;font-size:14px;border-radius:4px;cursor:pointer;margin-right:8px;">
          &#9654; Read Aloud
        </button>
        <button onclick="mathStopSpeech()"
                style="background:#888;color:#fff;border:none;padding:8px 14px;font-size:14px;border-radius:4px;cursor:pointer;">
          &#9646;&#9646; Stop
        </button>
      </div>'''

TTS_SCRIPT = '  <script src="js/tts.js" type="text/javascript"></script>\n'

repo_dir = os.path.dirname(os.path.abspath(__file__))

for prob_num, audio_text in AUDIO_TEXTS.items():
    fname = os.path.join(repo_dir, f'AMC8_2018_{prob_num}.html')
    if not os.path.exists(fname):
        print(f'MISSING: {fname}')
        continue

    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()

    # Skip if already patched
    if 'mathReadAloud' in html:
        print(f'Problem {prob_num}: already patched, skipping')
        continue

    # Add tts.js script tag after the last existing <script> in <head>
    if TTS_SCRIPT.strip() not in html:
        # Insert before </head>
        html = html.replace('</head>', TTS_SCRIPT + '</head>', 1)

    # Build button HTML (escape quotes in text for HTML attribute)
    safe_text = audio_text.replace('"', '&quot;').replace("'", '&#39;')
    button = BUTTON_HTML.format(text=safe_text)

    # Insert button before the question <p> tag — find <h2> with problem title, then insert before <form> or <p><b>
    # Strategy: insert the button div right after <script>setUpAnswers();</script> or after <h2>...</h2><div class="clr">
    # Find insertion point: after <script>setUpAnswers(); or after the article h2/clr block
    inserted = False

    # Pattern 1: after setUpAnswers(); (problems 1-11)
    m = re.search(r'(<script>\s*setUpAnswers\(\);\s*</script>)', html)
    if m:
        html = html[:m.end()] + '\n' + button + html[m.end():]
        inserted = True

    if not inserted:
        # Pattern 2: after <h2>AMC 8 2018 - Problem N</h2><div class="clr"></div>
        m = re.search(r'(<h2>AMC 8 2018[^<]*</h2>\s*<div class="clr"></div>)', html)
        if m:
            html = html[:m.end()] + '\n' + button + html[m.end():]
            inserted = True

    if not inserted:
        # Pattern 3: after <div class="article"> block start
        m = re.search(r'(<div class="article">)', html)
        if m:
            html = html[:m.end()] + '\n' + button + html[m.end():]
            inserted = True

    if not inserted:
        print(f'Problem {prob_num}: could not find insertion point')
        continue

    with open(fname, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'Problem {prob_num}: patched OK')

print('Done.')
