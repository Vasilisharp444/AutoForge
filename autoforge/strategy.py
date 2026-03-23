"""Strategy base class — all AutoForge strategies extend this."""

from abc import ABC, abstractmethod


class Context:
    """Passed to on_bar() — provides bar data, indicators, position state, and order methods."""

    __slots__ = (
        "bar", "ind", "position", "entry_price", "bars_in_trade",
        "bar_index", "_pending_orders",
    )

    def __init__(self):
        self.bar = None              # Current bar: dict with Open, High, Low, Close, Volume, DateTime
        self.ind = {}                # Indicator values at current bar: {name: value}
        self.position = 0            # 1 = long, -1 = short, 0 = flat
        self.entry_price = 0.0       # Price of current position entry
        self.bars_in_trade = 0       # Bars since entry
        self.bar_index = 0           # Current index in the data
        self._pending_orders = []

    def buy(self, order_type="market", price=None):
        """Go long (or close short and go long)."""
        self._pending_orders.append(("buy", order_type, price))

    def sell(self, order_type="market", price=None):
        """Close long position."""
        self._pending_orders.append(("sell", order_type, price))

    def short(self, order_type="market", price=None):
        """Go short (or close long and go short)."""
        self._pending_orders.append(("short", order_type, price))

    def cover(self, order_type="market", price=None):
        """Close short position."""
        self._pending_orders.append(("cover", order_type, price))


class Strategy(ABC):
    """Base class for all AutoForge strategies.

    Subclasses define:
        params: dict of {name: default_value} — optimizer overrides these
        indicators(): returns dict of indicator configs
        on_bar(ctx): called for each bar to generate signals
    """

    params = {}

    def __init__(self, **kwargs):
        self._params = {**self.params}
        for k, v in kwargs.items():
            if k in self._params:
                self._params[k] = v
            else:
                raise ValueError(f"Unknown parameter: {k}")
        for k, v in self._params.items():
            setattr(self, k, v)

    @abstractmethod
    def indicators(self):
        """Declare indicators needed.

        Returns:
            dict of {name: (indicator_type, {param: value, ...})}

        Example:
            return {
                'sma_fast': ('sma', {'period': self.fast, 'source': 'Close'}),
                'bb_upper': ('bb_upper', {'period': 20, 'std': 2.0}),
            }
        """
        return {}

    @abstractmethod
    def on_bar(self, ctx):
        """Called for each bar after warm-up. Use ctx to read data and submit orders.

        Args:
            ctx: Context object with bar data, indicators, position state, and order methods.
        """
        pass

    def get_warmup(self):
        """Auto-detect warm-up period from indicator declarations."""
        indicators = self.indicators()
        if not indicators:
            return 0
        periods = []
        for _name, (_ind_type, params) in indicators.items():
            if "period" in params:
                periods.append(params["period"])
        return max(periods) if periods else 0
