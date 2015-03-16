import json
import httpretty
from similarweb import SourcesClient


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
    f = "test_fixtures/sources_client_social_referrals_good_response.json"
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
    f = "test_fixtures/sources_client_social_referrals_invalid_api_key_response.json"
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
    f = "test_fixtures/sources_client_social_referrals_url_malformed_response.json"
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
    f = "test_fixtures/sources_client_social_referrals_url_with_http_response.json"
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
    f = "test_fixtures/sources_client_social_referrals_empty_response.json"
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
    f = "test_fixtures/sources_client_social_referrals_good_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_good_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_invalid_api_key_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_url_malformed_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_url_with_http_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_page_bad_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_start_bad_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_end_bad_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_out_of_order_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_main_domain_bad_response.json"
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
    f = "test_fixtures/sources_client_organic_search_keywords_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_organic_search_keywords_response_from_good_inputs():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/orgsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "test_fixtures/sources_client_organic_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        expected = json.loads(stringified) # <~ TODO noodle a better resultant data structure
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.organic_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "test_fixtures/sources_client_paid_search_keywords_good_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_invalid_api_key_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_url_malformed_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_url_with_http_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_page_bad_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_start_bad_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_end_bad_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_out_of_order_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_main_domain_bad_response.json"
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
    f = "test_fixtures/sources_client_paid_search_keywords_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_paid_search_keywords_response_from_good_inputs():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/paidsearch?start=11-2014&"
                  "end=12-2014&md=False&page=1&UserKey=test_key")
    f = "test_fixtures/sources_client_paid_search_keywords_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        expected = json.loads(stringified) # <~ TODO noodle a better resultant data structure
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.paid_search_keywords("example.com", 1, "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_sources_client_destinations_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/leadingdestinationsites?"
                  "UserKey=test_key")
    f = "test_fixtures/sources_client_destinations_good_response.json"
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
    f = "test_fixtures/sources_client_destinations_invalid_api_key_response.json"
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
    f = "test_fixtures/sources_client_destinations_url_malformed_response.json"
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
    f = "test_fixtures/sources_client_destinations_url_with_http_response.json"
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
    f = "test_fixtures/sources_client_destinations_empty_response.json"
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
    f = "test_fixtures/sources_client_destinations_good_response.json"
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
    f = "test_fixtures/sources_client_referrals_good_response.json"
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
    f = "test_fixtures/sources_client_referrals_invalid_api_key_response.json"
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
    f = "test_fixtures/sources_client_referrals_url_malformed_response.json"
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
    f = "test_fixtures/sources_client_referrals_url_with_http_response.json"
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
    f = "test_fixtures/sources_client_referrals_page_bad_response.json"
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
    f = "test_fixtures/sources_client_referrals_start_bad_response.json"
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
    f = "test_fixtures/sources_client_referrals_end_bad_response.json"
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
    f = "test_fixtures/sources_client_referrals_out_of_order_response.json"
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
    f = "test_fixtures/sources_client_referrals_empty_response.json"
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
    f = "test_fixtures/sources_client_referrals_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        expected = json.loads(stringified) # <~ TODO noodle a better resultant data structure
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SourcesClient("test_key")
        result = client.referrals("example.com", 1, "11-2014", "12-2014")

        assert result == expected

