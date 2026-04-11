import json

company = {
    "name": "ChaosCorp",
    "founded": 2019,
    "active": True,
    "departments":{
        "engineering": {
            "head": "Alice",
            "budget": 500000,
            "employees": [
                {"name": "bob", "age": 25, "skills":["python", "SQL"]},
                {"name": "charlie", "age": None, "skills": []},

            ],
            "sub_teams":{
                "backend": ["bob"],
                "frontend": [],
                "ml": None
            }
        },
        "sales":{
            "head": None,
            "budget": 0,
            "employees": []
        }
    },
    "metadata": {
        "last_updated": "2024-01-15",
        "version": 3.1,
        "tags": ["startup", "messy", "growing"],
        "notes": "this data has intentinal gaps and problems"
    }
}

print("original dictionary:")
print(company)
print()


with open("company.json", "w") as f:
    json.dump(company, f, indent=4)

print("saved to company.json!!")

with open("company.json", "r") as f:
    loaded = json.load(f)

print("\n loaded back from company.json:")

if company == loaded:
    print("INTERGITY CHECKPASSED: data matches perfectly!")
else:
    print("INTEGRITY CHECK FAILED: data was corrupted!")


print()
print("deep access test:")
print(f" company: {loaded['name']}")
print(f" eng head: {loaded['departments']['engineering']['head']}")
print(f" bob's skills: {loaded['departments']['engineering']['employees'][0]['skills']}")
print(f" sales head: {loaded['departments']['sales']['head']}")
print(f" ml team: {loaded['departments']['engineering']['sub_teams']['ml']}")
