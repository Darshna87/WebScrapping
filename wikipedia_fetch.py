
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd


android_url = "https://en.wikipedia.org/wiki/Android_version_history"

android_data = urlopen(android_url)
print(type(android_data))

android_html = android_data.read()
#print(android_html)
android_data.close()

android_soup = soup(android_html, 'html.parser')
print(android_soup)

print(type(android_soup))

print(android_soup.findAll('h1', {}))

tables = android_soup.findAll('table', {"class": "wikitable"})

print(len(tables))
android_table = tables[0]
print(android_table)

headers = android_table.findAll('th')
print(len(headers))

column_titles = [ct.text[:-1] for ct in headers] #slicing with -1 to avoid \n in text
print(column_titles)

rows_data = android_table.findAll('tr')[1:]# slicing 1st raw to avoid header row
print(len(rows_data))

first_row = rows_data[0].findAll('td')
for data in first_row:
    print(data.text[:-1])

table_rows = []
for row in rows_data:

    current_row = []
    columns_data = row.findAll('td', {})

    for d in columns_data:
        current_row.append(d.text[:-1])

    table_rows.append(current_row)

print(table_rows)
print(len(table_rows))

filename = "android_version_history.csv"
with open(filename, 'w', encoding='utf-8') as f:

    header_string = ",".join(column_titles)
    header_string += "\n"
    f.write(header_string)

    for row in table_rows:
        row_string = ''
        for word in row:
            word = word.replace(',', '')
            row_string += word + ","

        row_string= row_string[:-1] # removing , at the end
        row_string += "\n"
        f.write(row_string)

df = pd.read_csv(filename)
df.head(n=2)


