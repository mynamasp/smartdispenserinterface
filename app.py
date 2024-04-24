from flask import Flask, redirect
from flask import render_template
from datetime import datetime
from markupsafe import escape
import os

app = Flask(__name__)

import json

usernames = {1: 'Abhinav', 2: 'Aashiq'}


def run_face_recognition():
    try:
        os.system('C:/Users/prasa/smartdispenser/facedt/.venv/Scripts/python.exe C:/Users/prasa/smartdispenser/facedt/facedetect.py')
    except FileNotFoundError:
        print(f"Error: The file 'C:/Users/prasa/smartdispenser/facedt/facedetect.py' does not exist.")

# Dictionary to store drink details by ID
drinks_details = {
    201: {'name': 'Sweet Dream', 'details': 'A delightfully sweet concoction perfect for dessert.'},
    202: {'name': 'Caffeine Boost', 'details': 'A robust caffeinated drink to jump-start your day.'},
    203: {'name': 'Bitter Leaf', 'details': 'A refined bitter beverage for the acquired palate.'},
    204: {'name': 'Sour Punch', 'details': 'A tangy and sour drink that refreshes and excites.'},
}

def get_time_of_day():
    hour = datetime.now().hour
    if 5 <= hour < 12:
        return 'morning'
    elif 12 <= hour < 16:
        return 'afternoon'
    elif 16 <= hour < 19:
        return 'evening'
    else:
        return 'night'


@app.route('/')
def index():
    greeting = "Hello there, Need a Drink ?"
    return render_template('index.html', greet=greeting)


@app.route('/loading')
def loading():

    return render_template('loading.html')


@app.route('/checkUser')
def checkUser():
    run_face_recognition()
    f = open("user.txt", "r")
    if(f.readline()):
        userid = int(f.readline())
    username = usernames[userid]
    time_now = get_time_of_day()
    input_data = {
        "user_id": userid,
        "time_of_day": time_now
    }
    with open('input_data.json', 'w') as json_file:
        json.dump(input_data, json_file, indent=4)
        json_file.close()
    f.close()
    os.system("python Model.py")
    if username:
        print(username)
        address = '/user/' + username + '/home'
        return redirect(address)
    else:
        return render_template('newuser.html')




@app.route('/user/<username>/home')
def newuser(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    return render_template('user.html', username=username, balance=balance)


@app.route('/user/<username>/recommendations1')
def recommendations1(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    drink=drinks_details[202]
    return render_template('recommendations.html', username=username, balance=balance,drink=drink)

@app.route('/user/<username>/recommendations1_full')
def recommendations1_full(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    drink=drinks_details[202]
    return render_template('recommendation_full.html', username=username, balance=balance,drink=drink)

@app.route('/user/<username>/recommendations2')
def recommendations2(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    drink=drinks_details[203]
    return render_template('recommendations.html', username=username, balance=balance,drink=drink)

@app.route('/user/<username>/recommendations2_full')
def recommendations2_full(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    drink=drinks_details[203]
    return render_template('recommendation_full.html', username=username, balance=balance,drink=drink)




@app.route('/user/<username>/wallet')
def wallet(username):
    name = username
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    f.close()
    return render_template('wallet.html', username=username, balance=balance)


@app.route('/user/<username>/recharge/<amount>')
def recharge(username, amount):
    name = username
    funds = int(amount)
    f = open('wallet.json')
    wallet = json.load(f)
    balance = wallet[name]['balance']
    balance = balance + funds
    wallet[name]['balance'] = balance
    print(balance)
    with open('wallet.json', 'w') as f:
        json.dump(wallet, f)
    f.close()
    return render_template('recharge.html', username=username, balance=balance, amount=amount)


if __name__ == '__main__':
    app.run(debug=True)
