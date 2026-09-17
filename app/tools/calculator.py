import ast
import operator

from app.tools.base import BaseTool


class CalculatorTool(BaseTool):
    name = "calculator"
    description = "Performs basic arithmetic calculations."

    _operators = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def run(self, expression: str) -> str:
        try:
            tree = ast.parse(expression, mode="eval")
            result = self._evaluate(tree.body)
            return str(result)
        except Exception as exc:
            return f"Calculation error: {exc}"

    def _evaluate(self, node: ast.AST):
        if isinstance(node, ast.Constant) and isinstance(
            node.value,
            (int, float),
        ):
            return node.value

        if isinstance(node, ast.BinOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not allowed")

            return operation(
                self._evaluate(node.left),
                self._evaluate(node.right),
            )

        if isinstance(node, ast.UnaryOp):
            operation = self._operators.get(type(node.op))

            if operation is None:
                raise ValueError("Operator not allowed")

            return operation(self._evaluate(node.operand))

        raise ValueError("Expression not allowed")
