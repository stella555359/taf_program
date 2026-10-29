#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Quick fix for broken HTML files"""

import sys
from pathlib import Path

def fix_html_file(html_path):
    """Fix the broken newline in JavaScript"""
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix the broken newline
    old_text = "tooltip += '\nCustom Rule Applied';"
    new_text = "tooltip += ' | Custom Rule Applied';"
    
    if old_text in content:
        content = content.replace(old_text, new_text)
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'Fixed: {html_path}')
        return True
    else:
        print(f'Pattern not found in: {html_path}')
        return False


def main():
    # Fix all HTML files in reports directory
    reports_dir = Path(__file__).parent.parent / 'reports'
    fixed_count = 0
    
    for html_file in reports_dir.glob('*.html'):
        if fix_html_file(html_file):
            fixed_count += 1
    
    print(f'\nFixed {fixed_count} HTML files')


if __name__ == '__main__':
    main()
