data_path = "/Users/finnole/Uni/Sem 6/ArcPy:QPy/Data for Session 6/standard_land_value_muenster.csv"
csv = open(r"/Users/finnole/Uni/Sem 6/ArcPy:QPy/Data for Session 6/standard_land_value_muenster.csv", "r")
lines = csv.readlines()


for line in lines[1:]:
    print(line)