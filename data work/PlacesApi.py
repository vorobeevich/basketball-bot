import requests

class PlacesApi:
    def __init__(self):
        with open("key.txt") as f:
            self.key = f.read()

    def make_text_search_request(self, query):
        url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
        parameters = "query=" + query + "&language=ru" + "&key=" + self.key
        final_url = url + parameters
        response = requests.get(final_url)
        return response

    def make_photo_request(self, photoreference, maxwidth):
        url = "https://maps.googleapis.com/maps/api/place/photo?"
        parameters = "photoreference=" + photoreference + "&maxwidth=" + maxwidth + "&key=" + self.key
        final_url = url + parameters
        response = requests.get(final_url)
        return response

    @staticmethod
    def save_photo_response(response, path):
        if response.status_code == 200:
            with open(path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)

    def dict_from_json(response):
        result = dict()
        result["name"] = response["name"]
        result["latitude"] = response["geometry"]["location"]["lat"]
        result["longitude"] = response["geometry"]["location"]["lng"]
        result["adress"] = response["formatted_address"]
        if "photos" in response and len(response["photos"]) == 1:
            result["photo_id"] = response["photos"][0]["photo_reference"]
            result["photo_width"] = response["photos"][0]["width"]
        else:
            result["photo_id"] = None 
            result["photo_width"] = None
        return result
    