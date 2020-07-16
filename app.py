from flask import Flask, render_template, request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import yfinance as yf


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///stocks.db'
db = SQLAlchemy(app)

class Stocks(db.Model):
    ticker = db.Column(db.String(8), primary_key=True, nullable=False)
    name = db.Column(db.String(64), nullable=False)
    avg_cost = db.Column(db.Integer, nullable=False)
    shares = db.Column(db.Integer, nullable=False)


def get_last_price(ticker):
    stock_df = yf.Ticker(ticker).history()
    last_price = stock_df['Close'][-1]
    return last_price


def portfolio_to_json():

    stocks = Stocks.query.order_by(Stocks.ticker).all()
    stocks_array = []
    for stock in stocks:
        stock_obj = {
                    "name": stock.name,
                    "ticker": stock.ticker,
                    "shares": stock.shares,
                    "avg_cost": stock.avg_cost,
                    "last_price": get_last_price(stock.ticker)
                }
        stocks_array.append(stock_obj)

    stocks_json = {
        "stocks": stocks_array
    }
    return stocks_json


def return_stock(ticker):
    stocks = Stocks.query.order_by(Stocks.name).all()
    for stock in stocks:
        if ticker == stock.ticker:
            stock_obj = {
                "name": stock.name,
                "ticker": stock.ticker,
                "shares": stock.shares,
                "avg_cost": stock.avg_cost,
                "last_price": get_last_price(stock.ticker)
            }
            return stock_obj
    return 'No such stock'


def delete_stock(ticker):
    Stocks.query.filter(Stocks.ticker == ticker).delete()
    db.session.commit()


@app.route('/', methods=['GET'])
def home():
    return portfolio_to_json()


@app.route('/new', methods=['POST'])
def new():
    name = request.json['name']
    ticker = request.json['ticker']
    shares = int(request.json['shares'])
    cost = int(request.json['cost'])

    new_stock = Stocks(name=name, ticker=ticker, avg_cost=cost, shares=shares)

    try:
        db.session.add(new_stock)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem'


@app.route('/<ticker>', methods=['GET'])
def stock(ticker):
    return return_stock(ticker)


@app.route('/<ticker>/delete', methods=['DELETE'])
def stock_delete(ticker):
    delete_stock(ticker)
    return portfolio_to_json()


@app.route('/<ticker>/buy', methods=['PUT'])
def stock_buy(ticker):
    no_of_shares = int(request.json['shares'])
    cost = int(request.json['cost'])

    try:
        stock_tmp = Stocks.query.filter(Stocks.ticker == ticker).first()
        stock_tmp.avg_cost = round(((stock_tmp.avg_cost * stock_tmp.shares) + (cost * no_of_shares)) /\
                             (stock_tmp.shares + no_of_shares), 1)
        stock_tmp.shares += no_of_shares
        db.session.commit()
    except:
        return 'There was a problem'
    return return_stock(ticker)


@app.route('/<ticker>/sell', methods=['PUT'])
def stock_sell(ticker):
    no_of_shares = int(request.json['shares'])
    stock_tmp = Stocks.query.filter(Stocks.ticker == ticker).first()
    if no_of_shares == stock_tmp.shares:
        delete_stock(ticker)
        return portfolio_to_json()
    else:
        stock_tmp.shares -= no_of_shares
        db.session.commit()
        return return_stock(ticker)