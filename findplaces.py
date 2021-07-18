from distances import simple_time, clever_time
import pandas as pd

def find_places(limit, path, lat, lng):
    df = pd.read_csv(path)
    places = []
    for index, row in df.iterrows():
        if simple_time(lat, lng, df.loc[index, "latitude"], df.loc[index, "longitude"], 10) <= limit:
            if clever_time(lat, lng, df.loc[index, "latitude"], df.loc[index, "longitude"]) <= limit:
                places.append((index, row))
    return places

