import pytest


@pytest.fixture()
def some_json_file():
    yield [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
            "country": "FR",
            "city": "Paris",
            "currency": "EUR",
            "amount": 20
        },
        {
            "country": "FR",
            "city": "Lyon",
            "currency": "EUR",
            "amount": 11.4
        },
        {
            "country": "ES",
            "city": "Madrid",
            "currency": "EUR",
            "amount": 8.9
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "GBP",
            "amount": 12.2
        },
        {
            "country": "UK",
            "city": "London",
            "currency": "FBP",
            "amount": 10.9
        }
    ]


@pytest.fixture()
def some_keys_list():
    yield ['currency', 'country']


@pytest.fixture()
def some_dict_part_len_greater_one():
    yield ('Alvaro', 'Collantes', {'city': 'London', 'number': 8})


@pytest.fixture()
def some_list_of_args():
    yield ['fake/script_name.py', 'arg1', 'arg2', 'arg3']


@pytest.fixture()
def some_final_json():
    yield {"EUR": [{"country": "FR", "city": "Paris", "amount": 20}, {"country": "FR", "city": "Lyon", "amount": 11.4},
                   {"country": "ES", "city": "Madrid", "amount": 8.9}]}
