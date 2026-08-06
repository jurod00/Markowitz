from mathematics.allocations import Allocations

class SensitivityLocal:

    def __init__(self, allocations: Allocations=None):
        # Optional Dependency Injection
        self.allocations = allocations if allocations is not None else Allocations()

    def minimumReturnMARKOWITZ(self):
        pass

    def minimumReturnIRM(self):
        pass

    def stockMARKOWITZ(self):
        pass

    def stockIRM(self):
        pass

    def alphaIRM(self):
        pass

    def betaIRM(self):
        pass