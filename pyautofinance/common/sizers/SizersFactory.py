from dataclasses import dataclass, field
import backtrader as bt


@dataclass
class Sizer:
    sizer: bt.Sizer
    parameters: dict = field(default_factory=dict)


class SizersFactory:

    def make_sizer(self, sizer, **kwargs):
        return Sizer(sizer, kwargs)

