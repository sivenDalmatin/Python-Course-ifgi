import csv

#access mc
mc = iface.mapCanvas()

#use only the "Schools" Layer
layers = QgsProject.instance().mapLayersByName('Muenster — Schools')
layer = layers[0]

# decide whether to use all layer data or only selected features (just comment out what you want to use)
# features = layer.getFeatures()
features = layer.selectedFeatures()

#store features in a list, to not iterate over features twice, which would throw an error 
feature_list = []

#print Features into console
for feature in features:
    print('Name: ', feature['NAME'])
    
    #Access X and Y Coordinates
    geom = feature.geometry()
    x = geom.asPoint().x()
    y = geom.asPoint().y()
    print("X: " + str(x))
    print("Y: " + str(y))
    
    feature_list.append(feature)
    
# Change to desired Path/Filename
out_folder = '/Users/finnole/Uni/Sem 6/ArcPy:QPy/csv_files/SchoolReport.csv'

# Header for CSV Table
header = ['NAME', 'X Coordinate', 'Y Coordinates']

#Write CSV file
with open(out_folder, 'w', encoding ='UTF8', newline='') as f:
    writer = csv.writer(f, delimiter=';')
    
    #Write header
    writer.writerow(header)
    
    #Write body/data
    for feature in feature_list:
        name = feature['NAME']
        geom = feature.geometry()
        x_coord = geom.asPoint().x()
        y_coord = geom.asPoint().y()
        writer.writerow([name, x_coord, y_coord])