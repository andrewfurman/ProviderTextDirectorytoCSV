"""
This function takes a string containing provider data and saves it to output.csv.

Here are a few different examples of strings that are supported:

EXAMPLE 1:

BARANOWSKI, JENNIFER 
E, APRN
Family Nurse Practitioner
Prime Healthcare
44 Dale Rd Ste 204
Avon, CT  06001
860.674.8830
 #A3292

EXAMPLE 2:

BLACK, CATHERINE M, 
APRN
Family Nurse Practitioner
Hartford HealthCare Medical 

Group

339 W Main St
Avon, CT  06001
860.696.2150
 #B2800
 
"""

import csv
import re

def save_provider_data(provider, writer):
    lines = provider.strip().split('\n')

    data = {
        'Provider ID#': '',
        'Last Name': '',
        'First Name': '',
        'Middle Initial': '',
        'Professional Medical Title': '',
        'Affiliation': '',
        'Medical Specialty': '',
        'Street Address': '',
        'City': '',
        'State': '',
        'Zip Code': '',
        'Phone Number': '',
        'Restricted Panel': 'NotRestricted',
        'Provider E-Perscribes': 'NoEPerscribe',
    }

    # Initialize Hospital Affiliation Codes
    for i in range(1, 11):
        data[f'Hospital Affiliation Code {i}'] = ''

    line_idx = 0
    # Extracting Name and Title
    if line_idx < len(lines):
        name_title = re.match(r'([A-Z ,]+),\s*([A-Z]+)\s*(.*)', lines[line_idx])
        if name_title:
            data['Last Name'] = name_title.group(1).strip()
            first_middle = name_title.group(2).split()
            data['First Name'] = first_middle[0]
            if len(first_middle) > 1:
                data['Middle Initial'] = first_middle[1][0]
            data['Professional Medical Title'] = name_title.group(3).strip()
            line_idx += 1

    # Extracting Medical Specialty
    if line_idx < len(lines):
        data['Medical Specialty'] = lines[line_idx].strip()
        line_idx += 1

    # Extracting Affiliation if available
    while line_idx < len(lines) and lines[line_idx] and not lines[line_idx][0].isdigit():
        if data['Affiliation']:
            data['Affiliation'] += ' '
        data['Affiliation'] += lines[line_idx].strip()
        line_idx += 1

    # Extracting Address, City, State, Zip and Phone Number
    address_started = False
    while line_idx < len(lines):
        line = lines[line_idx].strip()
        if line.startswith('#'):
            data['Provider ID#'] = line
        elif re.match(r'\d', line):
            if not address_started:
                data['Street Address'] = line
                address_started = True
            elif not data['City']:
                city_state_split = line.rsplit(',', 1)
                data['City'] = city_state_split[0].strip()
                if len(city_state_split) > 1:
                    state_zip_split = city_state_split[1].strip().split()
                    if len(state_zip_split) > 1:
                        data['State'] = state_zip_split[0]
                        data['Zip Code'] = state_zip_split[1]
            elif not data['Phone Number']:
                data['Phone Number'] = line
        line_idx += 1

    # Final debugging print before writing to file
    print("Final Saved data:", data)
    writer.writerow(data)
    print("Data has been written to output.csv")  # Verify data write to CSV