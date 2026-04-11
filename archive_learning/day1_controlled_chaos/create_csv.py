data = """name.age.salary
alice,30,50000
bob,25,60000
charlie,35,70000
diana,28,55000"""

with open("employee.csv", "w") as f:
    f.write(data)

print("CSV file created!!")