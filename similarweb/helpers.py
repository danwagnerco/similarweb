import requests
try:
    import simplejson as json
except (ImportError, SyntaxError):
    import json

BAD_API_KEY = {"Error": "user_key_invalid"}
BAD_URL = {"Error": "Malformed or Unknown URL"}
BAD_DATE_ORDER = {"Error": "Date range is not valid"}
BAD_UNKNOWN_ERROR = {"Error": "Unknown Error"}
BAD_APP_STORE = {"Error": "App store must be 'apple' or 'google'"}

def get_http_response(url):
    try:
        response = requests.get(url)
        return json.loads(response.text)
    except ValueError:
        return BAD_URL


def dictify(list_of_dicts, to_be_keys, to_be_values, stringify_keys = False):
    values = [d[to_be_values] for d in list_of_dicts]
    if stringify_keys:
        keys = [str(d[to_be_keys]) for d in list_of_dicts]
    else:
        keys = [d[to_be_keys] for d in list_of_dicts]
    return dict(zip(keys, values))


def bad_inputs_to_traffic_or_sources_api(dictionary):
    sub = dictionary["ModelState"]
    error_message = list(sub.values())[0][0]
    return {"Error": error_message}


def input_to_app_store_is_bad(string):
    clean = string.strip().lower()
    if clean == "apple" or clean == "google":
        return False
    else:
        return True


def app_store_id_to_number(string):
    clean = string.strip().lower()
    if string == "apple":
        return 1
    else:
        return 0

