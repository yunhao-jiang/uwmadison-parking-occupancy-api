import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request

ENDPOINT = '/uw-parking-occupancy'

app = Flask(__name__)


@app.route(ENDPOINT, methods=['POST'])
def post_parking_occupancy():
    watched_lots = request.get_json()['lots']
    return get_parking_occupancy(watched_lots)


@app.route(ENDPOINT, methods=['GET'])
def get_parking_occupancy(watched_lots=None):
    lots_list = {}
    if watched_lots is None:
        # read from parameters in request if lots is None
        lots_str = request.args.get('lots')
        if lots_str is None:
            watched_lots = []
        else:
            watched_lots = [lot.strip() for lot in lots_str.split(',')]

    page = requests.get('https://transportation.wisc.edu/parking-lots/lot-occupancy-count/')
    page.raise_for_status()
    soup = BeautifulSoup(page.content, 'html.parser')

    # Find the parking lot occupancy table
    table = soup.find(id='table_1')

    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) > 0:
            region = cells[0].text.strip()
            garage = cells[1].text.split(" ", 1)
            id = garage[0].strip()
            name = garage[1].strip()
            vacancies = cells[2].text.strip()

            # add it to lot lists if it's in the watched list
            if len(watched_lots) == 0 or id in watched_lots:
                lots_list[id] = {
                    'region': region,
                    'name': name,
                    'occupancy': vacancies
                }

    return lots_list


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
