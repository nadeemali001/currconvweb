from flask import Flask, jsonify, render_template, request
import requests
from requests.models import Response

app = Flask(__name__)


def get_api_data(curr='INR'):
    url = "https://exchangerate-api.p.rapidapi.com/rapid/latest/"+curr
    headers = {
        'x-rapidapi-key': "c1d09c28bfmshb2808a837422c24p146597jsn3d0854df82ee",
        'x-rapidapi-host': "exchangerate-api.p.rapidapi.com"
    }
    return requests.request("GET", url, headers=headers).json()


def result(from_curr='INR', to_curr='USD', amt=1):
    conversion = {}
    for k, v in get_api_data(from_curr)["rates"].items():
        if(k == to_curr):
            result = float(v)*float(amt)
    # return str(result)
    return render_template("index.html", converted=str(result))


def get_dropdown():
    curr_list = []
    for i in get_api_data()["rates"]:
        curr_list.append(i)
    list_items = sorted(curr_list)
    return render_template("index.html", list_items=sorted(curr_list, reverse=True))


@app.route('/', methods=['GET', 'POST'])
def run():
    if (request.method == 'GET'):
        return get_dropdown()
    elif(request.method == 'POST'):
        # get_dropdown()
        from_cur = request.form.get('from_curr')
        to_cur = request.form.get('to_curr')
        amt = request.form.get('amt')
        #print(to_cur, from_cur, amt)
        return result(to_cur, from_cur, amt)
