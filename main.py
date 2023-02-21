import requests
from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
from livereload import Server


app = Flask(__name__)


@app.route('/')
def cricgfg():
    url = request.args.get('url')

    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, "html.parser")
    sect = soup.find_all('div', id='matchCenter')
    data_array = []

    section = sect[0]
    main = section.find('div', class_='cb-min-bat-rw')
    # WI 92/3 (42)
    score = main.find('span', class_='cb-font-20 text-bold').text
    # CRR: 2.19
    crr = main.find('span', class_='cb-font-12 cb-text-gray').text
    # 42/3 (42) | 2.19
    data_array.append([score.strip(), crr.strip()])

    # store stats
    stats = section.find('div', class_='cb-col cb-col-33 cb-key-st-lst')
    stats = stats.find_all('div', class_='cb-min-itm-rw')
    data_array.append([x.text for x in stats])

    # batting cards && bowling cards
    cards = section.find_all('div', class_='cb-min-inf')
    batting = cards[0].find_all('div', class_='cb-min-itm-rw')
    bowling = cards[1].find_all('div', class_='cb-min-itm-rw')

    for index, batter in enumerate(batting):
        data = [f'batter{index}'] + [x.text for x in batter.find_all('div', {'class': lambda c: c.startswith('cb-col')})]
        data_array.append(data)

    for index, bowler in enumerate(bowling):
        data = [f'bowler{index}'] + [x.text for x in bowler.find_all('div', {'class': lambda c: c.startswith('cb-col')})]
        data_array.append(data)

    return jsonify(data_array)


if __name__ == "__main__":
    app.run()  # TODO: for production, use waitress or gunicorn
    # server = Server(app.wsgi_app)
    # server.serve()
