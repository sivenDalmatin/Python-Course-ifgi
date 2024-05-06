import os
from qgis.core import QgsVectorLayer, QgsProject

# Supply path to qgis install location
# QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

# Path to data and QGIS-project
#data_folder = r"C:\Users\Sven Harpering\sciebo\GIS-GK\GIS-GK_WS_23_24\GIS Data\Muenster"
data_folder = r"C:\Users\Martin\Documents\WWU\6Semester\Python\Exercise4\Muenster\Muenster"
#project_path = r"C:\Users\Sven Harpering\myFirstProject.qgz"  # for QGIS version 3+
project_path = r"C:\Users\Martin\Documents\WWU\6Semester\Python\Exercise4\mySecondProject.qgz"

# List to store paths of shapefiles
shapefile_paths = []

# Iterate through files in the data folder
for file in os.listdir(data_folder):
    # Check if file is a shapefile
    if file.endswith(".shp"):
        # Construct full path to the shapefile
        shapefile_path = os.path.join(data_folder, file)
        # Add shapefile path to the list
        shapefile_paths.append(shapefile_path)

#show in console all shapefilepaths
print(shapefile_paths)


# Create QGIS instance and "open" the project
project = QgsProject.instance()
project.read(project_path)

# Iterate through shapefile paths
for shapefile_path in shapefile_paths:
    # Extract the filename without extension
    layer_name = os.path.splitext(os.path.basename(shapefile_path))[0]
    
    # Create layer
    layer = QgsVectorLayer(shapefile_path, layer_name, "ogr")
    
    # Check if layer is valid
    if layer.isValid():
        # Add layer to project
        project.addMapLayer(layer)
    else:
        print(f"Error loading layer: {layer_name}")

# Save project
project.write()
print("Project saved successfully!")