def return_coordinates(adress_name="parafia-królowej-jadwigi-rzeszów"):
    import requests

    api_key = ""
    address = adress_name

    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"
    print(url)
    response = requests.get(url).json()

    if response['status'] == 'OK':
        location = response['results'][0]['geometry']['location']
        lat = location['lat']
        lng = location['lng']
        print(lat, lng)
        return (lat, lng)
    else:
        print(f"Error: {response.get('error_message', 'Unknown error')}")
        return "Error"