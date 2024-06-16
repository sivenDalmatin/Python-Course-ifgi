#input and output feature classes
input_fc = "active_assets"
buffer_fc = "coverage"
helper_field = "BufferDist"


# Check if 'BufferDist' field exists and delete it if it does
if helper_field in [field.name for field in arcpy.ListFields(output_fc)]:
    arcpy.DeleteField_management(output_fc, helper_field)
    print(f"Field '{helper_field}' deleted.")

# Add a field to store buffer distances
arcpy.AddField_management(output_fc, helper_field, "DOUBLE")

# Calculate the buffer distances
buffer_dist_expression = """
def calc_buffer_dist(type):
    if type == 'mast':
        return 300
    elif type == 'mobile_antenna':
        return 50
    elif type == 'building_antenna':
        return 100
    else:
        return 0
"""

arcpy.CalculateField_management(output_fc, helper_field, "calc_buffer_dist(!type!)", "PYTHON3", buffer_dist_expression)

# Create buffers with calculated distances
arcpy.Buffer_analysis(output_fc, buffer_fc, helper_field)
print("Done")
