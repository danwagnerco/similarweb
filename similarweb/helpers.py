BAD_API_KEY = {"Error": "user_key_invalid"}
BAD_URL = {"Error": "Malformed or Unknown URL"}
BAD_DATE_ORDER = {"Error": "Date range is not valid"}
BAD_UNKNOWN_ERROR = {"Error": "Unknown Error"}


def bad_inputs_to_traffic_or_sources_api(dictionary):
    sub = dictionary["ModelState"]
    error_message = list(sub.values())[0][0]
    return {"Error": error_message}

