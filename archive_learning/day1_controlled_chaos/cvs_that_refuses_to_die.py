import csv

def read_csv_safe(filename, target_column):
    """
    Reads a csv file and calculates the average of a numeric column.
    Handles EVERY disaster that could happen
    """

    try:
        file = open(filename, "r")
    except FileNotFoundError:
        print(f"Error: The file '{filename}' was not found!.")
        print(" Check the file name and try again.")
        return
    
    reader = csv.reader(file)




    try:
        header = next(reader)
    except StopIteration:
        print("ERROR: file is empty! no header found.")
        file.close()
        return
    
    print(f"column found: {header}")

    if target_column not in header:
        print(f"ERROR: column '{target_column}' not found!")
        print(f" available columns: {header}")
        file.close()
        return
    col_index = header.index(target_column)


    total = 0
    count = 0
    row_count = 0
    bad_rows = []
    
    for row in reader:
        row_count += 1

        if col_index >= len(row):
            bad_rows.append(row_count +1)
            print(f"WARNING: row {row_count +1}: missing columns, skipped")
            continue

        value = row[col_index]


        if value.strip() == "":
            bad_rows.append(row_count +1)
            print(f"WARNING: row {row_count +1}: empty value, skipped")
            continue

        try:
            numeric_value = float(value)
        except ValueError:
            bad_rows.append(row_count +1)
            print(f"WARNING: row {row_count +1}: '{value}' is not a number, skipped")
            continue
        total += numeric_value
        count += 1

    file.close()


    print("\n" + "=" * 40)
    print("REPORT")
    print("=" * 40)
    print(f"total data rows: {row_count}")
    print(f" clean rows: {count}")
    print(f" bad rows: {len(bad_rows)}")

    if count > 0:
        average = total / count
        print(f"average {target_column}: {average:.2f}")
    else:
        print(f" no valid data to calculate average!")

    if bad_rows:
        print(f" problem rows : {bad_rows}")

    print("=" * 40)


print("\n TEST 1: normal file")
read_csv_safe("employee.csv", "salary")

print("\n TEST 2: wrong filename")
read_csv_safe("ghost_file.csv", "salary")

print("\n TEST 3: wrong column name")
read_csv_safe("employee.csv", "pizza")

print("\n TEST 4: corrupt file")
read_csv_safe("employee.cvs", "salary")

