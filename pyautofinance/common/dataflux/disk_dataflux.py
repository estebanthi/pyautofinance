from pyautofinance.common.dataflux.dataflux import Dataflux
from pyautofinance.common.dataflux.checkers import DiskChecker
from pyautofinance.common.dataflux.loaders import DiskLoader
from pyautofinance.common.dataflux.writers import DiskWriter


class DiskDataflux(Dataflux):

    def __init__(self):
        super().__init__(DiskWriter(), DiskLoader(), DiskChecker())