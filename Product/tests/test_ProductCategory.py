import pytest
from pytest_mock import mocker
from django.forms import ValidationError

from Product.models import ProductCategory, update_category_pre


@pytest.fixture(scope='module')
def product_category_instance():
    product_category = ProductCategory()
    yield product_category
    del product_category


# testy validate_attributes_types
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

# testy validate_root_category
def test_if_validate_root_category_raises_exception_correctly(product_category_instance):
    with pytest.raises(ValidationError):
        product_category_instance.root_category = product_category_instance
        product_category_instance.validate_root_category()



@pytest.fixture(scope = 'module')
def product_category_instances():
    product_category1 = ProductCategory()
    product_category2 = ProductCategory()
    yield (product_category1, product_category2)
    del product_category1
    del product_category2

# testy inherit_attributes
def test_inherit_attributes_method_works_correctly(product_category_instances): # TUTAJ TRZEBA UZYC MOCKOWANIA JAKIEGOS
    product_category_instances[0].attributes_json = {"test": 1}
    product_category_instances[1].root_category = product_category_instances[0]
    product_category_instances[1].attributes_json = {"dane": 0}
    product_category_instances[1].inherit_attributes()
    assert product_category_instances[1].attributes_json == product_category_instances[0].attributes_json

def test_if_inherit_attributes_method_is_called(mocker, product_category_instances):
    mocker.patch('Product.models.ProductCategory.inherit_attributes')
    update_category_pre(ProductCategory, product_category_instances[0])
    ProductCategory.inherit_attributes.assert_called()











#################################################################################################

# @pytest.fixture()
# def product_category_instances():
#     product_category1 = ProductCategory()
#     product_category2 = ProductCategory()
#     yield (product_category1, product_category2)
#     del product_category1
#     del product_category2

# testy validate_attributes_types
# def test_inherit_attributes(product_category_instances): # TUTAJ TRZEBA UZYC MOCKOWANIA JAKIEGOS
#     product_category_instances[0].attributes_json = {"test": 1}
#     product_category_instances[1].root_category = product_category_instances[1]
#     product_category_instances[1].attributes_json = {"dane": 0}
#     assert product_category_instances[1].attributes_json == product_category_instances[0].attributes_json
