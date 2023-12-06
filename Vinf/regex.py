import re,csv
csv_file = "matches.csv"

with open('downloaded_page.txt', 'r', encoding='utf-8') as file:
    html_content = file.read()

h2_pattern = re.compile(r'<font color="#fcfcfc" size="2">\s*All matches\s*</font>')

matches = [[]]

h2_match = re.search(h2_pattern, html_content)

h2_matches = re.finditer(h2_pattern, html_content)

for h2_match in h2_matches:
    league_pattern = r'league=(\w+)_'
    table_pattern = r'<table[^>]*>.*?<\/table>'
    table_matches = re.finditer(table_pattern, html_content[h2_match.end():], re.DOTALL)
    count = 0
    year_pattern = r'(202[0-3]|201[89])[^<]*'

    date = re.search(year_pattern, html_content[h2_match.end():])
    league = re.search(league_pattern, html_content[h2_match.end():])

    found_year = date.group(1)[:4]
    found_league = league.group(1)

    for table_match in table_matches:
        if count == 1:

            table_html = table_match.group(0)
            row_pattern = r'<tr[^>]*>.*?<\/tr>'
            rows = re.findall(row_pattern, table_html, re.DOTALL)

            for row in rows:

                cell_pattern = r'<t[dh][^>]*>(.*?)<\/t[dh]>'
                cells = re.findall(cell_pattern, row, re.DOTALL)

                if len(cells) >= 4:

                    cell_data = [re.sub(r'<[^>]*>', '', cell).strip() for cell in cells]
                    cell_data.insert(0, found_year)
                    cell_data.insert(0, found_league)


                    matches.append(cell_data[0:6])

            break
        count += 1
    else:
        print("Second table not found after 'Player Stats'.")

with open(csv_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(["id", "league", "season", "date", "home", "score", "away"])

    id = 0
    for match in matches:
        if len(match) > 2:
            writer.writerow([id, match[0], match[1], match[2], match[3], match[4], match[5]])
            id+=1

