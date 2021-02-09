import requests
import json
from dotenv import load_dotenv
import os
import pandas as pd
from geopy.distance import distance
from functools import reduce
import operator
import geopandas as gpd
load_dotenv()

tok1 = os.getenv("tok1")
tok2 = os.getenv("tok2")

def devuelve_data(lat,lng,radius,category_id, nombre_df):
    url = "https://api.foursquare.com/v2/venues/search"

    parametros = {"client_id" : tok1,
                  "client_secret" : tok2,
                  "v" : "20180323",
                  "ll" : f"{lng},{lat}",
                  "radius" : radius,
                  "categoryId" : f"{category_id}",
                  "limit" : 10
                 }
    resp = requests.get (url=url, params = parametros)
    data = json.loads(resp.text)
    decoding_data = data.get("response")

    decoding_data2 = decoding_data.get("venues")
    x=decoding_data2[0].get("location")
    y=decoding_data2[0].get("name")
    
    
    nombre_df=pd.DataFrame({
        "lat": [x.get("lat")],
        "lng": [x.get("lng")],
        "distance": [x.get("distance")],
        "formattedAddress":[x.get("formattedAddress")]
    })
    nombre_df["name"]= [decoding_data2[0].get("name")]
    nombre_df

   

    return nombre_df

def mapa(df):
    return df.applymap(lambda x: x[0] if isinstance(x, list) else x)

def clean_df(df):
    mapa(df)
    df_map=mapa(df)
    df_prueba=pd.DataFrame(df_map.offices.to_dict().items())
    g=mapa(df_prueba)
    g1=g.join(pd.DataFrame(g[1].to_dict()).T)
    g1.drop([0, 1],axis=1)
    df_new = pd.concat([df, g1], axis=1)
    df_clean=df_new.drop(["offices", 0, 1], axis=1)
    dfc=df_clean["city"]=="Los Angeles"
    df_la = df_clean[dfc]
    df_la=df_la.drop(["address2"], axis=1)
    return df_la