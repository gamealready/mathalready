#!/usr/bin/env python3
"""Fix AMC8_2018 HTML files: correct answer indices + correct image references."""

import re, os

repo = os.path.dirname(os.path.abspath(__file__))

# ── 1. Problems 1-11, 25: fix correctIdx ──────────────────────────────────────
# AoPS answer key → correct VALUE index in allAnswers array
# allAnswers are always in fixed order A,B,C,D,E → index 0-4
# AoPS key: 1=A,2=D,3=D,4=C,5=E,6=C,7=B,8=C,9=B,10=C,11=C,25=E
correct_idx = {
    1:0,   # A=14        (was 0 ✓)
    2:3,   # D=7         (was 4 ✗)
    3:3,   # D=Dan       (was 2 ✗)
    4:2,   # C=13        (was 4 ✗)
    5:4,   # E=1010      (was 1 ✗)
    6:2,   # C=80        (was 3 ✗)
    7:1,   # B=3         (was 2 ✗)
    8:2,   # C=4.36      (was 1 ✗)
    9:1,   # B=87        (was 3 ✗)
    10:2,  # C=12/7      (was 2 ✓)
    11:2,  # C=7/15      (was 4 ✗)
    25:4,  # E=58        (was 4 ✓)
}

def fix_correct_idx(html, new_idx):
    return re.sub(r'var correctIdx\s*=\s*\d+;',
                  f'var correctIdx={new_idx};', html)

# ── 2. Problems 12-24: fix rightAnswer localStorage bug ───────────────────────
# Bug: all 5 setItem calls run in sequence; 'E' always wins.
# Fix: replace all 5 calls with one call using rightAnsLocation.
OLD_PATTERN = re.compile(
    r"localStorage\.setItem\('rightAnswer','A'\);\s*"
    r"localStorage\.setItem\('rightAnswer','B'\);\s*"
    r"localStorage\.setItem\('rightAnswer','C'\);\s*"
    r"localStorage\.setItem\('rightAnswer','D'\);\s*"
    r"localStorage\.setItem\('rightAnswer','E'\);",
    re.DOTALL
)
NEW_RIGHTANSWER = "localStorage.setItem('rightAnswer',['A','B','C','D','E'][rightAnsLocation-1]);"

def fix_right_answer(html):
    return OLD_PATTERN.sub(NEW_RIGHTANSWER, html)

# ── 3. Image fixes ────────────────────────────────────────────────────────────
# P1-P11: switch _diagram.png → plain .png (full problem with numbers)
# P6, P7: currently no image → add plain .png
# P25: currently no image → add plain .png
# P12, P13, P14: remove wrong AMC8_2018_15.png reference
# P16, P17, P18: remove wrong AMC8_2018_19.png reference
# P21: remove wrong AMC8_2018_22.png reference

def switch_diagram_to_plain(html, prob):
    """Replace _diagram.png with plain .png for a given problem number."""
    old = f'images/AMC8_2018_{prob}_diagram.png'
    new = f'images/AMC8_2018_{prob}.png'
    return html.replace(old, new)

def add_image_after_h2(html, prob):
    """Add plain .png image if no img tag exists yet."""
    img_tag = (f'\n      <div style="text-align:center;margin:16px 0;">'
               f'<img src="images/AMC8_2018_{prob}.png" '
               f'alt="2018 AMC 8 Problem {prob}" style="max-width:600px;" /></div>')
    # Insert after <script>setUpAnswers();</script> or after <h2> block
    if f'AMC8_2018_{prob}.png' in html:
        return html  # already there
    m = re.search(r'<script>\s*setUpAnswers\(\);\s*</script>', html)
    if m:
        return html[:m.end()] + img_tag + html[m.end():]
    m = re.search(r'<h2>[^<]*</h2>\s*<div class="clr"></div>', html)
    if m:
        return html[:m.end()] + img_tag + html[m.end():]
    return html

def remove_wrong_image(html, wrong_img_name):
    """Remove the entire <div>...</div> or <img ...> block containing the wrong image."""
    # Try removing a wrapping div first
    pattern = re.compile(
        r'<div[^>]*>\s*<img[^>]*' + re.escape(wrong_img_name) + r'[^>]*/>\s*</div>',
        re.DOTALL
    )
    result, n = pattern.subn('', html)
    if n:
        return result
    # Fallback: just remove the bare img tag
    pattern2 = re.compile(r'<img[^>]*' + re.escape(wrong_img_name) + r'[^>]*/>', re.DOTALL)
    return pattern2.sub('', html)

# ── Apply all fixes ───────────────────────────────────────────────────────────
changes = []

for prob in range(1, 26):
    fname = os.path.join(repo, f'AMC8_2018_{prob}.html')
    if not os.path.exists(fname):
        print(f'MISSING: {fname}'); continue

    with open(fname, 'r', encoding='utf-8') as f:
        original = f.read()
    html = original

    mods = []

    # Fix 1: correctIdx for P1-P11, P25
    if prob in correct_idx:
        new_idx = correct_idx[prob]
        html2 = fix_correct_idx(html, new_idx)
        if html2 != html:
            mods.append(f'correctIdx→{new_idx}')
            html = html2

    # Fix 2: rightAnswer bug for P12-P24
    if 12 <= prob <= 24:
        html2 = fix_right_answer(html)
        if html2 != html:
            mods.append('rightAnswer bug fixed')
            html = html2

    # Fix 3: images
    if prob in range(1, 12):
        # Switch _diagram.png → plain .png
        if f'AMC8_2018_{prob}_diagram.png' in html:
            html = switch_diagram_to_plain(html, prob)
            mods.append(f'image: _diagram→plain.png')
    
    if prob in (6, 7):
        # No image currently; add plain .png
        if f'AMC8_2018_{prob}.png' not in html:
            html = add_image_after_h2(html, prob)
            mods.append(f'image: added plain.png')

    if prob == 25:
        if 'AMC8_2018_25.png' not in html:
            html = add_image_after_h2(html, prob)
            mods.append('image: added AMC8_2018_25.png')

    if prob in (12, 13, 14):
        if 'AMC8_2018_15.png' in html:
            html = remove_wrong_image(html, 'AMC8_2018_15.png')
            mods.append('image: removed wrong P15 circles image')

    if prob in (16, 17, 18):
        if 'AMC8_2018_19.png' in html:
            html = remove_wrong_image(html, 'AMC8_2018_19.png')
            mods.append('image: removed wrong P19 sign pyramid image')

    if prob == 21:
        if 'AMC8_2018_22.png' in html:
            html = remove_wrong_image(html, 'AMC8_2018_22.png')
            mods.append('image: removed wrong P22 square image')

    if html != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'P{prob:2d}: {", ".join(mods)}')
        changes.append(prob)
    else:
        print(f'P{prob:2d}: no changes needed')

print(f'\n{len(changes)} files updated: {changes}')
