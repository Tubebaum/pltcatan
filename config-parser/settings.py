import sys
sys.path.append('.')
import config

class Resource(object):
    def __init__(self):
        self.count = 0
        self.card = None
        self.name = None

    def setResource(self, resource):
        for k, v in resource.iteritems():
            if k == 'count':
                self.count = int(v)
            elif k == 'card':
                self.card = v
            elif k == 'name':
                self.name = v.strip('"')

class Exchange(object):
    def __init__(self):
        self.buy = None
        self.buyCount = 0
        self.sell = None
        self.sellCount = None

class Tile(object):
    def __init__(self):
        self.name = None
        self.resource = None
        self.allowExchange = None
        self.maxOnBoard = 0

    def setResource(self, resource):
        self.resource = Resource()
        self.resource.setResource(resource)

    def setExchange(self, exchange):
        self.exchange = Exchange()
        for k, v in exchange.iteritems():
            if k == 'buy':
                for k1, v1 in v.iteritems():
                    if k1 == 'card':
                        self.exchange.buy = v1
                    elif k1 == 'count':
                        self.exchange.buyCount = v1
            if k == 'sell':
                for k1, v1 in v.iteritems():
                    if k1 == 'card':
                        self.exchange.sell = v1
                    elif k1 == 'count':
                        self.exchange.sellCount = v1

class Chits(object):
    def __init__(self):
        self.distribution = 'uniform'
        self.types = []

class Tiles(object):
    def __init__(self):
        self.distribution = 'uniform'
        self.types = []

