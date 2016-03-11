import json
import httpretty
import os
from similarweb import MobileClient

TD = os.path.dirname(os.path.realpath(__file__))

def test_mobile_client_has_user_key():
    client = MobileClient("test_key")

    assert client.user_key == "test_key"


def test_mobile_client_has_base_url():
    client = MobileClient("test_key")

    assert client.base_url == "https://api.similarweb.com/Mobile/{0}/{1}/"


def test_mobile_client_has_empty_full_url():
    client = MobileClient("test_key")

    assert client.full_url == ""


@httpretty.activate
def test_mobile_client_app_details_completes_full_url():
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.yahoo.mobile.client.android.mail/v1/GetAppDetails"
                  "?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_app_details_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        client.app_details("com.yahoo.mobile.client.android.mail", "google")

        assert client.full_url == target_url


def test_mobile_client_app_details_response_from_bad_store():
    expected = {"Error": "App store must be 'apple' or 'google'"}
    client = MobileClient("test_key")
    result = client.app_details("com.yahoo.mobile.client.android.mail", "shrimp")

    assert result == expected


@httpretty.activate
def test_mobile_client_app_details_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.yahoo.mobile.client.android.mail/v1/GetAppDetails"
                  "?UserKey=invalid_key")
    f = "{0}/fixtures/mobile_client_app_details_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("invalid_key")
        result = client.app_details("com.yahoo.mobile.client.android.mail",
                                    "google")

        assert result == expected


@httpretty.activate
def test_mobile_client_app_details_response_from_malformed_app_id():
    expected = {"Title": None,
                "Cover": None,
                "Author": None,
                "Price": None,
                "MainCategory": None,
                "MainCategoryId": None,
                "Rating": 0}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.bad_app_id/v1/GetAppDetails?UserKey=invalid_key")
    f = "{0}/fixtures/mobile_client_app_details_malformed_app_id_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.app_details("com.bad_app_id",
                                    "google")

        assert result == expected


@httpretty.activate
def test_mobile_client_app_details_response_from_oddly_nil_response():
    expected = {"Title": None,
                "Cover": None,
                "Author": None,
                "Price": None,
                "MainCategory": None,
                "MainCategoryId": None,
                "Rating": 0}
    target_url = ("https://api.similarweb.com/Mobile/1/"
                  "com.clickgamer.angrybirds/v1/"
                  "GetAppDetails?UserKey=invalid_key")
    f = "{0}/fixtures/mobile_client_app_details_oddly_nil_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.app_details("com.clickgamer.angrybirds",
                                    "apple")

        assert result == expected


@httpretty.activate
def test_mobile_client_app_details_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("https://api.similarweb.com/Mobile/1/"
                  "com.cnn.cnnmoney/v1/GetAppDetails?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_app_details_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.app_details("com.cnn.cnnmoney",
                                    "apple")

        assert result == expected


@httpretty.activate
def test_mobile_client_app_details_response_from_good_inputs():
    expected = {"Title": "Yahoo Mail",
                "Cover": "http://www.shrimp.com",
                "Author": "Yahoo",
                "Price": "Free",
                "MainCategory": "Communication",
                "MainCategoryId": "communication",
                "Rating": 4.186773300170898}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.yahoo.mobile.client.android.mail/v1/"
                  "GetAppDetails?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_app_details_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.app_details("com.yahoo.mobile.client.android.mail",
                                    "google")

        assert result == expected


@httpretty.activate
def test_mobile_client_google_app_installs_completes_full_url():
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.yahoo.mobile.client.android.mail/v1/GetAppInstalls"
                  "?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_google_app_installs_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        client.google_app_installs("com.yahoo.mobile.client.android.mail")

        assert client.full_url == target_url


@httpretty.activate
def test_mobile_client_google_app_installs_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.yahoo.mobile.client.android.mail/v1/GetAppInstalls"
                  "?UserKey=invalid_key")
    f = "{0}/fixtures/mobile_client_google_app_installs_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("invalid_key")
        result = client.google_app_installs("com.yahoo.mobile.client.android.mail")

        assert result == expected


@httpretty.activate
def test_mobile_client_google_app_installs_response_oddly_nil_response():
    expected = {"InstallsMin": 0,
                "InstallsMax": 0}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.clickgamer.angrybirds/v1/"
                  "GetAppInstalls?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_google_app_installs_oddly_nil_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.google_app_installs("com.clickgamer.angrybirds")

        assert result == expected


@httpretty.activate
def test_mobile_client_google_app_installs_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "com.cnn.cnnmoney/v1/GetAppInstalls?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_google_app_installs_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.google_app_installs("com.cnn.cnnmoney")

        assert result == expected


def test_mobile_client_site_related_apps_response_from_bad_store():
    expected = {"Error": "App store must be 'apple' or 'google'"}
    client = MobileClient("test_key")
    result = client.site_related_apps("google.com", "shrimp")

    assert result == expected


@httpretty.activate
def test_mobile_client_site_related_apps_completes_full_url():
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "google.com/v1/GetRelatedSiteApps?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        print(stringified)
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        client.site_related_apps("google.com", "google")

        assert client.full_url == target_url


@httpretty.activate
def test_mobile_client_site_related_apps_response_from_invalid_api_key():
    expected = {"Error": "user_key_invalid"}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "google.com/v1/GetRelatedSiteApps?UserKey=invalid_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_invalid_api_key_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("invalid_key")
        result = client.site_related_apps("google.com", "google")

        assert result == expected


@httpretty.activate
def test_mobile_client_site_related_apps_response_from_malformed_url():
    expected = {"Error": "Malformed or Unknown URL"}
    target_url = ("https://api.similarweb.com/Mobile/1/"
                  "bad_url/v1/GetRelatedSiteApps?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_url_malformed_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.site_related_apps("bad_url", "apple")

        assert result == expected


@httpretty.activate
def test_mobile_client_site_related_apps_response_from_empty_response():
    expected = {"Error": "Unknown Error"}
    target_url = ("https://api.similarweb.com/Mobile/1/"
                  "apple.com/v1/GetRelatedSiteApps?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_empty_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.site_related_apps("apple.com", "apple")

        assert result == expected


@httpretty.activate
def test_mobile_client_site_related_apps_response_from_good_inputs_google():
    expected = {"com.google.android.youtube": "YouTube",
                "com.google.android.apps.maps": "Maps",
                "com.google.android.gms": "Google Play services"}
    target_url = ("https://api.similarweb.com/Mobile/0/"
                  "google.com/v1/GetRelatedSiteApps?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_good_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.site_related_apps("google.com", "google")

        assert result == expected


@httpretty.activate
def test_mobile_client_site_related_apps_response_from_good_inputs_apple():
    expected = {"284417350": "Remote",
                "364709193": "iBooks",
                "376101648": "Find My iPhone"}
    target_url = ("https://api.similarweb.com/Mobile/1/"
                  "apple.com/v1/GetRelatedSiteApps?UserKey=test_key")
    f = "{0}/fixtures/mobile_client_site_related_apps_good_apple_response.json".format(TD)
    with open(f) as data_file:
        stringified = json.dumps(json.load(data_file))
        httpretty.register_uri(httpretty.GET, target_url, body=stringified)
        client = MobileClient("test_key")
        result = client.site_related_apps("apple.com", "apple")

        assert result == expected

