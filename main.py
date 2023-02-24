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
    score_board = main.find('span', class_='cb-font-20 text-bold').text
    # store score
    data_array.append({
        'score': score_board.split(' ')[2],
        'overs': score_board.split(' ')[3],
    })

    # batting cards && bowling cards
    cards = section.find_all('div', class_='cb-min-inf')
    batting = cards[0].find_all('div', class_='cb-col cb-col-100 cb-min-itm-rw')
    bowling = cards[1].find_all('div', class_='cb-col cb-col-100 cb-min-itm-rw')

    for batter in batting:
        batter_data = batter.find_all('div', class_='cb-col')
        batter = {
            'name': batter_data[0].text,
            'R': batter_data[1].text,
            'B': batter_data[2].text,
            '4s': batter_data[3].text,
            '6s': batter_data[4].text,
            'SR': batter_data[5].text,
        }
        data_array.append(batter)

    for bowler in bowling:
        bowler_data = bowler.find_all('div', class_='cb-col')
        bowler = {
            'name': bowler_data[0].text,
            'O': bowler_data[1].text,
            'M': bowler_data[2].text,
            'R': bowler_data[3].text,
            'W': bowler_data[4].text,
            'Econ': bowler_data[5].text,
        }
        data_array.append(bowler)

    return jsonify(data_array)


if __name__ == "__main__":
    # app.run()  # TODO: for production, use waitress or gunicorn
    server = Server(app.wsgi_app)
    server.serve()
