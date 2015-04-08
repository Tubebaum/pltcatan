from engine.src.trading.trade_offer import *


# TODO: Improve Config structure. Normalize across classes.
class Config(object):
    # GameBoard
    DEFAULT_TILE_COUNT = 19

    # Bank
    DEFAULT_RATIO_TRADE_INPUT_COUNT = 4
    DEFAULT_RATIO_TRADE_OUTPUT_COUNT = 1

    # TradeCriteria
    TWO_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 2},
                                {TradeMetaCriteria.ANY: 1})

    THREE_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 3},
                                  {TradeMetaCriteria.ANY: 1})


