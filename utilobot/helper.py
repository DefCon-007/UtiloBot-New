import requests

def make_request(method, url, session=None, args={}):
    """
    Make a HTTP request and returns response if it was successful
    :param method:
    :param url:
    :param session:
    :param args: Dict of request arguments like data, params, headers etc
    :return: response, session
    """
    assert method and url, "Cannot create request without method and url"
    if not session:
        session = requests.Session()
    response = session.request(method=method, url=url, **args)
    if response.status_code == 200:
        return response, session
    else:
        print("Got invalid response, status-{}, \nresponse-{}".format(response.status_code,
                                                                                response.text))
        return None, session