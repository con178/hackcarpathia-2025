def return_specialists_times(doctor, city):
    # returns text with facilities and time of waiting for appointment
    import requests
    import pandas as pd

    url_benefits = "https://api.nfz.gov.pl/app-itl-api/queues?case=1&benefit=%s&locality=%s" % (doctor, city)
    response_benefits = requests.get(url_benefits)
    response_benefits.raise_for_status()
    benefits_data = response_benefits.json()["data"]

    all_facilities = []
    for facility in benefits_data:
        facility_data_point = [
            facility['attributes']['provider'],
            facility['attributes']['address'],
            facility['attributes']['locality'],
            facility['attributes']['phone'],
            facility['attributes']['statistics']['provider-data']['average-period'],
            facility['attributes']['place']]

        all_facilities.append(facility_data_point)

    all_facilities = pd.DataFrame(all_facilities)
    all_facilities.columns = ['facility_name', 'street', 'city', 'phone', 'waiting_time_in_days', 'benefit_name']
    all_facilities_text = all_facilities.to_string()

    return all_facilities_text






