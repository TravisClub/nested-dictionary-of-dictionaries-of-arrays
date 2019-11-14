from src import json_parser
import pytest
from unittest.mock import MagicMock

from pytest import fail


def test_read_and_sort_json_file_sorts_the_json_based_on_keys_list(some_keys_list, some_json_file):
    assert json_parser.read_and_sort_json_file(some_keys_list, some_json_file) == [
        {'country': 'ES', 'city': 'Madrid', 'currency': 'EUR', 'amount': 8.9},
        {'country': 'FR', 'city': 'Paris', 'currency': 'EUR', 'amount': 20},
        {'country': 'FR', 'city': 'Lyon', 'currency': 'EUR', 'amount': 11.4},
        {'country': 'UK', 'city': 'London', 'currency': 'FBP', 'amount': 10.9},
        {'country': 'UK', 'city': 'London', 'currency': 'GBP', 'amount': 12.2},
        {'country': 'US', 'city': 'Boston', 'currency': 'USD', 'amount': 100}]


def test_zip_dicts_zips_list_of_keys_with_sorted_json(some_keys_list, some_json_file):
    assert json_parser.zip_dicts(some_keys_list,
                                 json_parser.read_and_sort_json_file(some_keys_list, some_json_file)) == [
               {'EUR': {'ES': [{'city': 'Madrid', 'amount': 8.9}]}},
               {'EUR': {'FR': [{'city': 'Paris', 'amount': 20}]}},
               {'EUR': {'FR': [{'city': 'Lyon', 'amount': 11.4}]}},
               {'FBP': {'UK': [{'city': 'London', 'amount': 10.9}]}},
               {'GBP': {'UK': [{'city': 'London', 'amount': 12.2}]}},
               {'USD': {'US': [{'city': 'Boston', 'amount': 100}]}}]


def test_strip_key_returns_list_of_stripped_keys(some_json_file, some_keys_list):
    json_list_ordered = json_parser.read_and_sort_json_file(some_keys_list, some_json_file)
    assert json_parser.strip_key('currency', json_list_ordered) == ['EUR', 'EUR', 'EUR', 'FBP', 'GBP', 'USD']


def test_strip_key_returns_empty_list_of_stripped_keys_when_length_of_json_list_less_than_zero():
    json_list_ordered = [{}]
    assert json_parser.strip_key('currency', json_list_ordered) == []


def test_strip_key_returns_list_of_stripped_keys_when_length_of_dict_element_inside_json_list_less_than_zero():
    json_list_ordered = [
        {
            "country": "US",
            "city": "Boston",
            "currency": "USD",
            "amount": 100
        },
        {
        }]
    assert json_parser.strip_key('currency', json_list_ordered) == ['USD']


def test_script_name_removed_from_stdin_args_list(some_list_of_args):
    script_name = some_list_of_args[0]
    del some_list_of_args[0]
    assert script_name not in some_list_of_args


def test_read_and_sort_json_file_returns_same_json(some_json_file, some_keys_list):
    assert some_json_file == json_parser.read_and_sort_json_file(some_keys_list, some_json_file)
    assert type(json_parser.read_and_sort_json_file(some_keys_list, some_json_file)) == list


def test_read_and_sort_json_file_sorts_the_json(some_json_file, some_keys_list):
    first_element_unsorted_json = some_json_file[0]
    json_list_ordered = json_parser.read_and_sort_json_file(some_keys_list, some_json_file)
    first_element_sorted_json = json_list_ordered[0]
    assert first_element_unsorted_json != first_element_sorted_json


def test_read_and_sort_json_file_returns_a_valid_list_of_dicts(some_keys_list, some_json_file):
    json_list_ordered = json_parser.read_and_sort_json_file(some_keys_list, some_json_file)
    assert type(json_list_ordered) == list
    for element in json_list_ordered:
        assert type(element) == dict


def test_to_dict_parts_parameter_lenght_greater_than_one(some_dict_part_len_greater_one):
    assert json_parser.to_dict(some_dict_part_len_greater_one)


def test_build_list_dicts_converts_each_element_in_json_zipped_into_a_dict_and_adds_them_to_a_list(some_json_file,
                                                                                                   some_keys_list):
    fake_list_of_list = ['ALV', 'ALV1', 'ALV2']
    json_list_ordered = json_parser.read_and_sort_json_file(some_keys_list, some_json_file)
    fake_json_zipped = zip(*fake_list_of_list, json_list_ordered)
    assert type(json_parser.build_list_dicts(fake_json_zipped)) == list
    for _ in json_parser.build_list_dicts(fake_json_zipped):
        assert type(_) == dict


def test_build_json_generates_a_dict_out_of_a_list():
    fake_list_dicts = [{'Alvaro': 5, 'Alvaro2': 4}, {'Alvaro3': 3, 'Alvaro4': 2}]
    assert type(json_parser.build_json(fake_list_dicts)) == dict


def test_strip_keys_final_dict_nest_one_dict_inside_the_other_if_both_have_the_same_value_for_the_key_indicated_as_argument():
    fake_key = 'ALV'
    fake_dict_1 = {'ALV': [{'fake': 20}]}
    fake_dict_2 = [{'fake': 9}]
    assert json_parser.strip_keys_final_dict(fake_key, fake_dict_1, fake_dict_2) == {
        'ALV': [{'fake': 20}, {'fake': 9}]}


