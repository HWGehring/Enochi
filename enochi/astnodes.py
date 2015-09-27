from collections import namedtuple


class IntegerLiteral(namedtuple('IntegerLiteral', 'value')):

    def to_dict(self):
        return {'type': 'IntegerLiteral', 'value': self.value}


class UnaryOpExpression(namedtuple('UnaryOpExpression', ('op', 'rhs'))):

    def to_dict(self):
        return {'type': 'UnaryOpExpression', 'op': self.op, 'rhs': self.rhs.to_dict()}


class BinaryOpExpression(namedtuple('BinaryOpExpression', ('lhs', 'op', 'rhs'))):

    def to_dict(self):
        return {'type': 'BinaryOpExpression', 'lhs': self.lhs.to_dict(), 'op': self.op, 'rhs': self.rhs.to_dict()}
