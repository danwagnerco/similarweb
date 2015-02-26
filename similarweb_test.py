# TODO add a test that checks valid dates where start is after end
import json
import httpretty
from similarweb import SimilarwebTrafficClient


def test_traffic_client_has_user_key():
    client = SimilarwebTrafficClient("test_key")

    assert client.user_key == "test_key"


def test_traffic_client_has_base_url():
    client = SimilarwebTrafficClient("test_key")

    assert client.base_url == "http://api.similarweb.com/Site/%(url)s/v1/"


def test_traffic_client_has_empty_full_url():
    client = SimilarwebTrafficClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_traffic_client_visits_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        client.visits("example.com", "monthly", "11-2014", "12-2014", False)

    assert client.full_url == target_url


@httpretty.activate
def test_traffic_client_visits_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=invalid_key")
    f = "test_fixtures/traffic_client_visits_invalid_user_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("invalid_key")
        result = client.visits("example.com", "monthly",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("bad_url", "monthly",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("http://example.com", "monthly",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_bad_granularity():
    expected = {"Error": "The field Gr is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=bad"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_granularity_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "bad",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=14-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=0-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=12-2014&end=9-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=other&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visits_response_from_good_inputs():
    expected = {"2014-11-01": 12897241, "2014-12-01": 13917811}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visits?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visits_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visits("example.com", "monthly",
                               "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_traffic_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/traffic?UserKey=test_key")
    f = "test_fixtures/traffic_client_traffic_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        client.traffic("example.com")

    assert client.full_url == target_url


@httpretty.activate
def test_traffic_client_traffic_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/traffic?UserKey=invalid_key")
    f = "test_fixtures/traffic_client_traffic_invalid_user_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("invalid_key")
        result = client.traffic("example.com")

        assert result == expected


@httpretty.activate
def test_traffic_client_traffic_response_from_bad_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/traffic?UserKey=test_key")
    f = "test_fixtures/traffic_client_traffic_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.traffic("bad_url")

        assert result == expected


@httpretty.activate
def test_traffic_client_traffic_response_from_bad_url_with_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http:/example.com/v1/traffic?UserKey=test_key")
    f = "test_fixtures/traffic_client_traffic_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.traffic("http://example.com")

        assert result == expected


@httpretty.activate
def test_traffic_client_traffic_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/traffic?UserKey=test_key")
    f = "test_fixtures/traffic_client_traffic_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.traffic("example.com")

        assert result == expected


@httpretty.activate
def test_traffic_client_traffic_from_good_inputs():
    expected = {"GlobalRank": 2,
                "CountryCode": 840,
                "CountryRank": 1,
                "TopCountryShares": [
                 {
                 "CountryCode": 840,
                 "TrafficShare": 0.4191358779109708
                 },
                 {
                  "CountryCode": 356,
                  "TrafficShare": 0.04602783067100975
                 },
                 {
                  "CountryCode": 876,
                  "TrafficShare": 6.869084578359956e-7
                 },
                 {
                  "CountryCode": 10,
                  "TrafficShare": 0
                 }
                ],
                "TrafficReach": [
                 {
                  "Date": "02/01/2015",
                  "Value": 0.16306846864268815
                 },
                 {
                  "Date": "09/01/2015",
                  "Value": 0.16501993162160358
                 },
                 {
                  "Date": "16/01/2015",
                  "Value": 0.1655193577048118
                 },
                 {
                  "Date": "23/01/2015",
                  "Value": 0.1665235785224394
                 },
                 {
                  "Date": "30/01/2015",
                  "Value": 0.16295290825680991
                 }
                ],
                "TrafficShares": [
                 {
                  "SourceType": "Search",
                  "SourceValue": 0.10429090056545187
                 },
                 {
                  "SourceType": "Social",
                  "SourceValue": 0.030245335003191837
                 },
                 {
                  "SourceType": "Mail",
                  "SourceValue": 0.0041178890588041694
                 },
                 {
                  "SourceType": "Paid Referrals",
                  "SourceValue": 0.0015840071128134063
                 },
                 {
                  "SourceType": "Direct",
                  "SourceValue": 0.6771397777323854
                 },
                 {
                  "SourceType": "Referrals",
                  "SourceValue": 0.1826220905273533
                 }
                ],
                "Date": "01/2015"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/traffic?UserKey=test_key")
    f = "test_fixtures/traffic_client_traffic_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.traffic("example.com")

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly&start=11-2014"
                  "&end=12-2014&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        client.pageviews("example.com", "monthly", "11-2014", "12-2014", False)

    assert client.full_url == target_url


@httpretty.activate
def test_traffic_client_pageviews_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=invalid_key")
    f = "test_fixtures/traffic_client_pageviews_invalid_user_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("invalid_key")
        result = client.pageviews("example.com", "monthly",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("bad_url", "monthly",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("http://example.com", "monthly",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_bad_granularity():
    expected = {"Error": "The field Gr is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=bad"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_granularity_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "bad",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=14-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                  "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=0-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                  "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=12-2014&end=9-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                  "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=other&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                 "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_pageviews_response_from_good_inputs():
    expected = {"2014-11-01": 14.722378910549942,
                "2014-12-01": 14.23604875567647}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/pageviews?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_pageviews_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.pageviews("example.com", "monthly",
                                  "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly&start=11-2014"
                  "&end=12-2014&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        client.visit_duration("example.com", "monthly",
                              "11-2014", "12-2014", False)

    assert client.full_url == target_url


@httpretty.activate
def test_traffic_client_visit_duration_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=invalid_key")
    f = "test_fixtures/traffic_client_visit_duration_invalid_user_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("invalid_key")
        result = client.visit_duration("example.com", "monthly",
                                       "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("bad_url", "monthly",
                                       "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_url_with_http_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("http://example.com", "monthly",
                                       "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_bad_granularity():
    expected = {"Error": "The field Gr is invalid."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=bad"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_granularity_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "bad",
                                       "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_bad_start_date():
    expected = {"Error": "The value '14-2014' is not valid for Start."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=14-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_start_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "14-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_bad_end_date():
    expected = {"Error": "The value '0-2014' is not valid for End."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=0-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_end_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "11-2014", "0-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_out_of_order_dates():
    expected = {"Error": "Date range is not valid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=12-2014&end=9-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_out_of_order_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "12-2014", "9-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_bad_main_domain():
    expected = {"Error": "The value 'other' is not valid for Md."}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=other&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_main_domain_bad_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "11-2014", "12-2014", "other")

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "11-2014", "12-2014", False)

        assert result == expected


@httpretty.activate
def test_traffic_client_visit_duration_response_from_good_inputs():
    expected = {"2014-11-01": 971.0572442455453,
                "2014-12-01": 961.5564560783813}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v1/visitduration?gr=monthly"
                  "&start=11-2014&end=12-2014"
                  "&md=False&UserKey=test_key")
    f = "test_fixtures/traffic_client_visit_duration_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = SimilarwebTrafficClient("test_key")
        result = client.visit_duration("example.com", "monthly",
                                       "11-2014", "12-2014", False)

        assert result == expected
