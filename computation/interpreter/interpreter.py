class Machine(object):
    def __init__(self, expression, environment):
        self.expression = expression
        self.environment = environment

    def step(self):
        self.expression, self.environment = self.expression.reduce(self.environment)

    def run(self):
        while self.expression.reducible:
            print("{}, {}".format(self.expression, self.environment))
            self.step()
        print("{}, {}".format(self.expression, self.environment))
