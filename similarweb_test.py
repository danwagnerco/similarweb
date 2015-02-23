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


def test_traffic_client_has_full_url():
    client = SimilarwebTrafficClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_traffic_client_visits_method_completes_the_full_url():
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
def test_traffic_client_visits_method_response_with_invalid_api_key():
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
def test_traffic_client_visits_method_response_with_malformed_url():
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
def test_traffic_client_visits_method_response_with_malformed_url_incl_http():
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
def test_traffic_client_visits_method_response_with_bad_granularity():
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
def test_traffic_client_visits_method_response_with_bad_start_date():
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
def test_traffic_client_visits_method_response_with_bad_end_date():
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
def test_traffic_client_visits_method_response_with_bad_main_domain():
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
def test_traffic_client_visits_method_response_with_empty_response():
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
def test_traffic_client_visits_method_response_good_response():
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
