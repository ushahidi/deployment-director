from DeploymentDirector.rules import CoerceArray, CoerceToDict

def test_coerce_array():
  assert CoerceArray(1) == [1]
  assert CoerceArray([1,2,3]) == [1,2,3]

def test_coerce_to_dict():
  assert CoerceToDict('x')(1) == { 'x': 1 }
  assert CoerceToDict('x')({ 'x': 1, 'y': 2 }) == { 'x': 1, 'y': 2 }
