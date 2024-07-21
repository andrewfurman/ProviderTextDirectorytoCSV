"""
This function takes a string containing data for many different healthcare providers and identifies the individual provider records.

Every provider record in the content will start with a name in ALL CAPs.
Examples of provider names and titles in all caps (these names may appear on a single line in the content, or displayed across multiple lines):
BLACK, CATHERINE M, APRN
CHIU, JUDY, DO
DOBRITA, ALINA I, MD
HYMAN, ERIKA M, APRN

Every provider record will end with a Provider ID. 
Examples of Provider IDs:
#A3292
#B2800
"""

import re

def identify_provider_strings(content):
    # Regex pattern to capture provider records
    pattern = re.compile(
        r'(?:^[A-Z ,]+\s*(?:[A-Z]+\s*)*(?:[A-Z, ]*\n)*(?:[A-Z]+\s*)*\n(?:.*\n)*?)'
        r'(?:#|SFH #|HFD #|BAY Rx #|Rx #| BAY #)[A-Za-z0-9]+',
        re.MULTILINE
    )
    
    provider_blocks = re.findall(pattern, content)
    
    # Clean up each provider block to remove leading/trailing whitespace
    provider_blocks = [block.strip() for block in provider_blocks]
    
    return provider_blocks