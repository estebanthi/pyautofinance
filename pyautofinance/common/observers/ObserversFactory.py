from dataclasses import dataclass, field
import backtrader as bt


@dataclass
class Observer:
    analyzer: bt.Observer
    parameters: dict = field(default_factory=dict)


class ObserversFactory:

    def make_observer(self, observer, **kwargs):
        return Observer(observer, kwargs)

