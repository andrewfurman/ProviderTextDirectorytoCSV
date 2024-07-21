"""
This function takes a string containing data from many different healthcare providers and identifies strings containing the information for an individual provider, then sends that string containing info for an individual provider to SaveProviderString.py.
"""

import re

def identify_provider_strings(content):
    # Updated regular expression to match blocks of provider information.
    # This regex includes the name and title in the captured groups.
    provider_blocks = re.findall(r'([A-Z ,]+,\s*[A-Z ]+.*?)\n(?=[A-Z ,]+,\s*[A-Z ]+|\Z)', content, re.DOTALL)

    return provider_blocks