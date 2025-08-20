#!/usr/bin/env python3
"""
Debug filvägsextraktion
"""

import sys
import re
from pathlib import Path

# Add project paths
project_root = Path(__file__).parent.absolute()
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "api"))

def test_file_path_extraction():
    """Test filvägsextraktion"""
    
    # Test string
    test_request = "jag behöver hjälp med att planera instudering av denna boken: /home/bjorn/Dokument/Seccondbrain/3-Resources/books/philosophy/An Introduction to Moral Philosophy/An Introduction to Moral Philosophy and Moral Education.pdf"
    
    print(f"Test request: {test_request}")
    print()
    
    # Test patterns
    patterns = [
        r'~/[^:]+\.pdf',
        r'/home/[^:]+\.pdf',
        r'~/[^:]+\.epub', 
        r'/home/[^:]+\.epub',
        r'~/[^:]+\.txt',
        r'/home/[^:]+\.txt',
        r'[^:]*[Dd]okument[^:]*\.pdf',
        r'[^:]*[Bb]ook[s]?[^:]*\.pdf'
    ]
    
    for i, pattern in enumerate(patterns):
        match = re.search(pattern, test_request)
        print(f"Pattern {i+1}: {pattern}")
        if match:
            print(f"  Match: {match.group(0)}")
        else:
            print(f"  No match")
        print()
    
    # Generell pattern
    general_patterns = [
        r'[^:\s]*\.pdf',
        r'[^:\s]*\.epub', 
        r'[^:\s]*\.txt'
    ]
    
    print("General patterns:")
    for pattern in general_patterns:
        matches = re.findall(pattern, test_request)
        if matches:
            print(f"  Pattern {pattern}: {matches}")
            longest = max(matches, key=len)
            print(f"  Longest: {longest}")

if __name__ == "__main__":
    test_file_path_extraction()
