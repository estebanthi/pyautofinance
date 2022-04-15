import warnings
warnings.filterwarnings('ignore')

from pyautofinance.common.config.configurator import Configurator


def run(configurators_paths):
    for path in configurators_paths:
        configurator = Configurator(path)
        configurator.create_config_file()
        configurator.create_folders()


if __name__ == '__main__':
    configurators_paths = ['.']

    run(configurators_paths)
