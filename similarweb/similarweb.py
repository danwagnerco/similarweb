import re
import json
import requests
import similarweb.helpers as helpers

class TrafficClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "http://api.similarweb.com/Site/{0}/v1/"
        self.full_url = ""


    def traffic(self, url):
        traffic_url = ("traffic?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + traffic_url
        response = requests.get(self.full_url)

        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Happy path
        if "GlobalRank" in keys:
            top_country_shares = dictionary["TopCountryShares"]
            codes = [str(d["CountryCode"]) for d in top_country_shares]
            shares = [d["TrafficShare"] for d in top_country_shares]
            top_country_shares_dictionary = dict(zip(codes, shares))
            del dictionary["TopCountryShares"]
            dictionary["TopCountryShares"] = top_country_shares_dictionary

            traffic_reach = dictionary["TrafficReach"]
            dates = [d["Date"] for d in traffic_reach]
            values = [d["Value"] for d in traffic_reach]
            traffic_reach_dictionary = dict(zip(dates, values))
            del dictionary["TrafficReach"]
            dictionary["TrafficReach"] = traffic_reach_dictionary

            traffic_shares = dictionary["TrafficShares"]
            sources = [d["SourceType"] for d in traffic_shares]
            source_values = [d["SourceValue"] for d in traffic_shares]
            traffic_shares_dictionary = dict(zip(sources, source_values))
            del dictionary["TrafficShares"]
            dictionary["TrafficShares"] = traffic_shares_dictionary

            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and re.search("found", values[0], re.IGNORECASE):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


    def visits(self, url, gr, start, end, md = False):
        visits_url = ("visits?gr={0}&start={1}&end={2}"
                      "&md={3}&UserKey={4}"
                     ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url.format(url) + visits_url
        return self._results_from_web_traffic_apis(self.full_url)


    def page_views(self, url, gr, start, end, md = False):
        page_views_url = ("pageviews?gr={0}&start={1}&end={2}"
                         "&md={3}&UserKey={4}"
                        ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url.format(url) + page_views_url
        return self._results_from_web_traffic_apis(self.full_url)


    def visit_duration(self, url, gr, start, end, md = False):
        visit_duration_url = ("visitduration?gr={0}&start={1}&end={2}"
                              "&md={3}&UserKey={4}"
                             ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url.format(url) + visit_duration_url
        return self._results_from_web_traffic_apis(self.full_url)


    def bounce_rate(self, url, gr, start, end, md = False):
        bounce_rate_url = ("bouncerate?gr={0}&start={1}&end={2}"
                           "&md={3}&UserKey={4}"
                          ).format(gr, start, end, md, self.user_key)
        self.full_url = self.base_url.format(url) + bounce_rate_url
        return self._results_from_web_traffic_apis(self.full_url)


    def _results_from_web_traffic_apis(self, url):
        response = requests.get(url)
        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Handle good response (happy path)
        if "Values" in keys:
            sub = dictionary["Values"]
            dates = [x["Date"] for x in sub]
            values = [x["Value"] for x in sub]
            return dict(zip(dates, values))

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return helpers.BAD_URL

        # Handle out-of-order dates
        elif "Message" in keys and "Date range is not valid" in values:
            return helpers.BAD_DATE_ORDER

        # Handle bad inputs
        elif "Message" in keys and "The request is invalid." in values:
            return helpers.bad_inputs_to_traffic_or_sources_api(dictionary)

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


class ContentClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "http://api.similarweb.com/Site/{0}/v2/"
        self.full_url = ""


    def similar_sites(self, url):
        similar_sites_url = ("similarsites?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + similar_sites_url
        return self._results_from_non_category_content_apis(self.full_url,
                                                            "SimilarSites",
                                                            "Url",
                                                            "Score")


    def also_visited(self, url):
        also_visited_url = ("alsovisited?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + also_visited_url
        return self._results_from_non_category_content_apis(self.full_url,
                                                            "AlsoVisited",
                                                            "Url",
                                                            "Score")


    def tags(self, url):
        tags_url = ("tags?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + tags_url
        return self._results_from_non_category_content_apis(self.full_url,
                                                            "Tags",
                                                            "Name",
                                                            "Score")


    def _results_from_non_category_content_apis(self,
                                                url,
                                                happy_key,
                                                item_key,
                                                item_value):
        response = requests.get(url)

        # Look out, the nastiest urls do not return JSON
        try:
            dictionary = json.loads(response.text)
            keys = list(dictionary.keys())
            values = list(dictionary.values())
        except ValueError:
            return helpers.BAD_URL

        # Handle good response (happy path)
        if str(happy_key) in keys:
            sub_list = dictionary[str(happy_key)]
            sub_keys = [x[item_key] for x in sub_list]
            sub_values = [x[item_value] for x in sub_list]
            return dict(zip(sub_keys, sub_values))


        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


    def category(self, url):
        category_url = ("category?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + category_url
        return self._results_from_category_content_apis(self.full_url)


    def category_rank(self, url):
        category_rank_url = ("categoryrank?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + category_rank_url
        response = requests.get(self.full_url)
        return self._results_from_category_content_apis(self.full_url)


    def _results_from_category_content_apis(self, url):
        response = requests.get(url)

        # Look out, the nastiest urls do not return JSON
        try:
            dictionary = json.loads(response.text)
            keys = list(dictionary.keys())
            values = list(dictionary.values())
        except ValueError:
            return helpers.BAD_URL

        # Handle good response (happy path)
        if "Category" in keys:
            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


class SourcesClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "http://api.similarweb.com/Site/{0}/{1}/"
        self.full_url = ""


    def organic_search_keywords(self, url, page, start, end, md = False):
        organic_search_keywords_url = ("orgsearch?start={0}&end={1}"
                                       "&md={2}&page={3}&UserKey={4}"
                                      ).format(start, end, md, str(page), self.user_key)
        self.full_url = self.base_url.format(url, "v1") + organic_search_keywords_url
        return self._results_from_search_keywords_apis(self.full_url)


    def organic_keyword_competitors(self, url, page, start, end, md = False):
        organic_keyword_competitors_url = ("orgkwcompetitor?start={0}&end={1}"
                                           "&md={2}&page={3}&UserKey={4}"
                                          ).format(start, end, md, str(page), self.user_key)
        self.full_url = self.base_url.format(url, "v1") + organic_keyword_competitors_url
        return self._results_from_search_keywords_apis(self.full_url)


    def paid_keyword_competitors(self, url, page, start, end, md = False):
        paid_keyword_competitors_url = ("paidkwcompetitor?start={0}&end={1}"
                                        "&md={2}&page={3}&UserKey={4}"
                                       ).format(start, end, md, str(page), self.user_key)
        self.full_url = self.base_url.format(url, "v1") + paid_keyword_competitors_url
        return self._results_from_search_keywords_apis(self.full_url)


    def paid_search_keywords(self, url, page, start, end, md = False):
        paid_search_keywords_url = ("paidsearch?start={0}&end={1}"
                                    "&md={2}&page={3}&UserKey={4}"
                                   ).format(start, end, md, str(page), self.user_key)
        self.full_url = self.base_url.format(url, "v1") + paid_search_keywords_url
        return self._results_from_search_keywords_apis(self.full_url)


    def referrals(self, url, page, start, end):
        referrals_url = ("referrals?start={0}&end={1}"
                         "&page={2}&UserKey={3}"
                        ).format(start, end, str(page), self.user_key)
        self.full_url = self.base_url.format(url, "v1") + referrals_url
        return self._results_from_search_keywords_apis(self.full_url)


    def _results_from_search_keywords_apis(self, url):
        response = requests.get(url)
        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Happy path
        if "Data" in keys:
            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and "Data Not Found" in values:
            return helpers.BAD_URL

        # Handle out-of-order dates
        elif "Message" in keys and "Date range is not valid" in values:
            return helpers.BAD_DATE_ORDER

        # Handle bad inputs
        elif "Message" in keys and "The request is invalid." in values:
            return helpers.bad_inputs_to_traffic_or_sources_api(dictionary)

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


    def social_referrals(self, url):
        social_referrals_url = ("SocialReferringSites?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url, "v1") + social_referrals_url
        response = requests.get(self.full_url)

        dictionary = json.loads(response.text)
        keys = list(dictionary.keys())
        values = list(dictionary.values())

        # Happy path
        if "SocialSources" in keys:
            social_sources_list = dictionary["SocialSources"]
            sites = [d["Source"] for d in social_sources_list]
            scores = [d["Value"] for d in social_sources_list]
            social_sources_dictionary = dict(zip(sites, scores))
            del dictionary["SocialSources"]
            dictionary["SocialSources"] = social_sources_dictionary
            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and re.search("found", values[0], re.IGNORECASE):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


    def destinations(self, url):
        destinations_url = ("leadingdestinationsites?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url, "v2") + destinations_url
        response = requests.get(self.full_url)

        # Look out, the nastiest urls do not return JSON
        try:
            dictionary = json.loads(response.text)
            keys = list(dictionary.keys())
            values = list(dictionary.values())
        except ValueError:
            return helpers.BAD_URL

        # Happy path
        if "Sites" in keys:
            return dictionary

        # Handle invalid API key
        elif "Error" in keys:
            return helpers.BAD_API_KEY

        # Handle bad url
        elif "Message" in keys and re.search("found", values[0], re.IGNORECASE):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR

