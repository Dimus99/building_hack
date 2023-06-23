import csv
import xlsxwriter

name = "./data/dataset_ksg.csv"
output_file = "./research/output/dataset_ksg.xlsx"
rows = {}

with open(name, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file)
    
    # Loop through each row in the CSV file
    i = 0
    # Skip the first row
    head = next(csv_reader)
    for row in csv_reader:

        # Print the contents of each row
        rows[row[3]] = rows.get(row[3], [])
        rows[row[3]].append(tuple(row))
    
workbook = xlsxwriter.Workbook(output_file)
for key in rows:
    worksheet = workbook.add_worksheet(key)
    for r, row in enumerate([head] + rows[key]):
        for c, cell in enumerate(row):
            worksheet.write(r, c, cell)
workbook.close()

print(f"Saved {len(rows)} rows to {output_file}")
