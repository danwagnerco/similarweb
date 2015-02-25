import re
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
            return self._handle_invalid_api_key(dictionary)

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return self._handle_bad_url()

        # Handle bad inputs
        elif "Message" in keys and "The request is invalid." in values:
            sub_dictionary = dictionary["ModelState"]
            error_message = list(sub_dictionary.values())[0][0]
            return {"Error": error_message}

        # Handle any other weirdness that is returned
        else:
            return {"Error": "Unknown Error"}


    def traffic(self, url):
        traffic_url = ("traffic?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url % {"url": url} + traffic_url
        response = requests.get(self.full_url)

        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Happy path
        if "GlobalRank" in keys:
            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return self._handle_invalid_api_key(dictionary)

        # Handle bad url
        elif "Message" in keys and re.search("found", values[0], re.IGNORECASE):
            return self._handle_bad_url()

        # Handle any other weirdness that is returned
        else:
            return {"Error": "Unknown Error"}


    @staticmethod
    def _handle_invalid_api_key(dictionary):
        sub_dictionary = dictionary["Error"]
        return {"Error": sub_dictionary["Message"]}


    @staticmethod
    def _handle_bad_url():
        return {"Error": "Malformed or Unknown URL"}
