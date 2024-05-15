# Create a map canvas object
mc = iface.mapCanvas()

# get layers
pool_layer = QgsProject.instance().mapLayersByName("public_swimming_pools")[0]
districts_layer = layer = QgsProject.instance().mapLayersByName("Muenster_City_Districts")[0]

# get pool fields
pool_fields = pool_layer.fields()

# Getting access to the layers data provider and to the layers capabilities
pool_provider = pool_layer.dataProvider()
pool_capabilities = pool_provider.capabilitiesString()
print(pool_capabilities)

# function to add the column "City Districts" (due to length limitations its)
def add_CityDistricts_Column(new_field_name):
    #check if method is available
    if "Attribute hinzufügen" in pool_capabilities or "Add Features" in pool_capabilities:
        district_field = QgsField(new_field_name, QVariant.String, len = 50)
        
        # add field and update it
        pool_provider.addAttributes([district_field])
        pool_layer.updateFields()
    
        print("City District wurde erfolgreich den pools hinzugefügt")
    else:
        print("Fields können nicht zum Layer hinzugefügt werden")
   
   
def change_type(feature_id, feature):
    # check if method is available
    if "Change Attribute Values" in pool_capabilities or "Attributwerte ändern" in pool_capabilities:
        
        # check if H or F are the Type and then change the value to Hallenbad/Freibad
        if feature["Type"] == "H":
            # Create a dictionary with column and value to change
            attributes = {pool_fields.indexOf("Type"):"Hallenbad"}

            # Use the changeAttributeValues methode from the provider to 
            # process the attribute change for the specific feature id
            provider.changeAttributeValues({feature_id:attributes})
        elif feature["Type"] == "F":
    
            # Create a dictionary with column and value to change
            attributes = {pool_fields.indexOf("Type"):"Freibad"}
    
            # Use the changeAttributeValues methode from the provider to 
            # process the attribute change for the specific feature id
            provider.changeAttributeValues({feature_id:attributes})            
        else:
            pass
            
        print(f"Feature:  {feature_id} wurde geändert")
    else:
        print("Feature dieses Layers können nicht verändert werden")                



def check_contained(new_field_name):
    
    add_CityDistricts_Column(new_field_name)

    #iterate over each pool and district to check in which district the pool lays
    for pool in pool_layer.getFeatures():
        
        #change type for every attribute of pool layer
        feature_id = pool.id()
        change_type(feature_id, pool)
            
        for district in districts_layer.getFeatures():
            
            pool_geom = pool.geometry()
            if pool_geom.within(district.geometry()):                
                
                #aus mir unverständliche Gründen erkennt er "City_District" bzws. "City_Distr" nicht, deshalb gehardcoded
                attribute = {2: district["Name"]}
                pool_provider.changeAttributeValues({feature_id: attribute})

check_contained("City_District")
    
    