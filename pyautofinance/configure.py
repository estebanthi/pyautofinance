from pyautofinance.common.config.configurator import Configurator


configurators_paths = ['.', './tests']

for path in configurators_paths:
    configurator = Configurator(path)
    configurator.create_config_file()
    configurator.create_folders()
