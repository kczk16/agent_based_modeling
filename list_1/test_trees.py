from unittest.mock import Mock
from pytest import fixture
from trees import Tree

@fixture
def tree():
    return Tree()

def test__get_regular_neighbours():

