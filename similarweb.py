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
        return self._parse_response_from_visits_or_pageviews(response)


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
            return self._handle_bad_api_key(dictionary)

        # Handle bad url
        elif "Message" in keys and re.search("found", values[0], re.IGNORECASE):
            return self._handle_bad_url()

        # Handle any other weirdness that is returned
        else:
            return self._handle_all_other_errors()


    def pageviews(self, url, gr, start, end, md=False):
        visits_url = ("pageviews?gr={0}&start={1}&end={2}"
                      "&md={3}&UserKey={4}"
                      ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url % {"url": url} + visits_url
        response = requests.get(self.full_url)
        return self._parse_response_from_visits_or_pageviews(response)


    def _parse_response_from_visits_or_pageviews(self, response):
        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Handle good response (happy path)
        if "Values" in keys:
            return self._handle_good_response(dictionary)

        # Handle invalid API key
        elif "Error" in keys:
            return self._handle_bad_api_key(dictionary)

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return self._handle_bad_url()

        # Handle out-of-order dates
        elif "Message" in keys and "Date range is not valid" in values:
            return self._handle_out_of_order_dates()

        # Handle bad inputs
        elif "Message" in keys and "The request is invalid." in values:
            return self._handle_bad_inputs(dictionary)

        # Handle any other weirdness that is returned
        else:
            return self._handle_all_other_errors()


    @staticmethod
    def _handle_good_response(dictionary):
        sub_dictionary = dictionary["Values"]
        dates = [x["Date"] for x in sub_dictionary]
        values = [x["Value"] for x in sub_dictionary]
        return dict(zip(dates, values))


    @staticmethod
    def _handle_bad_api_key(dictionary):
        sub_dictionary = dictionary["Error"]
        return {"Error": sub_dictionary["Message"]}


    @staticmethod
    def _handle_bad_url():
        return {"Error": "Malformed or Unknown URL"}


    @staticmethod
    def _handle_out_of_order_dates():
        return {"Error": "Date range is not valid"}


    @staticmethod
    def _handle_bad_inputs(dictionary):
        sub_dictionary = dictionary["ModelState"]
        error_message = list(sub_dictionary.values())[0][0]
        return {"Error": error_message}


    @staticmethod
    def _handle_all_other_errors():
        return {"Error": "Unknown Error"}
