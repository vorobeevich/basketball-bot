import pandas as pd 
from PlacesApi import PlacesApi

class DataBuilder:
    def __init(self):
        pass
    
    @staticmethod
    def read_districts(path):
        districts = []
        with open(path, "r", encoding="utf-8") as f:
            districts = f.read().splitlines()
        return districts

    @staticmethod
    def create_dataframe(districts, keys, path):
        data = dict()
        for key in keys:
            data[key] = []

        places_api = PlacesApi()
        
        for district in districts:
            query = "Баскетбольная Площадка рядом с район " + district + ", Москва, " + district + ",  Россия"
            response = places_api.make_text_search_request(query)
            if response.status_code == 200:
                response = response.json()
                for result in response["results"]:
                    result_dict = PlacesApi.dict_from_json(result)
                    for key in result_dict.keys():
                        data[key].append(result_dict[key])
        
        df = pd.DataFrame(data)
        df.to_csv(path, encoding="utf-8")

    @staticmethod
    def get_photos_from_dataframe(path):
        df = pd.read_csv(path)
        places_api = PlacesApi()
        for index, row in df.iterrows():
            if df.loc[index, "photo_id"] != "0":
                response = places_api.make_photo_request(df.loc[index, "photo_id"], str(df.loc[index, "photo_width"]))  
                PlacesApi.save_photo_response(response, "data/photos/" + str(index) + ".png")