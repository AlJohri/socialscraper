import requests, json, re

regex = re.compile("https:\/\/www.facebook.com\/(.*)")
regex2 = re.compile("https:\/\/www.facebook.com\/profile.php\?id=(.*)\&ref")

def get_id(graph_name):
    "Get the graph ID given a name."""
    get_response = lambda : requests.get('https://graph.facebook.com/' + graph_name)
    response = get_response()
    counter = 0
    while response.status_code == 400 and counter < 3:
        response = get_response()
        counter += 1
    id = json.loads(response.text).get('id', None)
    return int(id) if id else None

def get_name(graph_id):
    """Get the graph name given a graph ID."""
    response = requests.get('https://graph.facebook.com/' + graph_id)
    name = json.loads(response.text).get('name', None)
    return name

def get_attribute(graph_id,attribute):
    """Get the graph name given a graph ID."""
    response = requests.get('https://graph.facebook.com/' + graph_id)
    name = json.loads(response.text).get('attribute', None)
    return name

def find_page_username(url):

    regex_result = regex.findall(url)

    if regex_result:
        username = regex_result[0]
        if 'pages/' in username:
            uid = username.split('/')[-1]
            username = uid
            return username, uid

        if username == None: raise ValueError("No username was parsed %s" % url)
        uid = get_id(username)
        # pages/The-Talking-Heads/110857288936141
        if uid == None: raise ValueError("No userid was parsed %s" % username) # just added this
        # it errors out when it HAS username but no uid (didn't think this was possible)
    else: # old style user that doesn't have username, only uid
        regex_result = regex2.findall(url)
        if not regex_result:
            raise ValueError("URL not parseable")
        uid = regex_result[0]
        username = regex_result[0]
        if uid == None: raise ValueError("No userid was parsed %s" % url)
    return username,uid