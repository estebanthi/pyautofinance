from dataclasses import dataclass, field
import backtrader as bt


@dataclass
class Analyzer:
    analyzer: bt.Analyzer
    parameters: dict = field(default_factory=dict)


class AnalyzersFactory:

    def make_analyzer(self, analyzer, **kwargs):
        return Analyzer(analyzer, kwargs)

