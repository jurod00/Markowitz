import datetime as dt

# TODO
# t0 und tn aus time zusammenbauen
# time aus t0 und tn zusammenbauen
# unterscheiden zwischen days, months, years, ... (interval)

class Time:

    def __init__(self, t0: dt.datetime, tn: dt.datetime):

        self.time = []
        self.t0 = t0
        self.tn = tn
        
        timeTemp = t0

        while timeTemp <= tn:
            self.time += [timeTemp]
            timeTemp += dt.timedelta(days=1)

    time = []
    interval : int # interval in Tagen

    def getTime(self) -> list:
        return self.time