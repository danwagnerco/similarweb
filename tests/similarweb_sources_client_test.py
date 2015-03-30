import json
import httpretty
from similarweb.similarweb import SourcesClient


def test_sources_client_has_user_key():
    client = SourcesClient("test_key")

    assert client.user_key == "test_key"


def test_sources_client_has_base_url():
    client = SourcesClient("test_key")

    assert client.base_url == "http://api.similarweb.com/Site/%(url)s/%(version)s/"


def test_sources_client_has_empty_full_url():
    client = SourcesClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_sources_client_social_referrals_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/SocialReferringSites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_social_referrals_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.social_referrals("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_social_referrals_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/SocialReferringSites?"
                  "UserKey=invalid_key")
    f = "fixtures/sources_client_social_referrals_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.social_referrals("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_social_referrals_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/SocialReferringSites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_social_referrals_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.social_referrals("bad_url")

        assert result == expected


@httpretty.activate
def test_sources_client_social_referrals_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/SocialReferringSites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_social_referrals_url_with_http_response.json"
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.social_referrals("http://example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_social_referrals_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/SocialReferringSites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_social_referrals_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.social_referrals("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_social_referrals_response_from_good_inputs():
    expected = {"SocialSources": {
                  "Facebook": 0.5872484011274256,
                  "Reddit": 0.1955231030114612,
                  "Twitter": 0.13209235484709875,
                  "Youtube": 0.06292737412742913,
                  "Weibo.com": 0.010782551614770926},
                "StartDate": "12/2014",
                "EndDate": "02/2015"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/SocialReferringSites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_social_referrals_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.social_referrals("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=invalid_key")
    f = "fixtures/sources_client_organic_search_keywords_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("bad_url", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("http://example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_bad_page():
    expected = {"Error": "The field Page is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=0&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_page_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 0, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=14-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=0-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=12-2014&"
                  "end=9-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=12-2014&"
                  "end=9-2014&md=other&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_good_inputs():
    expected = {"Data": [{"SearchTerm": "nba",
                          "Visits": 0.3112634279302496,
                          "Change": -0.1057165328807857},
                         {"SearchTerm": "nba league pass",
                          "Visits": 0.04344402567022226,
                          "Change": -0.28494011618310383},
                         {"SearchTerm": "nba standings",
                          "Visits": 0.026975361122759705,
                          "Change": 0.506606019589038},
                         {"SearchTerm": "nba.com",
                          "Visits": 0.024175302297685337,
                          "Change": -0.21470821673506887},
                         {"SearchTerm": "lakers",
                          "Visits": 0.020901069293644634,
                          "Change": -0.015496674800445101},
                         {"SearchTerm": "nba store",
                          "Visits": 0.009603534757614565,
                          "Change": 0.1954208822589453},
                         {"SearchTerm": "chicago bulls",
                          "Visits": 0.0093402142272212,
                          "Change": 0.09747235068892213},
                         {"SearchTerm": "raptors",
                          "Visits": 0.008992397410119684,
                          "Change": -0.32299852511496613},
                         {"SearchTerm": "cleveland cavaliers",
                          "Visits": 0.007440700569164507,
                          "Change": -0.13185965639266445},
                         {"SearchTerm": "nba game time",
                          "Visits": 0.007300049344512848,
                          "Change": -0.14326631607193804}],
                "ResultsCount": 10,
                "TotalCount": 11975,
                "Next": "http://api.similarweb.com/Site/example.com/v1/orgsearch?start=11-2014&end=12-2014&md=false&UserKey=test_key&page=2"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=invalid_key")
    f = "fixtures/sources_client_paid_search_keywords_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("bad_url", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("http://example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_bad_page():
    expected = {"Error": "The field Page is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=0&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_page_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 0, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=14-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=0-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=12-2014&"
                  "end=9-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=12-2014&"
                  "end=9-2014&md=other&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_good_inputs():
    expected = {"Data": [{"SearchTerm": "nba",
                          "Visits": 0.003344231214687972,
                          "Change": -0.062129215957638526},
                         {"SearchTerm": "nba store",
                          "Visits": 0.0029060240173658432,
                          "Change": 0.20846193245606223},
                         {"SearchTerm": "nba league pass",
                          "Visits": 0.0012716036162238515,
                          "Change": -0.7999901486315264},
                         {"SearchTerm": "nbastore",
                          "Visits": 0.0005023612587764184,
                          "Change": 0.9680003994439492},
                         {"SearchTerm": "portland trail blazers",
                          "Visits": 0.0005004670752349531,
                          "Change": 0.3499677164230108},
                         {"SearchTerm": "nba shop",
                          "Visits": 0.00045529952818624186,
                          "Change": 0.7850990143291091},
                         {"SearchTerm": "nba.com",
                          "Visits": 0.0003494276280350276,
                          "Change": -0.3860372438596248},
                         {"SearchTerm": "league pass",
                          "Visits": 0.00020733505676232166,
                          "Change": -0.8220804130834665},
                         {"SearchTerm": "nba ugly sweaters",
                          "Visits": 0.00019551746013417756,
                          "Change": 0.10131215601631173},
                         {"SearchTerm": "celtics schedule",
                          "Visits": 0.0001742655622935061,
                          "Change": 0.10131215601631166}],
                "ResultsCount": 10,
                "TotalCount": 243,
                "Next": "http://api.similarweb.com/Site/example.com/v1/paidsearch?start=11-2014&end=12-2014&md=false&UserKey=test_key&page=2"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_destinations_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_destinations_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.destinations("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_destinations_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/leadingdestinationsites?"
                  "UserKey=invalid_key")
    f = "fixtures/sources_client_destinations_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.destinations("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_destinations_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_destinations_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.destinations("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_sources_client_destinations_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_destinations_url_with_http_response.json"
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.destinations("http://example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_destinations_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_destinations_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.destinations("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_destinations_response_from_good_inputs():
    expected = {"Sites": ["ticketmaster.com",
                          "jmpdirect01.com",
                          "youradexchange.com",
                          "facebook.com",
                          "youtube.com",
                          "adcash.com",
                          "i.cdn.turner.com",
                          "oss.ticketmaster.com",
                          "mavs.com",
                          "spox.com"],
                "StartDate": "12/2014",
                "EndDate": "02/2015"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "fixtures/sources_client_destinations_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.destinations("example.com")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.referrals("example.com", 1, "11-2014", "12-2014")

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_referrals_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=invalid_key")
    f = "fixtures/sources_client_referrals_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.referrals("example.com", 1, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("bad_url", 1, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("http://example.com", 1, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_bad_page():
    expected = {"Error": "The field Page is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=0&UserKey=test_key")
    f = "fixtures/sources_client_referrals_page_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 0, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=14-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "14-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=0-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "11-2014", "0-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=12-2014&"
                  "end=9-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "12-2014", "9-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_referrals_response_from_good_inputs():
    expected = {"Data": [
                 {"Site": "bleacherreport.com",
                  "Visits": 0.13685091444901207,
                  "Change": -0.13783225525013185},
                 {"Site": "spox.com",
                  "Visits": 0.05541198081414703,
                  "Change": 0.09829387565169896},
                 {"Site": "sportal.com.au",
                  "Visits": 0.047765555793472955,
                  "Change": -0.10571922332026579},
                 {"Site": "espn.go.com",
                  "Visits": 0.034809331570584835,
                  "Change": 0.19681275612219412},
                 {"Site": "ajansspor.com",
                  "Visits": 0.033445473460156236,
                  "Change": 0.045225921939734626},
                 {"Site": "baloncesto.as.com",
                  "Visits": 0.0329538056630076,
                  "Change": 0.23717753959296534},
                 {"Site": "gazzetta.it",
                  "Visits": 0.032524041065096425,
                  "Change": 0.28017484722779185},
                 {"Site": "en.wikipedia.org",
                  "Visits": 0.028624177362280356,
                  "Change": 0.10503524254762013},
                 {"Site": "nba.sport24.gr",
                  "Visits": 0.02734001447504297,
                  "Change": -0.057600677746467314},
                 {"Site": "nba.co.jp",
                  "Visits": 0.02628877965004145,
                  "Change": -0.21513542547182316}],
                "ResultsCount": 10,
                "TotalCount": 1540,
                "Next": "http://api.similarweb.com/Site/example.com/v1/referrals?start=11-2014&end=12-2014&UserKey=test_key&page=2"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/referrals?start=11-2014&"
                  "end=12-2014&page=1&UserKey=test_key")
    f = "fixtures/sources_client_referrals_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "11-2014", "12-2014")

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.organic_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=invalid_key")
    f = "fixtures/sources_client_organic_keyword_competitors_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.organic_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("bad_url", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("http://example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_bad_page():
    expected = {"Error": "The field Page is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=0&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_page_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 0, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=14-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=0-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=12-2014&"
                  "end=9-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=12-2014&"
                  "end=9-2014&md=other&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_keyword_competitors_response_from_good_inputs():
    expected = {"Data": {"espn.go.com": 0.029560747253298304,
                         "bleacherreport.com": 0.018884794539523263,
                         "sports.yahoo.com": 0.01660474680676441,
                         "probasketballtalk.nbcsports.com": 0.011305560678493313,
                         "basketball-reference.com": 0.01121870592591383,
                         "cbssports.com": 0.010414195102828587,
                         "sports.sina.com.cn": 0.009849368251728115,
                         "si.com": 0.00836387054675375,
                         "thestar.com": 0.008291876367334255,
                         "stubhub.com": 0.007999157326624741},
                "ResultsCount": 10,
                "TotalCount": 1510,
                "Next": "http://api.similarweb.com/Site/example.com/v1/orgkwcompetitor?start=11-2014&end=12-2014&md=false&UserKey=test_key&page=2"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_organic_keyword_competitors_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        expected = json.loads(stringified)
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        client.paid_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert client.full_url == target_url


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=invalid_key")
    f = "fixtures/sources_client_paid_keyword_competitors_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("invalid_key")
        result = client.paid_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("bad_url", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("http://example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_bad_page():
    expected = {"Error": "The field Page is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=0&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_page_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 0, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=14-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=0-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=12-2014&"
                  "end=9-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=12-2014&"
                  "end=9-2014&md=other&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_keyword_competitors_response_from_good_inputs():
    expected = {"Data": {"lojanba.com": 0.07917791674254333,
                         "ticketscenter.co": 0.049233018800901834,
                         "fanatics.com": 0.04447244942383259,
                         "eventticketscenter.com": 0.039140080023049,
                         "fansedge.com": 0.038988779340718,
                         "aceticket.com": 0.03627101965540125,
                         "ticketmaster.com": 0.02999530980384764,
                         "oldglory.com": 0.020328655817132217,
                         "ticketnetwork.com": 0.01767243856389301,
                         "vividseats.com": 0.016849267072753825},
                "ResultsCount": 10,
                "TotalCount": 489,
                "Next": "http://api.similarweb.com/Site/example.com/v1/paidkwcompetitor?start=11-2014&end=12-2014&md=false&UserKey=test_key&page=2"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidkwcompetitor?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "fixtures/sources_client_paid_keyword_competitors_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        expected = json.loads(stringified)
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_keyword_competitors("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected

