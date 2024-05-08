# select map interface
mc = iface.mapCanvas()

#select map layer
layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]
schools_layer = QgsProject.instance().mapLayersByName("Schools")[0]


# create instance
request = QgsFeatureRequest()

# define and set clause
nameClause = QgsFeatureRequest.OrderByClause("Name", ascending = True)
orderby = QgsFeatureRequest.OrderBy([nameClause])
request.setOrderBy(orderby)

districts_names = [feature["Name"] for feature in layer.getFeatures(request)]


# make a variable that contains not only district name but also the geom features
def district_geom_available(selec_district):
    for district in layer.getFeatures():
        if district["Name"] == selec_district:
            selected_dist = district
            return selected_dist



#Search for Schools in City District
def check_schools(district):
    schools_contained = []
    
    #find centroid of selected district and set etrs89
    dist_centroid = district.geometry().centroid().asPoint()
    da = QgsDistanceArea()
    da.setEllipsoid("ETRS89")
    
    #iterate over schools. For each school look if its in the district. If so claculate the distance and return the name of the school
    for school in schools_layer.getFeatures():
        school_geom = school.geometry()
        if school_geom.within(district.geometry()):
            
            distance = da.measureLine(school_geom.asPoint(), dist_centroid) / 1000  # Convert to kilometers
            distance_rounded = round(distance, 2)
            print(distance_rounded)
            
            schools_contained.append((school["Name"], distance_rounded))
            
    return(schools_contained)

    
# open qinputdialog (given in exercise)
parent = iface.mainWindow()
sDistrict, bOk = QInputDialog.getItem(parent, "District Names", "Select District: ", districts_names)


if bOk:
    #make geometry available
    selected_district = district_geom_available(sDistrict)
    #check schools in district
    schools_in_dist = check_schools(selected_district)
    
    # Zoom to selected district
    mc.setExtent(selected_district.geometry().boundingBox())
    mc.refresh()
    
    #create body for the window
    schools_in_dist_str = "\n".join([f"{school[0]} - Distance to centroid: {school[1]} km" for school in schools_in_dist])
    QMessageBox.information(parent, f"Schools in {sDistrict}", f"{schools_in_dist_str}")
else:
    QMessageBox.warning(parent, "Schools", "User cancelled")