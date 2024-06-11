#define workspace first

# Define output feature class
output_fc = "active_assets"

# get all point geometry feature classes and exclude the "active_assets"
fc_list = arcpy.ListFeatureClasses(feature_type='Point')
fc_list = [fc for fc in fc_list if fc != output_fc]

# Iterate over the feature classes
for fc in fc_list:
    # Create the search cursor
    scur = arcpy.da.SearchCursor(fc, ['SHAPE@', 'status', 'type'], "status='active'")

    # Create the insert cursor
    icur = arcpy.da.InsertCursor(output_fc, ['SHAPE@', 'status', 'type'])

    # Iterate over the search cursor and insert rows into the insert cursor
    for row in scur:
        icur.insertRow(row)

    # Delete the cursors
    del scur
    del icur

print("Done")
