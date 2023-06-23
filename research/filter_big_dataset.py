import csv
import xlsxwriter

name = "./data/dataset_hackaton_ksg__23062023__1640_GMT3.csv"
output_file = "./research/output/dataset_big.xlsx"
rows = {}
workbook = xlsxwriter.Workbook(output_file)
worksheet = workbook.add_worksheet("first")

with open(name, mode='r') as file:
    # Create a CSV reader object
    csv_reader = csv.reader(file, delimiter=";")

    # Loop through each row in the CSV file
    i = 0
    # Skip the first row
    # head = next(csv_reader)
    rows = []
    i = 0
    while True:
        if i == 971841:
            break
        try:
            row = next(csv_reader)
        except IndexError:
            break
        except Exception as e:
            print(i, e)
            continue
        if i % 10000 == 0:
            print(i)
            
        for c, cell in enumerate(row):
            # print(row)
            worksheet.write(i, c, cell)
        
        i+=1
        
workbook.close()
        
print(f"Saved {i} rows to {output_file}")
