from pyautofinance.common.timers.timer import Timer


class StopSession(Timer):

    def execute(self, cerebro):
        cerebro.runstop()
