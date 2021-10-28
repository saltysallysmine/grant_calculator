import webbrowser

from flask import Flask, render_template, redirect, url_for, request

from pprint import pprint
import json

import grant_calculate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    html_keys = {
        "title": "Вычисление грантов",
        "css_url": url_for('static', filename='/css/base.css'),
        'page_header': 'Заполнение данных о номинантах'
    }    

    if request.method == 'GET':
        # pprint(html_keys)
        return render_template('index.html', **html_keys)

    if request.method == 'POST':
        d = {}
        for key, value in request.form.items():
            if value:
                d[key] = value
        
        html_keys['count'] = d.get('count', None)
        html_keys['checkMe'] = d.get('checkMe', None)
        # pprint(html_keys)
        if html_keys['checkMe'] is not None:
            grant_calculate.calculate_from_file()
            return redirect('/results')

        if html_keys['count'] is None:
            return redirect('/')
        else:
            message1 = json.dumps({"count": int(html_keys['count'])})
            return redirect(url_for('.calculate', messages=message1))


@app.route('/calculate',  methods=['GET', 'POST'])
def calculate():
    html_keys = {
        'title': 'Вычисление грантов',
        'css_url': url_for('static', filename='/css/base.css'),
        'page_header': 'Заполнение данных о номинантах'
    }

    if request.method == 'GET':
        args_recieved = request.args['messages']
        html_keys.update(json.loads(args_recieved))
        
        return render_template('calculate.html', **html_keys)

    if request.method == 'POST':
        d = {}
        for key, value in request.form.items():
            if value:
                d[key] = value

        budget = int(d['budget'])
        d.pop('budget')

        ordered_keys = sorted(d.keys(), key=lambda x: (int(x.split()[-1]), x))

        participants = []
        for i in range(0, len(ordered_keys), 3):
            name = d[ordered_keys[i]]
            points = int(d[ordered_keys[i + 1]])
            requested_grant = int(d[ordered_keys[i + 2]])

            participants.append((name, points, requested_grant))
        
        grant_calculate.set_conf(budget, participants)
        grant_calculate.calculate()

        return redirect('/results')


@app.route('/results', methods=['GET', 'POST'])
def results():
    html_keys = {
        'title': 'Вычисление грантов',
        'css_url': url_for('static', filename='/css/base.css'),
        'page_header': 'Результаты',
        'min_points': grant_calculate.MIN_POINTS,
        'remainder':  grant_calculate.REMAINDER
    }
    
    if request.method == 'GET':
        html_keys['participants'] = grant_calculate.PARTICIPANTS

        return render_template('results.html', **html_keys)


if __name__ == "__main__":
    webbrowser.open('http://127.0.0.1:8080/')
    app.run(port=8080, host='127.0.0.1')
