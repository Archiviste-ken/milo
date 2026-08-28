import ast
import operator
from app.tools.tool_result import ToolResult


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
}


def _evaluate(node):

    if isinstance(node, ast.Constant):

        if isinstance(node.value, (int, float)):
            return node.value

        raise ValueError("Only numbers are allowed.")

    if isinstance(node, ast.BinOp):

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operator not allowed.")

        left = _evaluate(node.left)
        right = _evaluate(node.right)

        return operation(left, right)

    if isinstance(node, ast.UnaryOp):

        operation = OPERATORS.get(type(node.op))

        if operation is None:
            raise ValueError("Operator not allowed.")

        return operation(
            _evaluate(node.operand)
        )

    raise ValueError("Invalid expression.")


def calculate(expression: str) -> ToolResult:

    try:
        tree = ast.parse(
            expression,
            mode="eval",
        )

        result = _evaluate(tree.body)

        return ToolResult(
            success=True,
            data={
                "expression": expression,
                "result": result,
            },
        )

    except Exception as exc:

        return ToolResult(
            success=False,
            error=str(exc),
        )