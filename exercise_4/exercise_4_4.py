#Is required for using the processing tools
import processing

mc = iface.mapCanvas()

#Access the Schools and Muenster_City_District Layers
schools = QgsProject.instance().mapLayersByName('Schools')
schools = schools[0]
districts = QgsProject.instance().mapLayersByName('Muenster_City_Districts')
districts = districts[0]



# Run "Count points in polygon" algorithm
result = processing.run("qgis:countpointsinpolygon", {
    'POLYGONS': districts,
    'POINTS': schools,
    'FIELD': None,
    'OUTPUT': 'TEMPORARY_OUTPUT'
})

# Get the output layer from the result
output_layer = result['OUTPUT']

# Create a dictionary to store the count of schools per district
district_school_count = {}

# Iterate through features in the output layer and print the results
for feature in output_layer.getFeatures():
    district_name = feature['P_DISTRICT']
    count = feature['NUMPOINTS']

    if district_name in district_school_count:
        district_school_count[district_name] += count
    else:
        district_school_count[district_name] = count

# Print the aggregated counts for each district
for district_name, count in district_school_count.items():
    print(f"{district_name}: {count}")
