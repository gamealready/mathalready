#!/usr/bin/env python3
"""Fix P15, P16, P17 JavaScript answer logic bugs."""

import re, os

repo = os.path.dirname(os.path.abspath(__file__))

fixes = {
    # P15: midVariableRnd randomly 1-5 → should be 1 (shaded area = 1 sq unit)
    # Also choices are fractional so can't use consecutive formula — hardcode them
    15: {
        'find':    r'let midVariableRnd = \(rand_temp\);',
        'replace': 'let midVariableRnd = 1;',
        'extra': [
            # Fix the consecutive formula to hardcoded fractional choices
            (r'var answerA=String\(ans\+\(\(1-rightAnsLocation\+5\)%5\)\);',
             "var answerA='1/4';"),
            (r'var answerB=String\(ans\+\(\(2-rightAnsLocation\+5\)%5\)\);',
             "var answerB='1/3';"),
            (r'var answerC=String\(ans\+\(\(3-rightAnsLocation\+5\)%5\)\);',
             "var answerC='1/2';"),
            (r'var answerD=String\(ans\+\(\(4-rightAnsLocation\+5\)%5\)\);',
             "var answerD='1';"),
            (r'var answerE=String\(ans\+\(\(5-rightAnsLocation\+5\)%5\)\);',
             "var answerE='pi/2';"),
            # rightAnsLocation must be hardcoded to 4 (D=1 is the correct answer)
            (r'let rightAnsLocation = Math\.floor\(\(Math\.random\(\) \* 5\) \+ 1\);',
             'let rightAnsLocation = 4;'),
        ]
    },
    # P16: midVariableRnd = rand_temp+1 (2 or 3) → must be 2 (for 2 Arabic books)
    16: {
        'find':    r'let midVariableRnd = \(rand_temp\+1\);',
        'replace': 'let midVariableRnd = 2;',
    },
    # P17: midVariableRnd = 10560+60*(rand_temp-1) → must be 10560 (fixed distance)
    17: {
        'find':    r'let midVariableRnd = 10560\+60\*\(rand_temp-1\);',
        'replace': 'let midVariableRnd = 10560;',
    },
}

for prob, spec in fixes.items():
    fname = os.path.join(repo, f'AMC8_2018_{prob}.html')
    with open(fname, 'r', encoding='utf-8') as f:
        html = f.read()
    original = html

    # Primary fix
    html2 = re.sub(spec['find'], spec['replace'], html)
    if html2 == html:
        print(f'P{prob}: primary pattern NOT found')
    else:
        html = html2
        print(f'P{prob}: midVariableRnd fixed')

    # Extra fixes (P15 only)
    for find_pat, replace_str in spec.get('extra', []):
        html2 = re.sub(find_pat, replace_str, html)
        if html2 != html:
            print(f'P{prob}:   + extra fix: {replace_str[:60]}')
        html = html2

    if html != original:
        with open(fname, 'w', encoding='utf-8') as f:
            f.write(html)
        print(f'P{prob}: saved')
    else:
        print(f'P{prob}: no changes written')

print('Done.')
