import csv
import re
from bs4 import BeautifulSoup
import glob

# Define the regex patterns
pattern_raw = re.compile(r'(.*?), (.*), (mm\. \d+-\d+)')
pattern_generic = re.compile(r'((.* )?(Cantata|Concerto|Symphony|Sonata|Trio|Quartet|Quintet|Sextet|Suite|Prelude|Mass|Sinfonia|Mazurka|Waltz|Overture|Requiem|Etude|Minuet|Rondo|Berceuse|Ecossaisen|Menuett|Chorale|Fantasy|Ballade|Sonatina|Caprice|Intermezzo|Partita|Nocturne|Capriccio)( .*)?)(, )?')
pattern_mvt = re.compile(r'mvt\. \d')
pattern_catalog = re.compile(r'((((op|op\. posth|D|K)\. )|BWV |HWV |WoO |Hob\. [A-Z]*:)\d+[a-z]?)( no. \d+)?')

# Function to parse HTML files and collect data
def parse_html_files(file_paths):
    rows = []
    for file_path in file_paths:
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')
            
            topic = ""
            subtopic1 = ""
            subtopic2 = ""
            
            for element in soup.find_all(['h1','h2', 'h3', 'table']):
                if element.name == 'h1':
                    topic = element.get_text(strip=True)
                elif element.name == 'h2':
                    subtopic1 = element.get_text(strip=True)
                elif element.name == 'h3':
                    subtopic2 = element.get_text(strip=True)
                elif element.name == 'table':
                    table_rows = element.find_all('tr')
                    for row in table_rows:
                        cols = row.find_all('td')
                        if len(cols) >= 3:
                            raw_ex_info = cols[0].get_text(strip=True)
                            mp3 = cols[1].find('a')['href'] if cols[1].find('a') else ''
                            pdf = cols[2].find('a')['href'] if cols[2].find('a') else ''
                            rows.append([topic, subtopic1, subtopic2, raw_ex_info, None, None, None,
                                        None, None, None, None, None, None, None, mp3, pdf])
    return rows

# Function to parse the raw info
def process_csv(file_path, rows):
    with open(file_path, mode='w', newline='', encoding='utf-8') as outfile:
        writer = csv.writer(outfile)
        # Write the header row
        writer.writerow(['topic', 'subtopic1', 'subtopic2', 'raw_ex_info', 'composer', 
                        'raw_ex_title', 'raw_ex_mm', 'larger_work', 'generic_title', 'piece_title', 
                        'catalog_no', 'movement', 'measure_start', 'measure_end', 'mp3', 'pdf'])
        
        # Break raw info into composer, title, and measure numbers
        for row in rows:
            match = pattern_raw.search(row[3])
            if match:
                row[4] = match.group(1)
                row[5] = match.group(2)
                row[6] = match.group(3)
            writer.writerow(row)

        # Find generic title
        # for row in rows:
        #     match = pattern_generic.search(row[5])
        #     if match:
        #         row[4] = match.group(1)
        #         row[5] = match.group(2)
        #         row[6] = match.group(3)
        #     writer.writerow(row)

# Main script
html_files = glob.glob('../../docs/_site/2024/12/01/*.html')  # Adjust the path and pattern as needed
rows = parse_html_files(html_files)
output_file = 'output.csv'
process_csv(output_file, rows)

print("Data has been successfully extracted to output.csv")
