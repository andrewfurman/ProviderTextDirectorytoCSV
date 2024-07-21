import csv
import re
from SaveProviderString import save_provider_data, save_provider_data_as_text
from IdentifyProviderString import identify_provider_strings

def process_provider_data(input_file, output_file):
    with open(input_file, 'r') as f:
        content = f.read()

    # Use the identify_provider_strings function to split the content into individual provider records.
    providers = identify_provider_strings(content)

    with open(output_file, 'w', newline='') as csvfile, open('output.txt', 'w') as txtfile:
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
        
        # Write the header to the text file
        txtfile.write(' | '.join(f"{field:<20}" for field in fieldnames) + '\n')
        txtfile.write('-' * (len(fieldnames) * 22) + '\n')  # Adjust the number of dashes based on your field length

        for provider in providers:
            if not provider.strip():
                continue
            print("\nFOUND:", provider.replace('\n', ' '))  # Debugging print for each provider
            save_provider_data(provider, writer)
            save_provider_data_as_text(provider, txtfile)

if __name__ == "__main__":
    process_provider_data('input.txt', 'output.csv')