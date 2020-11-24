import pytest
from pytest_mock import mocker
from unittest.mock import patch
from django.forms import ValidationError

from Product.models import ProductCategory, pre_save_product_category


@pytest.fixture(scope='module')
def product_category_instance():
    product_category = ProductCategory()
    yield product_category
    del product_category

@pytest.fixture(scope = 'function')
def product_category_instances():
    product_category1 = ProductCategory()
    product_category2 = ProductCategory()
    yield (product_category1, product_category2)
    del product_category1
    del product_category2

# test pre_save_product_category signal called methods order
def test_pre_save_product_category_signal_called_methods_order(mocker):
    product_category_mock = mocker.Mock()
    calls = [mocker.call.validate_root_category(), mocker.call.validate_attributes_types(),
             mocker.call.update_category_fields(), mocker.call.inherit_attributes()]
    pre_save_product_category(mocker.Mock, product_category_mock)
    product_category_mock.assert_has_calls(calls)

# test validate_root_category
def test_if_validate_root_category_raises_exception_correctly(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.root_category = product_category_instance
        product_category_instance.validate_root_category()


# test validate_attributes_types
def test_if_validate_attributes_types_raises_exception_correctly_when_string_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': 'string'}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_dict_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': {'key': 'value'}}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_bool_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': True}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_tuple_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': (1, 2)}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_set_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': {1, 2}}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_complex_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': 3+2.7j}
        product_category_instance.validate_attributes_types()

def test_if_validate_attributes_types_raises_exception_correctly_when_none_attribute(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.attributes_json = {'atr1': None}
        product_category_instance.validate_attributes_types()

# test update_category_fields
def test_update_category_fields_method_when_none_root_category(product_category_instances):
    product_category_instances[0].category_name = 'Test category'
    product_category_instances[0].update_category_fields()
    assert product_category_instances[0].category_path == product_category_instances[0].category_name

def test_update_category_fields_method_when_specific_root_category(product_category_instances):
    product_category_instances[0].category_name = 'Test category'
    product_category_instances[1].category_path = 'Root category'

    product_category_instances[0].root_category = product_category_instances[1]
    with patch('Product.models.ProductCategory.make_root'): # TODO: Nie przetestowane metody: make_root i un_root
       product_category_instances[0].update_category_fields()
    assert product_category_instances[0].category_path == product_category_instances[1].category_path + '-' + product_category_instances[0].category_name

def test_update_category_fields_method_when_none_attributes_old_json(product_category_instances):
    product_category_instances[0].attributes_json = {"test": 2}
    with patch('Product.models.ProductCategory.make_root'):
       product_category_instances[0].update_category_fields()
    assert product_category_instances[0].attributes_old_json == product_category_instances[0].attributes_json

def test_update_category_fields_method_when_specific_attributes_old_json(product_category_instances):
    product_category_instances[0].attributes_json = {"test": 2}
    product_category_instances[0].attributes_old_json = {"test": 1}
    expected_value = product_category_instances[0].attributes_old_json
    with patch('Product.models.ProductCategory.make_root'):
       product_category_instances[0].update_category_fields()
    assert product_category_instances[0].attributes_old_json == expected_value

# test inherit_attributes
def test_inherit_attributes_method_works_correctly(product_category_instances):
    product_category_instances[0].attributes_json = {"test": 1}
    product_category_instances[1].root_category = product_category_instances[0]
    product_category_instances[1].attributes_json = {"dane": 0}
    product_category_instances[1].inherit_attributes()
    assert product_category_instances[1].attributes_json == product_category_instances[0].attributes_json













#################################################################################################

# @pytest.fixture()
# def product_category_instances():
#     product_category1 = ProductCategory()
#     product_category2 = ProductCategory()
#     yield (product_category1, product_category2)
#     del product_category1
#     del product_category2

# testy validate_attributes_types
# def test_inherit_attributes(product_category_instances):
#     product_category_instances[0].attributes_json = {"test": 1}
#     product_category_instances[1].root_category = product_category_instances[1]
#     product_category_instances[1].attributes_json = {"dane": 0}
#     assert product_category_instances[1].attributes_json == product_category_instances[0].attributes_json
