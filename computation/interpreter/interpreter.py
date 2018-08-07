class Machine:
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression, self.environment = self.expression.reduce(self.environment)

    def log(self):
        print(f"{self.expression}, {self.environment}")

    def run(self):
        self.log()
        while self.expression.reducible:
            self.step()
            self.log()
