class test():
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, value):
        self.value = value

verdi = test(5)
#print(verdi.value)
