import requests
from datetime import datetime, timedelta

def test_add_birthday_today(server):
    birthday="1988" + datetime.now().strftime("-%m-%d")
    with server.app_context():
        r = requests.put(server.url + '/hello/testuserA', json={'dateOfBirth': birthday})
        assert r.status_code == 204

def test_add_birthday_tomorrow(server):
    birthday="1988" + (datetime.now() + timedelta(days=1)).strftime("-%m-%d")
    with server.app_context():
        r = requests.put(server.url + '/hello/testuserB', json={'dateOfBirth': birthday})
        assert r.status_code == 204

def test_add_birthday_future(server):
    birthday=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    with server.app_context():
        r = requests.put(server.url + '/hello/testuserC', json={'dateOfBirth': birthday})
        assert r.status_code == 400

def test_add_bad_birthday(server):
    birthday=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    with server.app_context():
        r = requests.put(server.url + '/hello/weird123userFormat', json={'dateOfBirth': birthday})
        assert r.status_code == 400

def test_add_missing_birthday(server):
    birthday=(datetime.now() + timedelta(days=3)).strftime("%Y-%m-%d")
    with server.app_context():
        r = requests.put(server.url + '/hello/testuserD')
        assert r.status_code == 400  

def test_get_birthday_today(server):
    r = requests.get(server.url + '/hello/testuserA')
    assert r.status_code == 200
    items = r.json()

    assert items['message'] == 'Hello, testuserA! Happy birthday!'

def test_get_birthday_tomorrow(server):
    r = requests.get(server.url + '/hello/testuserB')
    assert r.status_code == 200  
    items = r.json()
    assert items['message'] == 'Hello, testuserB! Your birthday is in 1 day(s)!'
  

def test_get_birthday_wrong_username(server):
    r = requests.get(server.url + '/hello/weird123userFormat')
    assert r.status_code == 400

def test_get_birthday_username_not_found(server):
    r = requests.get(server.url + '/hello/testuserZ')
    assert r.status_code == 204