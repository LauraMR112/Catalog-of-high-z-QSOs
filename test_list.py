import os
import yaml
from yaml.loader import SafeLoader
import glob
import warnings

import pytest


# Grab all the QSOs
QSOs_files = glob.glob('QSOs/*yml')

def test_repo_structure():
    assert os.path.exists('list.yaml') == True, "There doesn't seem to be a `list.yaml` file present"
    assert os.path.exists('QSOs/') == True, "There don't seem to be any QSOs"

def test_list_yaml():

    with open('list.yaml') as f:
        list_yaml = yaml.load(f, Loader=SafeLoader)
        required_yaml_keys = ["name", "description", "properties"]

        for key in required_yaml_keys:
            assert key in list_yaml.keys(), f"`list.yaml` is missing `{key}` property"

        # check the defailt keys?
        #required_assets = ['default_id','default_ra','default_dec','default_phot_z','default_ref']

@pytest.mark.parametrize("QSO", QSOs_files)
def test_list_properties(QSO):

    """
    Check that all keys in every QSO are valid and that all keys in list.yaml are defined.
    """

    # Gather the List property keys defined in list.yaml
    property_keys = []
    with open('list.yaml') as f:
        list_yaml = yaml.load(f, Loader=SafeLoader)
        for dic in list_yaml['properties']:
            property_keys.append(dic['key'])

    # For each QSO file check that we're not defining invalid properties
    with open(QSO) as f:
        QSO_yaml = yaml.load(f, Loader=SafeLoader)
        QSO_name = os.path.basename(QSO).replace('.yml','')
        QSO_property_keys = QSO_yaml.keys()

        invalid_keys = set(QSO_property_keys) - set(property_keys)
        assert not invalid_keys, f"{QSO_name} has invalid property keys: {invalid_keys}"

        unused_keys = list[set(property_keys) - set(QSO_property_keys)]
        if not unused_keys:
            warning.warn(f'{QSO_name} does not define the following properties: {unused_keys}', Warning)


@pytest.mark.parametrize("QSO", QSOs_files)
def test_required_list_properties(QSO):
    """
    Check that all required properties are defined.
    """

    required_property_keys = {}
    with open('list.yaml') as f:
        list_yaml = yaml.load(f, Loader=SafeLoader)
        for dic in list_yaml['properties']:
            if dic['required']:
                required_property_keys[dic['key']] = dic['kind']

    with open(QSO) as f:
        QSO_yaml = yaml.load(f, Loader=SafeLoader)
        QSO_name = os.path.basename(QSO).replace('.yml','')
        QSO_property_keys = QSO_yaml.keys()

        for key in required_property_keys.keys():
            # check that all requred properties are present
            assert key in QSO_property_keys, f'{QSO_name} is missing required property {key}'
            # check that all required properties are the set
            assert QSO_yaml[key]['value'], f"{QSO_name}: {key} is a required value, it must be set"

            # check that all required properties are the correct type
            if required_property_keys[key] == 'string':
                assert isinstance(QSO_yaml[key]['value'], str), f"{QSO_name}: value for {key} must be {required_property_keys[key]}"

            if required_property_keys[key] == 'float':
                assert isinstance(QSO_yaml[key]['value'], float), f"{QSO_name}: value for {key} must be {required_property_keys[key]}"

            if required_property_keys[key] == 'int':
                assert isinstance(QSO_yaml[key]['value'], int), f"{QSO_name}: value for {key} must be {required_property_keys[key]}"


#if __name__ == '__main__':
#    test_repo_structure()
#    test_list_yaml()
#    test_list_properties()
#    test_required_list_properties()
