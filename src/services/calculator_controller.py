


class CalculatorController:
    def __init__(self):
        self.engine = CalculatorEngine()
        self.expression = ""

    def input(self, value: str) -> str:
        if value == "AC":
            self.expression = ""
            return "0"

        elif value == "=":
            result = self.engine.evaluate(self.expression)
            self.expression = result
            return result

        else:
            self.expression += value
            return self.expression