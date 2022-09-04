import abc


class Condition:
    name: str

    def __init__(self, name: str):
        self.name = name

    def name(self):
        return self.name

    @abc.abstractmethod
    def test(self):
        return


