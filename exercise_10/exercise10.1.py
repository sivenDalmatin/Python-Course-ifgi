import arcpy

def find_nearest_bus_stop(input_fc, stops_fc):
    try:
        # input feature class is in Web Mercator
        input_spatial_ref = arcpy.Describe(input_fc).spatialReference
        web_mercator = arcpy.SpatialReference(3857)
        
        if input_spatial_ref.name != web_mercator.name:
            arcpy.AddMessage("Projecting input feature class to Web Mercator projection.")
            projected_input_fc = "in_memory/projected_input"
            arcpy.management.Project(input_fc, projected_input_fc, web_mercator)
            input_fc = projected_input_fc

        # stops feature class is in Web Mercator
        stops_spatial_ref = arcpy.Describe(stops_fc).spatialReference
        if stops_spatial_ref.name != web_mercator.name:
            arcpy.AddMessage("Projecting stops feature class to Web Mercator projection.")
            projected_stops_fc = "in_memory/projected_stops"
            arcpy.management.Project(stops_fc, projected_stops_fc, web_mercator)
            stops_fc = projected_stops_fc

        # Run Near tool 
        arcpy.analysis.Near(input_fc, stops_fc)

        # get the NEAR_FID and NEAR_DIST via the input feature class
        near_fid = None
        near_dist = None
        with arcpy.da.SearchCursor(input_fc, ["NEAR_FID", "NEAR_DIST"]) as cursor:
            for row in cursor:
                near_fid = row[0]
                near_dist = row[1]

        # no nearby values
        if near_fid is None:
            arcpy.AddMessage("No nearby bus stop found.")
            return

        # get name of the nearest bus stop
        bus_stop_name = None
        where_clause = f"OBJECTID = {near_fid}"
        with arcpy.da.SearchCursor(stops_fc, ["Name"], where_clause) as cursor:
            for row in cursor:
                bus_stop_name = row[0]

        # If the bus stop name is None, handle it gracefully
        if bus_stop_name is None:
            bus_stop_name = "Unknown"

        # Print the distance and bus stop name
        arcpy.AddMessage(f"The nearest bus stop is '{bus_stop_name}' at a distance of {near_dist} meters.")

    except Exception as e:
        arcpy.AddError(f"An error occurred: {str(e)}")
        arcpy.AddMessage(f"Error details: {arcpy.GetMessages(2)}")

# Define input parameters
input_fc = arcpy.GetParameterAsText(0) 
stops_fc = r"C:\Users\finng\Downloads\arcpy_2\arcpy_2.gdb\stops_ms_mitte"  # Hardcoded feature class with bus stops

# Call the function with the input parameters
find_nearest_bus_stop(input_fc, stops_fc)
