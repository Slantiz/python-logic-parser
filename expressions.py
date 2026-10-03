from __future__ import annotations
from typing import Callable

class Exp:
    def eval(self) -> bool: ...
    def apply(self, targets: list[int], expressions: list[Exp | int]) -> Exp: ...
    def copy(self) -> Exp: ...


class AtomicExp(Exp):
    value: bool

    # def __init__(self, value: bool):
    #     self.value = value

    def eval(self):
        return self.value

    def apply(self, targets: list[int], expressions: list[Exp | int]):
        return self
    
    def copy(self):
        exp = AtomicExp()
        exp.value = self.value
        return exp


class UnaryExp(Exp):
    expression: Exp
    operand: Callable[[bool], bool]

    def __init__(self, operand: Callable[[bool], bool]):
        self.operand = operand

    def eval(self):
        return self.operand(self.expression.eval())
    
    def apply(self, targets: list[int], expressions: list[Exp | int]):
        i = targets[0]
        target = expressions[i]
        while isinstance(target, int):
            i = target
            target = expressions[i]
        self.expression = target
        expressions[i] = self
        return self

    def copy(self):
        exp = UnaryExp(self.operand)
        return exp


class BinaryExp(Exp):
    left_expression: Exp
    right_expression: Exp
    operand: Callable[[bool, bool], bool]

    def __init__(self, operand: Callable[[bool, bool], bool]):
        self.operand = operand
    
    def eval(self):
        return self.operand(self.left_expression.eval(), self.right_expression.eval())
    
    def apply(self, targets: list[int], expressions: list[Exp | int]):
        li = targets[0]
        left = expressions[li]
        while isinstance(left, int):
            li = left
            left = expressions[li]

        ri = targets[1]
        right = expressions[ri]
        while isinstance(right, int):
            ri = right
            right = expressions[ri]

        self.left_expression = left
        self.right_expression = right
        expressions[ri] = li
        expressions[li] = self
        return self
    
    def copy(self):
        exp = BinaryExp(self.operand)
        return exp
