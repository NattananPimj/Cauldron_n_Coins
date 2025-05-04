import csv


data = []
with open('cnc_save_test.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        data.append(row)

print(data)

