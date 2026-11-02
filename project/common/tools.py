"""Small, safe example tools shared by the steps. Each tool = a Python function + a JSON schema."""
import ast
import operator

_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul,
        ast.Div: operator.truediv, ast.USub: operator.neg, ast.Pow: operator.pow}


def calculator(expression: str) -> str:
    """Evaluate basic arithmetic safely (no eval!)."""
    def ev(n):
        if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
            return n.value
        if isinstance(n, ast.BinOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.left), ev(n.right))
        if isinstance(n, ast.UnaryOp) and type(n.op) in _OPS:
            return _OPS[type(n.op)](ev(n.operand))
        raise ValueError("only numbers and + - * / ** are allowed")
    try:
        r = ev(ast.parse(expression, mode="eval").body)
        return str(round(r, 6))
    except Exception as e:  # errors go back to the model as text
        return f"error: {e}"


_FAKE_WEATHER = {"dhaka": "31°C, humid, light rain", "london": "12°C, cloudy", "tokyo": "18°C, clear"}


def get_weather(city: str) -> str:
    """Fake weather so the project works offline. Swap in a real API later."""
    return f"Weather in {city}: {_FAKE_WEATHER.get(city.lower(), '22°C, sunny (demo data)')}"


def schema(name, description, **params):
    """Build an OpenAI-style tool schema. params: name=(type, description)."""
    return {"type": "function", "function": {
        "name": name, "description": description,
        "parameters": {"type": "object",
                       "properties": {k: {"type": t, "description": d} for k, (t, d) in params.items()},
                       "required": list(params)}}}


TOOLS = {"calculator": calculator, "get_weather": get_weather}
SCHEMAS = [
    schema("calculator", "Evaluate an arithmetic expression like '12*(3+4)'.",
           expression=("string", "The arithmetic expression")),
    schema("get_weather", "Get the current weather for a city.", city=("string", "City name")),
]
