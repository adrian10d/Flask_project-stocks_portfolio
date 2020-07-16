import requests

address = 'http://127.0.0.1:5000/'


print('1. Show Portfolio [GET]')
request = requests.get(address)
print(request.text)


print('2. Add two new stocks [POST]')
request = requests.post(address + 'new', json={
    "name": "Apple",
    "ticker": "AAPL",
    "shares": "5",
    "cost": "365"
})
print(request.text)

request = requests.post(address + 'new', json={
    "name": "ExxonMobil",
    "ticker": "XOM",
    "shares": "15",
    "cost": "45"
})
print(request.text)


print('3. Show specific stock [GET]')
request = requests.get(address + 'XOM')
print(request.text)


print('4. Buy more shares [PUT]')
request = requests.put(address + 'XOM/buy', json={
    "shares": "15",
    "cost": "40"
})
print(request.text)


print('5. Sell shares [PUT]')
request = requests.put(address + 'AAPL/sell', json={
    "shares": "3"
})
print(request.text)


print('6. Sell all shares [PUT]')
request = requests.put(address + 'AAPL/sell', json={
    "shares": "2"
})
print(request.text)


print('7. Delete stock [DELETE]')
request = requests.delete(address + 'XOM/delete')
print(request.text)

