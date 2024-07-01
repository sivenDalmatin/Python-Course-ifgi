import arcpy

class ToolValidator:
    def __init__(self): 
        self.params = arcpy.GetParameterInfo()
        try:
            arcpy.Delete_management('in_memory\\freq_table')
        except:
            pass

    def initializeParameters(self):
        return

    def updateParameters(self):

        if self.params[1].altered and self.params[0].altered:

            fields = arcpy.Describe(self.params[1]).fields
            field_names = [x.name for x in fields]
            # set the field names as filter for parameter [1]
            self.params[2].filter.list = field_names
    
        if self.params[1].altered and self.params[0].altered and self.params[2].altered:
            # get a table of the unique values for the name field
            arcpy.analysis.Frequency(in_table=self.params[1].value,out_table='in_memory\\freq_table',frequency_fields=self.params[2].value)
            name_values = [row[0] for row in arcpy.da.SearchCursor(in_table='in_memory\\freq_table', field_names=[self.params[2].value])]
            #delete the table in memory
            arcpy.Delete_management('in_memory\\freq_table')
            #set the parameter filter list
            self.params[3].filter.list = name_values
    
    def updateMessages(self):
        return