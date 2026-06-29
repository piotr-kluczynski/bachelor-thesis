from abc import ABC, abstractmethod

class PlayerStrategy(ABC):
    @abstractmethod
    def initializePlayer(self):
        pass

    @abstractmethod
    def simulationStart(self, simulationStartMessage):
        pass

    @abstractmethod
    def simulationEnd(self):
        pass

    @abstractmethod
    def roundStart(self, roundStartMessage):
        pass

    @abstractmethod
    def roundEnd(self):
        pass

    @abstractmethod
    def turnStart(self):
        pass

    @abstractmethod
    def turnEnd(self, turnEndMessage):
        pass