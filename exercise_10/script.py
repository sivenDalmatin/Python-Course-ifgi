import arcpy
def find_nearest_bus_stop(input_fc, stops_fc):
    try:
        # input feature is in Web Mercator?
        spatial_ref = arcpy.Describe(input_fc).spatialReference
        web_mercator = arcpy.SpatialReference(3857)
        
        if spatial_ref.name != web_mercator.name:
            arcpy.AddMessage("Projecting input feature class to Web Mercator projection.")
            projected_fc = "in_memory/projected_input"
            arcpy.management.Project(input_fc, projected_fc, web_mercator)
            input_fc = projected_fc
        # Near tool
        arcpy.analysis.Near(input_fc, stops_fc)
        # Use SearchCursor to get NEAR_FID and NEAR_DIST
        near_fid = None
        near_dist = None
        with arcpy.da.SearchCursor(input_fc, ["NEAR_FID", "NEAR_DIST"]) as cursor:
            for row in cursor:
                near_fid = row[0]
                near_dist = row[1]
        if near_fid is None:
            arcpy.AddMessage("No nearby bus stop found.")
            return
        # Use SearchCursor for nearest bus stop
        bus_stop_name = None
        where_clause = f"OBJECTID = {near_fid}"
        with arcpy.da.SearchCursor(stops_fc, ["Name"], where_clause) as cursor:
            for row in cursor:
                bus_stop_name = row[0]
        if bus_stop_name is None:
            bus_stop_name = "Unknown"
        # Print the distance and bus stop name
        arcpy.AddMessage(f"The nearest bus stop is '{bus_stop_name}' at a distance of {near_dist} meters.")
    except Exception as e:
        arcpy.AddError(f"An error occurred: {str(e)}")
        arcpy.AddMessage(f"Error details: {arcpy.GetMessages(2)}")
# Define input parameters
input_fc = arcpy.GetParameterAsText(0)
stops_fc = r"C:\Users\Martin\Documents\WWU\6Semester\Python\exercise10\arcpy_2.gdb\stops_ms_mitte"  # Hardcoded fc you should adjust the file location
# Call function
find_nearest_bus_stop(input_fc, stops_fc)