from base import Class, Constant, OperatorCall, forward_declarations
from base import to_primitive_function, IPrimitiveType
from typing import Union, Callable
from functools import wraps
from logic import Bool


class Numerical(IPrimitiveType):
    def __init__(self, value: Union[int, float], *args, **kwargs) -> None:
        self.value = value
        super().__init__(*args, **kwargs)


class Int(Numerical):
    def __init__(self, value: int) -> None:
        super().__init__(value, int_class)


class Float(Numerical):
    def __init__(self, value: float) -> None:
        super().__init__(value, float_class)


def numerical_compatible(fn: Callable):
    @wraps(fn)
    def numerical_compatible_fn(this: Int, other):
        assert(type(other) in [Int, Float, Bool])
        result = fn(this.value, other.value)
        if type(result) is int:
            return Int(result)
        elif type(result) is float:
            return Float(result)
        elif type(result) is bool:
            return Bool(result)
    return numerical_compatible_fn


def numerical_to_bool(this: Union[Int, Float]) -> Bool:
    return Bool(bool(this.value))


numerical_methods = {
    "#add":                 (lambda x, y: x + y),
    "#substract_left":      (lambda x, y: x - y),
    "#multiply":            (lambda x, y: x * y),
    "#divide_left":         (lambda x, y: x / y),
    "#modulo_left":         (lambda x, y: x % y),
    "#exponent_left":       (lambda x, y: x ** y),
    "#equal":               (lambda x, y: x == y),
    "#not_equal":           (lambda x, y: x != y),
    "#lesser_left":         (lambda x, y: x < y),
    "#lesser_equal_left":   (lambda x, y: x <= y),
    "#greater_left":        (lambda x, y: x > y),
    "#greater_equal_left":  (lambda x, y: x >= y),
    "#substract_right":     (lambda x, y: y - x),
    "#divide_right":        (lambda x, y: y / x),
    "#modulo_right":        (lambda x, y: y % x),
    "#exponent_right":      (lambda x, y: y ** x),
    "#lesser_right":        (lambda x, y: y < x),
    "#lesser_equal_right":  (lambda x, y: y <= x),
    "#greater_right":       (lambda x, y: y > x),
    "#greater_equal_right": (lambda x, y: y >= x)

}

int_class = Class("int",
                  {name: to_primitive_function(numerical_compatible(method))
                   for name, method in numerical_methods.items()}, {})
int_class["#to_bool"] = to_primitive_function(numerical_to_bool)

float_class = Class("float",
                    {name: to_primitive_function(numerical_compatible(method))
                     for name, method in numerical_methods.items()}, {})
float_class["#to_bool"] = to_primitive_function(numerical_to_bool)

forward_declarations["Int"] = Int
forward_declarations["Float"] = Float


print(OperatorCall("#multiply", [OperatorCall("#add", [Constant(Int(7)), Constant(Int(2))]), Constant(Int(2))]).eval({}).value)
