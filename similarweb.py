import json
import requests

class SimilarwebTrafficClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "http://api.similarweb.com/Site/%(url)s/v1/"
        self.full_url = ""


    def visits(self, url, gr, start, end, md=False):
        visits_url = ("visits?gr={0}&start={1}&end={2}"
                      "&md={3}&UserKey={4}"
                      ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url % {"url": url} + visits_url
        response = requests.get(self.full_url)

        # This is the old _parse_visits_response method
        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Happy path
        if "Values" in keys:
            sub_dictionary = dictionary["Values"]
            dates = [x["Date"] for x in sub_dictionary]
            values = [x["Value"] for x in sub_dictionary]
            return dict(zip(dates, values))

        # Handle invalid API key
        elif "Error" in keys:
            sub_dictionary = dictionary["Error"]
            return {"Error": sub_dictionary["Message"]}

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return {"Error": "Malformed or Unknown URL"}

        # Handle bad inputs
        elif "Message" in keys and "The request is invalid." in values:
            sub_dictionary = dictionary["ModelState"]
            error_message = list(sub_dictionary.values())[0][0]
            return {"Error": error_message}

        # Handle any other weirdness that is returned
        else:
            return {"Error": "Unknown Error"}
