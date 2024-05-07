#given code from exercise
parent = iface.mainWindow()
sCoords, bOK = QInputDialog.getText(parent, "Coordinates", "Enter coordinates as latitude, longitude", text="51.96066,7.62476")

#check if okay button clicked or cancelled
if bOK:
    # Parse the input string to get lat and lon
    latitude, longitude = map(float, sCoords.split(','))

    # Transform WGS84 coordinates to ETRS89
    source_crs = QgsCoordinateReferenceSystem('EPSG:4326')
    target_crs = QgsCoordinateReferenceSystem('EPSG:25832')  # ETRS89
    
    #initatlize transformation and transform parsed point
    transformation = QgsCoordinateTransform(source_crs, target_crs, QgsProject.instance())
    target_point = transformation.transform(QgsPointXY(longitude, latitude))

    # Check if the transformed coordinates are in a city district
    layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
    for feature in layer.getFeatures():
        if feature.geometry().contains(target_point):
            QMessageBox.information(parent, "Result", "Coordinates fall within a city district of Münster.")
            break
    else:
        QMessageBox.information(parent, "Result", "Coordinates do not fall within any city district of Münster.")
else:
    QMessageBox.warning(parent, "Input Cancelled", "User cancelled input.")