class DevelopmentCard(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.maxCount = None
        self.pointReward = 0
        self.effects = None

    def setDevelopmentCard(self, name, developmentCard):
        self.name = name
        for k, v in developmentCard.iteritems():
            if k == 'description': 
                self.description = v.strip('"')
            elif k == 'max-count':
                self.maxCount = int(v)
            elif k == 'point-reward':
                self.pointReward = int(v)
            elif k == 'effect':
                self.effects = Effects()
                self.effects.setEffects(v)

class SpecialCard(object):
    def __init__(self):
        self.name = None
        self.description = None
        self.maxCount = 0
        self.pointReward = 0
        self.criteria = None

    def setSpecialCard(self, name, specialCard):
        self.name = name
        for k, v in specialCard.iteritems():
            if k == 'description':
                self.description = v.strip('"')
            elif k == 'max-count':
                self.maxCount = int(v)
            elif k == 'point-reward':
                self.pointReward = int(v)
            elif k == 'criteria':
                self.criteria = v

class Cards(object):
    def __init__(self):
        self.developmentCards = {}
        self.developmentCost = []
        self.resource = []
        self.specialCards = {}

    def setDevelopmentCards(self, developmentCards):
        for k, v in developmentCards.iteritems():
            developmentCard = DevelopmentCard()
            developmentCard.setDevelopmentCard(k, v)
            self.developmentCards[k] = developmentCard

    def setDevelopmentCost(self, developmentCost):
        for k in developmentCost:
            resource = Resource()
            resource.setResource(k)
            self.developmentCost.append(resource)

    def setResource(self, resources):
        for k in resources:
            resource = Resource()
            resource.setResource(k)
            self.resource.append(k)

    def setSpecial(self, special):
        for k, v in special.iteritems():
            specialCard = SpecialCard()
            specialCard.setSpecialCard(k, v)
            self.specialCards[k] = specialCard

class Effects(object):
    def __init__(self):
        self.onRoll = None
        self.whenPlayed = None

    def setEffects(self, effects):
        for k, v in effects.iteritems():
            if k == 'on-roll':
                self.onRoll = v
            elif k == 'when-played':
                self.whenPlayed = v

class Constraints(object):
    def __init__(self):
        self.placementType = None
        self.adjacentTo = []
        self.notAdjacentTo = []

    def setConstraints(self, constraints):
        for k, v in constraints.iteritems():
            if k == 'placement-type':
                self.placementType = v.strip('"')
            elif k == 'adjacent-to':
                for k1 in v:
                    self.adjacentTo.append(k1)
            elif k == 'notAdjacentTo':
                for k1 in v:
                    self.notAdjacentTo.append(k1)

class BuildingCost(object):
    def __init__(self):
        self.costs = []

    def setBuildingCost(self, buildingCost):
        for k in buildingCost:
            resource = Resource()
            resource.setResource(k)
            self.costs.append(resource)

class Structure(object):
    def __init__(self):
        self.name = None
        self.maxCountPerPlayer = 0
        self.victoryPointValue = 0
        self.upgradeOf = None
        self.buildingCost = None
        self.constraints = None
        self.effects = None

    def setStructure(self, name, structure):
        self.name = name
        for k, v in structure.iteritems():
            if k == 'max-count-per-player':
                self.maxCountPerPlayer = int(v)
            elif k == 'victory-point-value':
                self.victoryPointValue = int(v)
            elif k == 'upgrade-of':
                self.upgradeOf = v
            elif k == 'building-cost':
                self.buildingCost = BuildingCost()
                self.buildingCost.setBuildingCost(v)
            elif k == 'constraints':
                self.constraints = Constraints()
                self.constraints.setConstraints(v)
            elif k == 'effects':
                self.effects = Effects()
                self.effects.setEffects(v)

class Structures(object):
    def __init__(self):
        self.playerBuilt = {}

    def setPlayerBuilt(self, playerBuilt):
        for k, v in playerBuilt.iteritems():
            structure = Structure()
            structure.setStructure(k, v)
            self.playerBuilt[k] = structure

class Board(object):
    def __init__(self):
        self.radius = 0

    def setChits(self, chits):
        self.chits = Chits()
        for k, v in chits.iteritems():
            if k == 'distribution':
                self.chits.distribution = v
            elif k == 'types':
                for n in v:
                    self.chits.types.append(int(n))

    def setTiles(self, tiles):
        self.tiles = Tiles()
        for k, v in tiles.iteritems():
            if k == 'distribution':
                self.chits.distribution = v
            elif k == 'types':
                for n in v:
                    tile = Tile()
                    for k1, v1 in n.iteritems():
                        if k1 == 'name':
                            tile.name = v1.strip('"')
                        elif k1 == 'resource':
                            tile.setResource(v1)
                        elif k1 == 'allow-exchange':
                            tile.setExchange(v1)
                    self.tiles.types.append(tile)

class Game(object):
    def __init__(self):
        self.pointsToWin = 0

    def setCards(self, cards):
        self.cards = Cards()
        for k, v in cards.iteritems():
            if k == 'development':
                self.cards.setDevelopmentCards(v)
            elif k == 'development-cost':
                self.cards.setDevelopmentCost(v)
            elif k == 'resource':
                self.cards.setResource(v)
            elif k == 'special':
                self.cards.setSpecial(v)

    def setStructures(self, structures):
        self.structures = Structures()
        for k, v in structures.iteritems():
            if k == 'player-built':
                self.structures.setPlayerBuilt(v)

    def setBoard(self, board):
        self.board = Board()
        for k, v in board.iteritems():
            if k == 'radius':
                self.board.radius = 3
            elif k == 'chits':
                self.board.setChits(v)
            elif k == 'tiles':
                self.board.setTiles(v)

class Settings(object):
    def __init__(self, file='default.skit'):
        self.skit = config.parser.parse(open(file, 'r').read())
        for k, v in self.skit.iteritems():
            if k == 'game':
                self.setGame(v)

    def setGame(self, game):
        self.game = Game()
        for k, v in game.iteritems():
            if k == 'points-to-win':
                self.game.pointsToWin = v
            elif k == 'cards':
                self.game.setCards(v)
            elif k == 'structures':
                self.game.setStructures(v)
            elif k == 'board':
                self.game.setBoard(v)
