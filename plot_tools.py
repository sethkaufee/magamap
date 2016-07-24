import vincent
import json
import pandas as pd
import requests

def mergeToMap(df, df_key_col, map_type):
    (map_key, map_path) = getMapParams(map_type)
    with open(map_path, 'r') as f:
        get_id = json.load(f)
    feature_name = get_id['objects'].keys()[0]
    #A little FIPS code type casting to ensure keys match
    new_geoms = []
    district_codes =  [x['properties'][map_key] for x in get_id['objects'][feature_name]['geometries']]
    districts_df = pd.DataFrame({'code': district_codes}, dtype=str)

    #Perform an inner join, pad NA's with data from nearest county
    df_merged = pd.merge(df, districts_df, left_on=df_key_col, right_on='code', how='inner')
    df_merged = df_merged.fillna(method='pad')
    
    return (df_merged, feature_name)

# Helper function that gets the name of the data structure within a file
def getFeatureName(map_path):
    with open(map_path, 'r') as f:
        get_id = json.load(f)
    return get_id['objects'].keys()[0]


def getMapParams(map_type):
    if map_type == 'county':
        return ('GEOID', '')
    elif map_type == 'congress':
        return ('GEOID', 'geography/congress/json/tl_2015_us_cd114.topojson')
    elif map_type == 'state':
        return('GEOID', '')


def plotMap(df, df_key_col, df_data_col, map_type):
    (df_merged, feature_name) = mergeToMap(df, df_key_col, map_type)
    (map_key, map_path) = getMapParams(map_type)
    map_key_str = 'properties.'+map_key
    # Set up map
    geo_data = [{'name': 'districts',
                 'url': map_path,
                 'feature': feature_name}]

    vis = vincent.Map(data=df, geo_data=geo_data, scale=1100,
                      projection='albersUsa', data_bind=df_data_col,
                      data_key=df_key_col, map_key={'districts': map_key_str}, brew='YlOrBr') # BuGn, YlGnBu, YlOrBr 
    # 'brew' color schemes: http://colorbrewer2.org/
    vis.marks[0].properties.enter.stroke_opacity = vincent.ValueRef(value=0.5)
    #Change our domain for an even inteager
    vis.scales['color'].domain = [0, 20]
    vis.legend(title='%% Unemployment')
    #vis.to_json('vega.json')
    return vis
