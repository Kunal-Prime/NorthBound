import csv 

file = open("employee.csv", "r")
reader = csv.reader(file)
header = next(reader)

target_column = "salary"

col_index = header.index(target_column)
print(f"'{target_column}' is at position {col_index}")

total = 0 
count = 0

for row in reader:
    value = row[col_index]
    value = float(value)
    total += value
    count += 1

average = total / count
print(f"average {target_column} is {average}")
 
file.close()
