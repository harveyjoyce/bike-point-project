{{ codegen.generate_source(schema_name= 'CO_DES5_BIKE_POINT'
    , database_name= 'TIL_DATA_ENGINEERING'
    , table_names= ['bike_point_raw']
    , generate_columns = True
    , include_descriptions =True )}}