## Basic Overview

Build and test trading systems. Once you found something satisfying, go live with it automatically. Be notified on Telegram about what's happening while live trading.

PyAutoFinance is an upgrade of [binance-trading-bot](https://github.com/estebanthi/binance-trading-bot) with more features and generalized to any broker or exchange providing an API.

## Visualize the results

![](https://zupimages.net/up/21/45/dnis.png)

## Key features

* **Develop** trading components easily :
  * Strategies : to decide whether to enter / exit a trade or not.
  * Indicators : to give information about data to your strategies.
  * Analyzers : to analyze the results of your backtests or trading sessions.
  * Sizers : to define how much quantity of assets the engine should buy depending on parameters.
  * Observers : to define what you plot on the results chart.
  * Timers : to define actions to do at a precise time, repeatedly or not.
* **Test** your strategies through any testing process you wish : split train/test testing, walk forward testing, Monte-Carlo simulation, etc...
* **Optimize** your strategies parameters to find the more appropriate to a market, or a ticker.
* **Visualize** the results on a chart you can configure.
* Automatic **live trading** with fake or real money, using any API you want.
* **Telegram** configuration to get information about what is happening within your scripts.
* **Advanced features** : develop your own data sources, write your data anywhere you want, etc...

## How to install

```
# clone the repo
git clone https://github.com/estebanthi/PyAutoFinance

# go to folder
cd PyAutoFinance/pyautofinance

# install requirements
pip3 install -r requirements.txt
pip3 install git+https://github.com/Dave-Vallance/bt-ccxt-store.git
```

Go into `backtrader` package, in folder `plot`, open file `locator.py`, and remove warnings in line 35, because it is deprecated :

```python
from matplotlib.dates import (HOURS_PER_DAY, MIN_PER_HOUR, SEC_PER_MIN,
                              MONTHS_PER_YEAR, DAYS_PER_WEEK,
                              SEC_PER_HOUR, SEC_PER_DAY,
                              num2date, rrulewrapper, YearLocator,
                              MicrosecondLocator, warnings) # Remove warnings here
```

Go into `ccxt` package, in `binance.py`, and add at line 2723 :

```python
                request['stopPrice'] = self.price_to_precision(symbol, stopPrice)

        params = {}  # Add this
        response = getattr(self, method)(self.extend(request, params))
```

## How to use

To use the package, just go in the folder ```pyautofinance``` and create your first run script, or edit the one already existing. But first, you have to create the ```config.yml``` file.

### Create and configure the config file

First, create a ```config.yml``` in the `pyautofinance` file. Fill it like the following :

```yaml
datasets_pathname: "<FOLDER WHERE YOU WANT TO SAVE YOUR DATASETS>"

# If you want to use Telegram
telegram_token: "<YOUR TELEGRAM BOT TOKEN>"
user: "<YOUR TELEGRAM USER ID>"


# If you want to use live trading
BROKER_NAME_api_key: "<YOUR BROKER'S API KEY>"
BROKER_NAME_api_secret: "<YOUR BROKER'S API SECRET>"


# Example for Binance
binance_api_key: "AZERTYUIOPazertyuiop"
binance_api_secret: "azertyuiopAZERTYUIOP"
```

If you don't know how to get a Telegram token, you can check it on https://sendpulse.com/knowledge-base/chatbot/create-telegram-chatbot.

## Develop !

If you want to use the bot the best way, you will have to develop strategies, indicators, analyzers, ... First, you have to understand the ```backtrader``` python library, because everything operates around this. Find the documentation here : https://www.backtrader.com/docu/.

## Multiple strategies

Running multiple strategies at once is not fully supported, so prefer not to do this.

## To Do

- [ ] Walk-forward tester
- [ ] Monte-Carlo simulator
- [ ] Performance reports
- [ ] More plotting options
