BAD_API_KEY = {"Error": "user_key_invalid"}
BAD_URL = {"Error": "Malformed or Unknown URL"}
BAD_DATE_ORDER = {"Error": "Date range is not valid"}
BAD_UNKNOWN_ERROR = {"Error": "Unknown Error"}
BAD_APP_STORE = {"Error": "App store must be 'apple' or 'google'"}


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

