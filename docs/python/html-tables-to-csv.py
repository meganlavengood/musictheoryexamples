import csv
from bs4 import BeautifulSoup

# Read the HTML file
with open('docs/_site/2024/12/01/37.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

# Create a CSV file to write the output
with open('output.csv', 'w', newline='', encoding='utf-8') as csvfile:
    csvwriter = csv.writer(csvfile)
    # Write the header row
    csvwriter.writerow(['topic', 'subtopic1', 'subtopic2', 'raw_ex_title', 'composer', 
                        'larger_work', 'generic_title', 'piece_title', 'catalog_no', 
                        'movement', 'measure_start', 'measure_end', 'mp3', 'pdf'])

    # Initialize variables
    subtopic1 = ""
    subtopic2 = ""

    # Extract data
    for element in soup.find_all(['h2', 'h3', 'table']):
        if element.name == 'h2':
            subtopic1 = element.get_text(strip=True)
        elif element.name == 'h3':
            subtopic2 = element.get_text(strip=True)
        elif element.name == 'table':
            rows = element.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) >= 3:
                    raw_ex_title = cols[0].get_text(strip=True)
                    mp3 = cols[1].find('a')['href'] if cols[1].find('a') else ''
                    pdf = cols[2].find('a')['href'] if cols[2].find('a') else ''
                    csvwriter.writerow([None, subtopic1, subtopic2, raw_ex_title, None, 
                                        None, None, None, None, None, None, None, 
                                        mp3, pdf])

print("Data has been successfully extracted to output.csv")
