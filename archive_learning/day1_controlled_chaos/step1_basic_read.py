import csv

file = open ("employee.csv", "r")

reader = csv.reader(file)

header = next(reader)
print("column names:", header)

row_count = 0
for row in reader:
    print(row)
    row_count += 1

print("total rows:", row_count)

file.close()