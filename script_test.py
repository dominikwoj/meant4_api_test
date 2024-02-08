import json

import requests


class restful_booker:
    base_url = 'https://restful-booker.herokuapp.com/'
    headers_options = {}

    def __init__(self):
        self.session = requests.Session()
        self.token = 'YWRtaW46cGFzc3dvcmQxMjM='
        self.headers = {"Content-Type": "application/json", "Authorization": f"Basic {self.token}"}
        self.url = None

    def get_url(self, partial_url):
        self.url = f'{self.base_url}{partial_url}'
        # print(f'url:{self.url}')
        return self.url

    def ping(self):
        response = self.session.get(url=self.get_url('ping'), data=None, headers=None)
        return response

    def auth_create_token(self, data):
        return self.session.post(url=self.get_url('auth'), data=data, headers=None)

    def get_booking_ids(self, filter):
        return self.session.get(url=self.get_url(f'booking?{filter}'), data=None, headers=None)

    def get_booking_by_id(self, id):
        return self.session.get(url=self.get_url(f'booking/{id}'), data=None, headers=None)

    def create_booking(self, data):
        return self.session.post(url=self.get_url(f'booking/'), data=json.dumps(data), headers=self.headers)

    def update_booking(self, id, data):
        return self.session.put(url=self.get_url(f'booking/{id}'), data=json.dumps(data), headers=self.headers)

    def partial_update_booking(self, id, data):
        return self.session.patch(url=self.get_url(f'booking/{id}'), data=json.dumps(data), headers=self.headers)

    def delete_booking_by_id(self, id):
        return self.session.delete(url=self.get_url(f'booking/{id}'), data=None, headers=self.headers)


book_id = None


def test__ping():
    api = restful_booker()
    response = api.ping()
    assert response.status_code == 201


def test__auth():
    api = restful_booker()
    response = api.auth_create_token({"username": "admin", "password": "password123"})
    assert response.status_code == 200


def test__get_booking_ids():
    api = restful_booker()
    response = api.get_booking_ids(filter)
    assert response.status_code == 200
    response_json = response.json()
    global book_id
    book_id = response_json[0]['bookingid']


def test__get_booking_by_ids():
    global book_id
    api = restful_booker()
    response = api.get_booking_by_id(book_id)
    assert response.status_code == 200


def test__create_booking():
    api = restful_booker()
    data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = api.create_booking(data)
    assert response.status_code == 200
    response_json = response.json()

    global book_id
    book_id = response_json['bookingid']


def test__update_booking():
    global book_id
    api = restful_booker()
    data = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 112,
        "depositpaid": True,
        "bookingdates": {
            "checkin": "2018-01-01",
            "checkout": "2019-01-01"
        },
        "additionalneeds": "Breakfast"
    }
    response = api.update_booking(book_id, data)
    assert response.status_code == 200


def test__partial_update_booking():
    global book_id
    api = restful_booker()
    data = {
        "firstname": "Jim",
        "lastname": "Brown"
    }
    response = api.partial_update_booking(book_id, data)
    assert response.status_code == 200


def test__delete_booking():
    global book_id
    api = restful_booker()
    response = api.delete_booking_by_id(book_id)
    assert response.status_code == 201
