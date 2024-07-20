import csv
import re

def process_provider_data(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    providers = re.split(r'\n(?=[A-Z]+,\s[A-Z]+)', content)

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = [
            'Provider ID#', 'Last Name', 'First Name', 'Middle Initial',
            'Professional Medical Title', 'Affiliation', 'Medical Specialty',
            'Street Address', 'City', 'State', 'Zip Code', 'Phone Number',
            'Restricted Panel', 'Provider E-Perscribes', 
            'Hospital Affiliation Code 1', 'Hospital Affiliation Code 2',
            'Hospital Affiliation Code 3', 'Hospital Affiliation Code 4',
            'Hospital Affiliation Code 5', 'Hospital Affiliation Code 6',
            'Hospital Affiliation Code 7', 'Hospital Affiliation Code 8',
            'Hospital Affiliation Code 9', 'Hospital Affiliation Code 10'
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for provider in providers:
            if not provider.strip():
                continue

            lines = provider.strip().split('\n')
            print("Processing provider:", lines)  # Debugging print

            name_parts = re.match(r'([^,]+),\s*(.+?)\s*,\s*([A-Z-]+)$', lines[0])
            if not name_parts:
                print("Name parts not matched:", lines[0])  # Debugging print
                continue

            last_name, first_name, title = name_parts.groups()
            name_split = first_name.split()
            first_name = name_split[0]
            middle_initial = name_split[1][0] if len(name_split) > 1 else ""

            data = {
                'Provider ID#': '',
                'Last Name': last_name,
                'First Name': first_name,
                'Middle Initial': middle_initial,
                'Professional Medical Title': title,
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

            for i in range(1, 11):
                data[f'Hospital Affiliation Code {i}'] = ''

            address_started = False
            for line in lines[1:]:
                if 'Restricted Panel' in line:
                    data['Restricted Panel'] = 'RestrictedPanel'
                elif 'Rx' in line:
                    data['Provider E-Perscribes'] = 'YesEPerscribe'
                elif '#' in line:
                    # Assume Provider ID is the part of the line starting with '#'
                    provider_id_match = re.search(r'#\S+', line)
                    if provider_id_match:
                        data['Provider ID#'] = provider_id_match.group(0).strip('# ')
                        print("Extracted Provider ID#:", data['Provider ID#'])  # Debugging print
                elif not address_started and not line[0].isdigit():
                    if data['Medical Specialty']:
                        data['Affiliation'] = line.strip()
                    else:
                        data['Medical Specialty'] = line.strip()
                elif line[0].isdigit() or address_started:
                    address_started = True
                    if not data['Street Address']:
                        data['Street Address'] = line.strip()
                    elif not data['City']:
                        city_state_zip = line.split(',')
                        data['City'] = city_state_zip[0].strip()
                        if len(city_state_zip) > 1:
                            state_zip = city_state_zip[1].strip().split()
                            data['State'] = state_zip[0]
                            if len(state_zip) > 1:
                                data['Zip Code'] = state_zip[1]
                    elif not data['Phone Number']:
                        data['Phone Number'] = line.strip()

            hospital_codes = [code for code in lines if len(code) == 3 and code.isupper()]
            for i, code in enumerate(hospital_codes[:10], 1):
                data[f'Hospital Affiliation Code {i}'] = code

            writer.writerow(data)

if __name__ == "__main__":
    process_provider_data('input.txt', 'output.csv')