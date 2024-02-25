import pandas as pd
from math import radians, cos, sin, asin, sqrt
import numpy as np
import json

#DATA PROCESSING

def read_file(file_path):
    """
    Read a CSV file using pandas.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - DataFrame: A pandas DataFrame containing the data from the CSV file.
    """
    try:
        # Use pandas to read the CSV file
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        # Handle any exceptions that might occur during file reading
        print(f"Error reading CSV file: {e}")
        return None
    
def hospital_processing(data_frame):
    hospital_list = data_frame.drop(data_frame[data_frame.STATUS == "CLOSED"].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.LATITUDE.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.LONGITUDE.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.NAME.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.ADDRESS.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.CITY.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.STATE.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.ZIP.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.TELEPHONE.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.TYPE.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.COUNTY.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.COUNTRY.isna()].index)
    hospital_list = hospital_list.drop(data_frame[data_frame.ID.isna()].index)
    hospital_list = data_frame[["ID","NAME","ADDRESS","CITY","STATE","ZIP","TELEPHONE","TYPE","COUNTY","COUNTRY","LATITUDE","LONGITUDE","OWNER","WEBSITE"]]
    hospital_list = hospital_list.rename(columns={"ID":"HOSPITAL_ID"})
    return hospital_list

def dist(lat1, long1, lat2, long2):

    # convert decimal degrees to radians 
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula 
    dlon = long2 - long1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    # Radius of earth in miles is 3,958.8
    mi = 3958.8* c
    return mi

def nearest_hospitals(lat,long,df,num_of_hospitals):
    nearest_hospitals_df = df
    nearest_hospitals_df["Distance"] = [None]*len(nearest_hospitals_df)
    for i in range(len(nearest_hospitals_df)):
        nearest_hospitals_df.at[i,"Distance"]=dist(lat,long,(nearest_hospitals_df.at[i,"LATITUDE"]),(nearest_hospitals_df.at[i,"LONGITUDE"]))
    
    nearest_hospitals_df = nearest_hospitals_df.sort_values(by=["Distance"])
    nearest_hospitals_df = nearest_hospitals_df[["HOSPITAL_ID","NAME","ADDRESS","CITY","STATE","ZIP","TELEPHONE","TYPE","COUNTY","COUNTRY","LATITUDE","LONGITUDE","OWNER","WEBSITE"]]
    
    
    return nearest_hospitals_df.head(num_of_hospitals)
    
#GETTER METHODS
def get_hospital_id(df,hospital_name):
    hospital_name = hospital_name.upper()
    hospital_id = df.loc[df["NAME"]==hospital_name,"HOSPITAL_ID"].iloc[0]
    return hospital_id

def get_lat(df,hospital_id):
    lat = df.loc[df["HOSPITAL_ID"]==hospital_id,"LATITUDE"].iloc[0]
    return lat

def get_long(df,hospital_id):
    long = df.loc[df["HOSPITAL_ID"]==hospital_id,"LONGITUDE"].iloc[0]
    return long

def get_hospital_name(df,hospital_id):
    name = df.loc[df["HOSPITAL_ID"]==hospital_id,"NAME"].iloc[0]
    return name

def get_address(df,hospital_id):
    add = df.loc[df["HOSPITAL_ID"]==hospital_id,"ADDRESS"].iloc[0]
    return add

def get_city(df,hospital_id):
    city = df.loc[df["HOSPITAL_ID"]==hospital_id,"CITY"].iloc[0]
    return city

def get_state(df,hospital_id):
    state = df.loc[df["HOSPITAL_ID"]==hospital_id,"STATE"].iloc[0]
    return state

def get_zip(df,hospital_id):
    zip = df.loc[df["HOSPITAL_ID"]==hospital_id,"ZIP"].iloc[0]
    return zip

def get_telephone(df,hospital_id):
    phone = df.loc[df["HOSPITAL_ID"]==hospital_id,"TELEPHONE"].iloc[0]
    return phone

def get_county(df,hospital_id):
    county = df.loc[df["HOSPITAL_ID"]==hospital_id,"COUNTY"].iloc[0]
    return county

def get_country(df,hospital_id):
    country = df.loc[df["HOSPITAL_ID"]==hospital_id,"COUNTRY"].iloc[0]
    return country

def get_owner(df,hospital_id):
    owner = df.loc[df["HOSPITAL_ID"]==hospital_id,"OWNER"].iloc[0]
    return owner

def get_website(df,hospital_id):
    website = df.loc[df["HOSPITAL_ID"]==hospital_id,"WEBSITE"].iloc[0]
    return website

def get_complete_address(df,hospital_id):
    complete_address = f"{get_hospital_name(df,hospital_id)}, {get_address(df,hospital_id)}, {get_county(df,hospital_id)}, {get_city(df,hospital_id)}, {get_state(df,hospital_id)} - {get_zip(df,hospital_id)}"
    return complete_address

def get_coordinates(df):
    coordinates_df = df[["HOSPITAL_ID","NAME","LATITUDE","LONGITUDE"]]
    coordinates_dict = dict()
    for i in range(len(coordinates_df)):
        coordinates_dict[coordinates_df.loc[i].iloc[0]] = {coordinates_df.loc[i].iloc[1],coordinates_df.loc[i].iloc[2],coordinates_df.loc[i].iloc[3]}
    return coordinates_dict,

def json_write(dict,filepath):
    json_object = json.dumps(dict)
    with open(filepath,"w") as f:
        f.write(json_object)



#TESTERS
def nearest_hospital_tester(filepath):
    df = read_file(filepath)
    df_processed = hospital_processing(df)
    lat = 43.07204885507844
    long = -89.40653223250834
    top_n = nearest_hospitals(lat,long, df_processed,10)
    print(top_n[["NAME","LATITUDE","LONGITUDE"]])

def getter_testers(filepath):
    df = read_file(filepath)
    df_processed = hospital_processing(df)
    hospital_id = get_hospital_id(df_processed,"Meriter Hsptl")
    print(hospital_id)
    print(get_complete_address(df_processed,hospital_id))
    get_lat(df_processed,hospital_id)
    get_long(df_processed,hospital_id)
    get_telephone(df_processed,hospital_id)
    get_website(df_processed,hospital_id)


    
    

#RUNNING TESTERS
    
nearest_hospital_tester("Datasets/Hospitals.csv")
#getter_testers("Datasets/Hospitals.csv")

#RUNNING JSON
df = read_file("Datasets/Hospitals.csv")
df_processed = hospital_processing(df)

json_write(get_coordinates(df_processed),"Datasets/hospital_backend.json")
