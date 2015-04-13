from engine.src.trading.trade_offer import *

from engine.src.card.development_card import KnightCard
from engine.src.card.development_card import VictoryPointCard
from engine.src.card.development_card import MonopolyCard
from engine.src.card.development_card import RoadBuildingCard
from engine.src.card.development_card import YearOfPlentyCard


# TODO: Improve Config structure. Normalize across classes.
# TODO: Config-DevCards ripe for circular import errors.
class Config(object):
    # Game
    POINTS_TO_WIN = 10
    DEFAULT_PLAYER_COUNT = 3

    # GameBoard
    DEFAULT_TILE_COUNT = 19

    # Bank
    DEFAULT_RATIO_TRADE_INPUT_COUNT = 4
    DEFAULT_RATIO_TRADE_OUTPUT_COUNT = 1

    DEFAULT_DEVELOPMENT_CARD_ALLOCATION = {
        KnightCard: 14,
        VictoryPointCard: 5,
        MonopolyCard: 2,
        RoadBuildingCard: 2,
        YearOfPlentyCard: 2
    }

    # TradeCriteria
    TWO_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 2},
                                {TradeMetaCriteria.ANY: 1})

    THREE_FOR_ONE = TradeCriteria({}, {}, {TradeMetaCriteria.SAME: 3},
                                  {TradeMetaCriteria.ANY: 1})