def test_strip_keys_final_dict_nest_more_than_one_level_dict_inside_the_other_if_both_have_the_same_value_for_the_key_indicated_as_argument():
    fake_key = 'ALV'
    fake_dict_1 = {'ALV': {'ALV1': [{'surname': 'COLL', 'number': 8}], 'ALV2': [{'surname': 'CAN', 'number': 2}]}}
    fake_dict_2 = {'ALV2': [{'surname': 'DEL', 'number': 1}]}
    assert json_parser.strip_keys_final_dict(fake_key, fake_dict_1, fake_dict_2) == {
        'ALV1': [{'number': 8, 'surname': 'COLL'}],
        'ALV2': [{'number': 2, 'surname': 'CAN'}, {'number': 1, 'surname': 'DEL'}]}


def test_strip_keys_final_dict_removes_key_from_temp_dict_when_it_only_has_one_key_before_returning_it():
    fake_key = 'ALV'
    fake_dict_1 = {'ALV': {'ALV1': [{'surname': 'COLL', 'number': 8}]}}
    fake_dict_2 = {'ALV2': [{'surname': 'DEL', 'number': 1}]}
    assert json_parser.strip_keys_final_dict(fake_key, fake_dict_1, fake_dict_2) == {
        'ALV1': [{'number': 8, 'surname': 'COLL'}], 'ALV2': [{'number': 1, 'surname': 'DEL'}]}


def test_strip_keys_final_dict_nest_one_dict_inside_the_other_where_there_are_more_than_one_key_at_the_same_level():
    fake_key = 'ALV2'
    fake_dict_1 = {'ALV1': {'fake1': [{'number': 8}]}, 'ALV2': {'fake2': [{'number': 1}]}}
    fake_dict_2 = {'fake3': [{'number': 2}]}
    assert json_parser.strip_keys_final_dict(fake_key, fake_dict_1, fake_dict_2) == {'ALV1': {'fake1': [{'number': 8}]},
                                                                                     'ALV2': {'fake2': [{'number': 1}],
                                                                                              'fake3': [{'number': 2}]}}


def test_build_json_nest_dicts_when_there_is_just_one_key_to_strip_by_that_is_shared_in_more_than_one_dicts():
    # fake_list_dicts = [{'Alvaro': 5, 'Alvaro2': 4}, {'Alvaro3': 3, 'Alvaro4': 2}]
    fake_list_dicts = [{'ALV': [{'surname': 'COLL', 'number': 2}]},
                       {'ALV': [{'surname': 'CAN', 'number': 1}]},
                       {'ALV': [{'surname': 'DEL', 'number': 8}]},
                       {'VAL': [{'surname': 'LES', 'number': 5}]}]
    assert json_parser.build_json(fake_list_dicts) == {
        'ALV': [{'surname': 'COLL', 'number': 2}, {'surname': 'CAN', 'number': 1},
                {'surname': 'DEL', 'number': 8}],
        'VAL': [{'surname': 'LES', 'number': 5}]}


def test_build_json_assign_tmp_dict_to_the_key_when_the_key_has_been_stripped_from_tmp_dict():
    fake_list_dicts = [{'ALV': {'ALV1': [{'surname': 'COLL', 'number': 8}]}},
                       {'ALV': {'ALV2': [{'surname': 'CAN', 'number': 2}]}},
                       {'ALV': {'ALV2': [{'surname': 'DEL', 'number': 1}]}}]
    assert json_parser.build_json(fake_list_dicts) == {'ALV': {'ALV1': [{'number': 8, 'surname': 'COLL'}],
                                                               'ALV2': [{'number': 2, 'surname': 'CAN'},
                                                                        {'number': 1, 'surname': 'DEL'}]}}


def test_build_json_file_swallows_FileNotFoundError_exception_when_non_existing_directory_indicated(some_json_file):
    try:
        open('/fake/path')
        fail('Exception not thrown!')
    except FileNotFoundError:
        assert True

    json_parser.build_json_file(some_json_file, '/fake/path')


def test_build_json_file_creates_a_json_file_with_the_resulting_nested_dictionary(some_final_json, tmpdir):
    file_name = tmpdir.join('result.json')
    json_parser.build_json_file(some_final_json, file_name)


def test_handle_control_flow_handles_script_flow(some_json_file, some_keys_list):
    assert json_parser.handle_control_flow(some_keys_list, some_json_file) == None


def test_typeerror_exception_raised_if_a_not_valid_number_of_keys_is_indicated(some_json_file):
    with pytest.raises(TypeError) as te:
        json_parser.read_and_sort_json_file([], some_json_file)
        assert "That was not valid number of keys" in str(te.value)


def test_keyerror_exception_raised_if_a_not_valid_key_is_indicated(some_json_file):
    with pytest.raises(KeyError) as ke:
        json_parser.read_and_sort_json_file(['ci'], some_json_file)
        assert "That was not a valid key" in str(ke.value)
