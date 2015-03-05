import json
import httpretty
from similarweb import ContentClient


def test_content_client_has_user_key():
    client = ContentClient("test_key")

    assert client.user_key == "test_key"


def test_content_client_has_base_url():
    client = ContentClient("test_key")

    assert client.base_url == "http://api.similarweb.com/Site/%(url)s/v2/"


def test_content_client_has_empty_full_url():
    client = ContentClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_content_client_similar_sites_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/similarsites?UserKey=test_key")
    f = "test_fixtures/content_client_similar_sites_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        client.similar_sites("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_content_client_similar_sites_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/similarsites?UserKey=invalid_key")
    f = "test_fixtures/content_client_similar_sites_invalid_api_key_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("invalid_key")
        result = client.similar_sites("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_similar_sites_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/similarsites?UserKey=test_key")
    f = "test_fixtures/content_client_similar_sites_url_malformed_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_content_client_similar_sites_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/similarsites?UserKey=test_key")
    f = "test_fixtures/content_client_similar_sites_url_with_http_response.json"
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("http://example.com")

        assert result == expected


@httpretty.activate
def test_content_client_similar_sites_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/similarsites?UserKey=test_key")
    f = "test_fixtures/content_client_similar_sites_empty_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_similar_sites_completes_full_url():
    expected = {"nfl.com": 0.9999999999999999,
                "espn.go.com": 0.9999999999998606,
                "nhl.com": 0.9999999878602834,
                "sportsillustrated.cnn.com": 0.9999872885189645,
                "sports.yahoo.com": 0.9999787609071635,
                "cbssports.com": 0.9997651564945856,
                "golfweb.com": 0.9994886009452536,
                "mlb.com": 0.9987758980414373,
                "hoopshype.com": 0.9892681920426786,
                "msn.foxsports.com": 0.98444827064877,
                "insidehoops.com": 0.9704204922805049,
                "mlb.mlb.com": 0.9610661670727825,
                "sportingnews.com": 0.9379576739746633,
                "nba-basketball.org": 0.5895781619019344,
                "dimemag.com": 0.5761373928338995,
                "sportsline.com": 0.4785488863147692,
                "slamonline.com": 0.37097801648129436,
                "realgm.com": 0.3262779713759013,
                "basketball-reference.com": 0.2913301249701222,
                "82games.com": 0.28480732814372367}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/similarsites?UserKey=test_key")
    f = "test_fixtures/content_client_similar_sites_good_response.json"
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("example.com")

        assert result == expected

