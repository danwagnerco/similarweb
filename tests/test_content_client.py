import json
import httpretty
import os
from similarweb.similarweb import ContentClient

TD = os.path.dirname(os.path.realpath(__file__))

def test_content_client_has_user_key():
    client = ContentClient("test_key")

    assert client.user_key == "test_key"


def test_content_client_has_base_url():
    client = ContentClient("test_key")

    assert client.base_url == "http://api.similarweb.com/Site/{0}/v2/"


def test_content_client_has_empty_full_url():
    client = ContentClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_content_client_similar_sites_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/similarsites?UserKey=test_key")
    f = "{0}/fixtures/content_client_similar_sites_good_response.json".format(TD)
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
    f = "{0}/fixtures/content_client_similar_sites_invalid_api_key_response.json".format(TD)
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
    f = "{0}/fixtures/content_client_similar_sites_url_malformed_response.json".format(TD)
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
    f = "{0}/fixtures/content_client_similar_sites_url_with_http_response.json".format(TD)
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
    f = "{0}/fixtures/content_client_similar_sites_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_similar_sites_response_from_good_inputs():
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
    f = "{0}/fixtures/content_client_similar_sites_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.similar_sites("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_also_visited_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/alsovisited?UserKey=test_key")
    f = "{0}/fixtures/content_client_also_visited_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        client.also_visited("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_content_client_also_visited_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/alsovisited?UserKey=invalid_key")
    f = "{0}/fixtures/content_client_also_visited_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("invalid_key")
        result = client.also_visited("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_also_visited_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/alsovisited?UserKey=test_key")
    f = "{0}/fixtures/content_client_also_visited_url_malformed_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.also_visited("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_content_client_also_visited_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/alsovisited?UserKey=test_key")
    f = "{0}/fixtures/content_client_also_visited_url_with_http_response.json".format(TD)
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.also_visited("http://example.com")

        assert result == expected


@httpretty.activate
def test_content_client_also_visited_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/alsovisited?UserKey=test_key")
    f = "{0}/fixtures/content_client_also_visited_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.also_visited("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_also_visited_response_from_good_inputs():
    expected = {"basketball.fantasysports.yahoo.com": 0.0044233824462893015,
                "bleacherreport.com": 0.0040226422900098285,
                "nfl.com": 0.003225871488152607,
                "nhl.com": 0.0027238867724788027,
                "nbaliveonline.tv": 0.0019106016141946106,
                "basketball.realgm.com": 0.0019085029774910736,
                "basketusa.com": 0.001823751528937848,
                "nba-stream.com": 0.0012604654635019507,
                "sbnation.com": 0.0010647115089141197,
                "games.espn.go.com": 0.00103766904980084,
                "espn.go.com": 0.0008876453503041353,
                "scores.espn.go.com": 0.0007570183284250613,
                "pba.inquirer.net": 0.0004930968059184227,
                "rotoworld.com": 0.0004921489592139762}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/alsovisited?UserKey=test_key")
    f = "{0}/fixtures/content_client_also_visited_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.also_visited("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_tags_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/tags?UserKey=test_key")
    f = "{0}/fixtures/content_client_tags_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        client.tags("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_content_client_tags_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/tags?UserKey=invalid_key")
    f = "{0}/fixtures/content_client_tags_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("invalid_key")
        result = client.tags("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_tags_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/tags?UserKey=test_key")
    f = "{0}/fixtures/content_client_tags_url_malformed_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.tags("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_content_client_tags_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/tags?UserKey=test_key")
    f = "{0}/fixtures/content_client_tags_url_with_http_response.json".format(TD)
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.tags("http://example.com")

        assert result == expected


@httpretty.activate
def test_content_client_tags_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/tags?UserKey=test_key")
    f = "{0}/fixtures/content_client_tags_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.tags("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_tags_response_from_good_inputs():
    expected = {"nba": 0.6398514098507464,
                "sports": 0.36910410054316395,
                "nba draft": 0.3662137380042584,
                "basketball": 0.30321123768053937,
                "professional sports": 0.2537060998187944,
                "us sports": 0.2537060998187944,
                "pro": 0.1728851238680308,
                "sport": 0.14998747927195202,
                "leagues": 0.10235439910323241,
                "imported": 0.09014857846589025}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/tags?UserKey=test_key")
    f = "{0}/fixtures/content_client_tags_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.tags("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/category?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        client.category("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_content_client_category_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/category?UserKey=invalid_key")
    f = "{0}/fixtures/content_client_category_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("invalid_key")
        result = client.category("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/category?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_url_malformed_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_content_client_category_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/category?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_url_with_http_response.json".format(TD)
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category("http://example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/category?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_response_from_good_inputs():
    expected = {"Category": "Sports/Basketball"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/category?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_rank_completes_full_url():
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/categoryrank?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_rank_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        client.category_rank("example.com")

        assert client.full_url == target_url


@httpretty.activate
def test_content_client_category_rank_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/categoryrank?UserKey=invalid_key")
    f = "{0}/fixtures/content_client_category_rank_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("invalid_key")
        result = client.category_rank("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_rank_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "bad_url/v2/categoryrank?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_rank_url_malformed_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category_rank("bad_url")

        assert result == expected


# This response is not JSON-formatted
@httpretty.activate
def test_content_client_category_rank_response_from_malformed_url_incl_http():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("http://api.similarweb.com/Site/"
                  "http://example.com/v2/categoryrank?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_rank_url_with_http_response.json".format(TD)
    with open(f) as data_file:
        stringified = data_file.read().replace("\n", "")
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category_rank("http://example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_rank_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/categoryrank?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_rank_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category_rank("example.com")

        assert result == expected


@httpretty.activate
def test_content_client_category_rank_response_from_good_inputs():
    expected = {"Category": "Sports/Basketball",
                "CategoryRank": 1}
    target_url = ("http://api.similarweb.com/Site/"
                  "example.com/v2/categoryrank?UserKey=test_key")
    f = "{0}/fixtures/content_client_category_rank_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = ContentClient("test_key")
        result = client.category_rank("example.com")

        assert result == expected

