import datetime as dt

class Time:

    def __init__(self):
        pass

    @staticmethod
    def prob(times: list) -> list:
        n = len(times) - 1
        duration = times[-1] - times[0]

        prob = []
        for i in range(n):
            prob.append((times[i+1] - times[i])/duration)

        return prob