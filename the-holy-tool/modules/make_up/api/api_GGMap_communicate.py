import requests

url = 'https://maps.googleapis.com/maps/api/geocode/json?'
key = '&key=AIzaSyARFbwnqTzxsfWosJ6fTyEDKeMriFiAlIY'


def get_from_ggmap(address):
    # Do the request and get the response data
    params = {
        'address': address,
        'componentRestrictions': {
            'country': 'VN'
        }
    }
    req = requests.get(url + key, params=params)
    res = req.json()
    # Use the first result
    try:
        return res['results'][0]['geometry']['location']
    except IndexError:
        return None