from __future__ import annotations
from typing import Callable

class Exp:
    def eval() -> bool: pass
    def apply(self, targets: list[int], expressions: list[Exp | int]) -> Exp: pass
    def copy() -> Exp: pass


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
        while isinstance(expressions[targets[0]], int): targets[0] = expressions[targets[0]]
        self.expression = expressions[targets[0]]
        expressions[targets[0]] = self
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
        while isinstance(expressions[targets[0]], int): targets[0] = expressions[targets[0]]
        while isinstance(expressions[targets[1]], int): targets[1] = expressions[targets[1]]
        self.left_expression = expressions[targets[0]]
        self.right_expression = expressions[targets[1]]
        expressions[targets[1]] = targets[0]
        expressions[targets[0]] = self
        return self
    
    def copy(self):
        exp = BinaryExp(self.operand)
        return exp
