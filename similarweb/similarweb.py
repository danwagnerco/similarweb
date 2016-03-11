from . import helpers


class TrafficClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "https://api.similarweb.com/Site/{0}/v1/"
        self.full_url = ""

    def traffic(self, url):
        traffic_url = ("traffic?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url) + traffic_url
        response = helpers.get_http_response(self.full_url)

        # Happy path
        if "GlobalRank" in response.keys():
            top_country_shares = helpers.dictify(response["TopCountryShares"],
                                                          "CountryCode",
                                                          "TrafficShare",
                                                          stringify_keys = True)
            traffic_reach = helpers.dictify(response["TrafficReach"],
                                                     "Date",
                                                     "Value")
            traffic_shares = helpers.dictify(response["TrafficShares"],
                                                      "SourceType",
                                                      "SourceValue")

            del response["TopCountryShares"]
            response["TopCountryShares"] = top_country_shares
            del response["TrafficReach"]
            response["TrafficReach"] = traffic_reach
            del response["TrafficShares"]
            response["TrafficShares"] = traffic_shares

            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "found" in [x for x in response.values()][0].lower().split()):
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
        response = helpers.get_http_response(self.full_url)

        # Handle good response (happy path)
        if "Values" in response.keys():
            return helpers.dictify(response["Values"], "Date", "Value")

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "Data Not Found" in response.values()):
            return helpers.BAD_URL

        # Handle out-of-order dates
        elif ("Message" in response.keys() and
              "Date range is not valid" in response.values()):
            return helpers.BAD_DATE_ORDER

        # Handle bad inputs
        elif ("Message" in response.keys() and
              "The request is invalid." in response.values()):
            return helpers.bad_inputs_to_traffic_or_sources_api(response)

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


class ContentClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "https://api.similarweb.com/Site/{0}/v2/"
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
        response = helpers.get_http_response(url)

        # Handle good response (happy path)
        if str(happy_key) in response.keys():
            return helpers.dictify(response[happy_key], item_key, item_value)

        # The API response was not JSON and get_http_response caught ValueError
        elif response == helpers.BAD_URL:
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "Data Not Found" in response.values()):
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
        return self._results_from_category_content_apis(self.full_url)

    def _results_from_category_content_apis(self, url):
        response = helpers.get_http_response(url)

        # Handle good response (happy path)
        if "Category" in response.keys():
            return response

        # The API response was not JSON and get_http_response caught ValueError
        elif response == helpers.BAD_URL:
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "Data Not Found" in response.values()):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


class SourcesClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "https://api.similarweb.com/Site/{0}/{1}/"
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
        response = helpers.get_http_response(url)

        # Happy path
        if "Data" in response.keys():
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "Data Not Found" in response.values()):
            return helpers.BAD_URL

        # Handle out-of-order dates
        elif ("Message" in response.keys() and
              "Date range is not valid" in response.values()):
            return helpers.BAD_DATE_ORDER

        # Handle bad inputs
        elif ("Message" in response.keys() and
              "The request is invalid." in response.values()):
            return helpers.bad_inputs_to_traffic_or_sources_api(response)

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR

    def social_referrals(self, url):
        social_referrals_url = ("SocialReferringSites?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url, "v1") + social_referrals_url
        response = helpers.get_http_response(self.full_url)

        # Happy path
        if "SocialSources" in response.keys():
            social_sources = helpers.dictify(response["SocialSources"],
                                             "Source",
                                             "Value")
            del response["SocialSources"]
            response["SocialSources"] = social_sources
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "found" in [x for x in response.values()][0].lower().split()):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR

    def destinations(self, url):
        destinations_url = ("leadingdestinationsites?UserKey={0}").format(self.user_key)
        self.full_url = self.base_url.format(url, "v2") + destinations_url
        response = helpers.get_http_response(self.full_url)

        # Happy path
        if "Sites" in response.keys():
            return response

        # The API response was not JSON and get_http_response caught ValueError
        elif response == helpers.BAD_URL:
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle bad url
        elif ("Message" in response.keys() and
              "found" in [x for x in response.values()][0].lower().split()):
            return helpers.BAD_URL

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR


class MobileClient(object):
    def __init__(self, user_key):
        self.user_key = user_key
        self.base_url = "https://api.similarweb.com/Mobile/{0}/{1}/"
        self.full_url = ""

    def app_details(self, app_id, app_store):
        if helpers.input_to_app_store_is_bad(str(app_store)):
            return helpers.BAD_APP_STORE

        app_store_num = helpers.app_store_id_to_number(app_store)
        temp_url = self.base_url.format(app_store_num, str(app_id))
        self.full_url = "{0}v1/GetAppDetails?UserKey={1}".format(temp_url,
                                                                  self.user_key)

        response = helpers.get_http_response(self.full_url)

        # Happy path (including no stats)
        if "Title" in response.keys():
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR

    def google_app_installs(self, app_id):
        temp_url = self.base_url.format(0, str(app_id))
        self.full_url = "{0}v1/GetAppInstalls?UserKey={1}".format(temp_url,
                                                                  self.user_key)

        response = helpers.get_http_response(self.full_url)

        # Happy path (including no stats)
        if "InstallsMin" in response.keys():
            return response

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle any other weirdness that is returned
        else:
            return helpers.BAD_UNKNOWN_ERROR

    def site_related_apps(self, app_id, app_store):
        if helpers.input_to_app_store_is_bad(str(app_store)):
            return helpers.BAD_APP_STORE

        app_store_num = helpers.app_store_id_to_number(app_store)
        temp_url = self.base_url.format(app_store_num, str(app_id))
        self.full_url = "{0}v1/GetRelatedSiteApps?UserKey={1}".format(temp_url,
                                                                  self.user_key)

        response = helpers.get_http_response(self.full_url)

        # Happy path
        if "RelatedApps" in response.keys():
            return helpers.dictify(response["RelatedApps"], "AppId", "Title")

        # Handle invalid API key
        elif "Error" in response.keys():
            return helpers.BAD_API_KEY

        # Handle malformed URL
        elif "Message" in response.keys():
            return helpers.BAD_URL

        # Handle any other weirdness
        else:
            return helpers.BAD_UNKNOWN_ERROR

