import sys
import os
import json
from operator import itemgetter


def read_and_sort_json_file(keys_list, json_list):
    """Sorts json based on list of keys.

    Parameters
    ----------
    keys_list : list
        List of keys specified in command line arguments
    json_list : list
        List of dictionaries inside json file

    Raises
    ------
    KeyError
        If one the keys passed as argument is not a valid key.
    TypeError
        If none key is indicated as argument

    Returns
    -------
    json_list : list
        The list of dictionaries inside json file sorted by keys
    """
    try:
        json_list.sort(key=itemgetter(*keys_list))
        return json_list
    except KeyError as ke:
        print("Oops!  That was not a valid key.  Try again...", ke)
        raise KeyError
    except TypeError as te:
        print("Oops!  That was not valid number of keys.  Try again...", te)
        raise TypeError


def zip_dicts(list_keys, json_list_ordered):
    """Zips the list of keys passed as arguments and the list of dictionaries inside the json file sorted by keys.
    Creates a list of lists where each list is the values of the stripped keys in each dictionary. Then zips that
    list of lists with the list of dictionaries inside the json file that have been sorted by keys.

    Parameters
    ----------
    list_keys : list
        List of keys specified in command line arguments
    json_list_ordered : list
        The list of dictionaries inside json file sorted by keys

    Returns
    -------
    list_stripped_keys_dicts : list
        a list of the no-nested dicts with the keys already stripped
    """
    list_of_lists = []
    for key in list_keys:
        list_of_lists.append(strip_key(key, json_list_ordered))
    json_zipped = zip(*list_of_lists, json_list_ordered)

    return build_list_dicts(json_zipped)


def build_list_dicts(json_zipped):
    """Builds a list of the no-nested dicts with the keys already stripped.

    Parameters
    ----------
    json_zipped : zip object
        values of the stripped keys zipped with what is left from the dicts after stripping the keys

    Returns
    -------
    list_stripped_keys_dicts : list
    """
    list_stripped_keys_dicts = []
    for i in json_zipped:
        list_stripped_keys_dicts.append(to_dict(i))
    return list_stripped_keys_dicts


def to_dict(parts):
    """Converts a tuple to a dict using dict comprehension.

    Parameters
    ----------
    parts : tuple
        each tuple in the zipped json

    Returns
    -------
    parts : dict
        the tuple transformed to a dict
    """
    if len(parts) == 1:
        return list(parts)
    else:
        return {parts[0]: to_dict(parts[1:])}


def strip_key(key, json_list_ordered):
    """Strips the key from each dictionary inside the ordered list of dictionaries and
    creates a list with the values of the stripped keys.

    Parameters
    ----------
    key : str
        The key to be stripped from the dict
    json_list_ordered : list
        The list of dictionaries inside json file sorted by keys

    Returns
    -------
    stripped_keys_list : list
        a list of the values of the stripped keys
    """
    stripped_keys_list = []
    for dict_element in json_list_ordered:
        if len(dict_element) > 0:
            stripped_keys_list.append(dict_element.pop(key))
    return stripped_keys_list


def build_json(list_dicts):
    """Generates a nested dictionary of dictionaries of arrays with the leaf values as arrays of flat dictionaries

    Parameters
    ----------
    list_dicts : list
        a list of the no-nested dicts with the keys already stripped

    Returns
    -------
    final_dict : dict
        a nested dictionary of dictionaries of arrays
    """
    final_dict = {}
    tmp_dict = {}
    for dic in list_dicts:
        key = list(dic)[0]
        if key in tmp_dict.keys():
            tmp_dict_2 = strip_keys_final_dict(key, tmp_dict, dic.pop(key))
            if key in tmp_dict_2.keys():
                tmp_dict[key] = tmp_dict_2.pop(key)
            else:
                tmp_dict[key] = tmp_dict_2
        else:
            final_dict[key] = dic.pop(key)
            tmp_dict = final_dict
    return final_dict


def strip_keys_final_dict(key, tmp_dict, aux_dict):
    """Strips the keys from the final dict and updates the dict inside recursively. If the key already exists in the dict,
    updates the value of that key with a nest dict.

    Parameters
    ----------
    key : str
        key to strip by
    tmp_dict : dict
        temporary dict where the generated dicts are added
    aux_dict : dict
        auxiliary dict

    Returns
    -------
    tmp_dict : dict
        temporary dict with the nested dicts
    """
    if isinstance(aux_dict, list):
        tmp_dict[key].append(dict(aux_dict[0]))
        return tmp_dict
    else:
        next_key = list(aux_dict)[0]
        if next_key in tmp_dict[key].keys():
            return strip_keys_final_dict(next_key, tmp_dict.pop(key), aux_dict.pop(next_key))
        else:
            tmp_dict[key].update(aux_dict)
            if len(tmp_dict.keys()) == 1:
                return tmp_dict.pop(key)
            return tmp_dict


def build_json_file(final_json, file_name):
    """Creates a json file with the resulting nested dictionary of dictionaries of arrays

    Parameters
    ----------
    final_json : dict
        a nested dictionary of dictionaries of arrays
    file_name : str
        a str that contains the path and the name of the result file

    Raises
    ------
    IOError
        If there is an error creating result file.
    """
    try:
        with open(file_name, 'w') as fp:
            json.dump(final_json, fp)
        print('[INFO] Json file created in {}'.format(file_name))
    except FileNotFoundError as fnf_error:
        print("I/O error: {}".format(fnf_error))


def handle_control_flow(list_of_keys, json_list_of_dicts):
    """Handles the control flow of the script

    Parameters
    ----------
    list_of_keys : list
        List of keys specified in command line arguments
    json_list_of_dicts : list
        List of dictionaries inside json file
    """
    json_list_ordered = read_and_sort_json_file(list_of_keys, json_list_of_dicts)
    list_dicts = zip_dicts(list_of_keys, json_list_ordered)

    final_json = build_json(list_dicts)

    # create filename for the results file
    path = os.path.abspath(__file__)
    dir_path = os.path.dirname(path)
    file_name = dir_path[:-3] + 'docs/result.json'

    build_json_file(final_json, file_name)


if __name__ == '__main__':
    # keys list and json file from stdin
    del sys.argv[0]
    stdin_str = sys.stdin.read()
    json_list = json.loads(stdin_str)

    handle_control_flow(sys.argv, json_list)
