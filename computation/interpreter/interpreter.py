class Machine:
    def __init__(self, expression, environment: dict, debug: bool = False):
        self.expression = expression
        self.environment = environment
        self.debug = debug

    def step(self):
        self.expression, self.environment = self.expression.reduce(self.environment)

    def log(self):
        if self.debug:
            print(f"{self.expression}, {self.environment}")

    def run(self):
        self.log()
        while self.expression.reducible:
            self.step()
            self.log()
        return self
