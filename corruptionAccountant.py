
import numpy as np
from parameters import corruption_rate, amount_corruption_removed, dark_prism_drop_rates
from parameters import percent_corr_forged_by_legion, harvester_age, default_initial_balances
from parameters import initial_corruption_balances, harvester_list


class CorruptionAccountant:
    """ Corruption minting/breaking accounting history object """


    def __init__(self):
        self.max_corruption = 1_000_000
        self.y_structures = [
            "questing",
            "crafting",
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'h7',
        ]
        self.y_corruption = {
            "questing": [],
            "crafting": [],
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': [],
            'h7': [],
        }
        self.corruption_rate = corruption_rate

        self.amount_corruption_removed = amount_corruption_removed

        self.y_harvester_dmg = {
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': [],
            'h7': [],
        }

        self.y_prisms = {
            0: 0,
        }
        self.y_dark_prisms = {
            0: 0,
        }
        self.y_prisms_cumulative = {
            0: 0,
        }
        self.y_dark_prisms_cumulative = {
            0: 0,
        }
        self.y_forgeable_corruption = {
            0: 0,
        }
        self.y_crafted_corruption = {
            0: 0,
        }
        self.y_total_circulating_corruption = {
            0: 0,
        }


    def getDarkPrismDropRate(self, c):
        cLevel = getCorruptionLevel(c)
        if cLevel <= 6:
            return dark_prism_drop_rates[cLevel]
        else:
            return dark_prism_drop_rates[6]



    def emitCorruption(self, hour):
        # 1800 a hour = 302_400 a week per building
        for k in self.y_structures:

            rate = self.corruption_rate[k]

            if len(self.y_corruption[k]) > 0:
                prev_value = self.y_corruption[k][-1]
                if prev_value <= 1_000_000:
                    self.y_corruption[k].append(prev_value + rate)
            else:
                self.y_corruption[k].append(initial_corruption_balances[k])


    def emitForgeableCorruption(self, hour, rate=8000):
        if hour == 0:
            prev_value = 0
        else:
            prev_value = self.y_forgeable_corruption[hour-1]
        self.y_forgeable_corruption[hour] = prev_value + rate


    def _removeCorruption(self, k):
        prev_value = self.y_corruption[k][-1]
        self.y_corruption[k][-1] = prev_value - self.amount_corruption_removed[k]
        # print('{} corruption level: {}'.format(k, self.y_corruption[k][-1]))


    def maybeRemoveCorruptionNTimes(self, hour, k):

        if isHarvester(k):
            PR_REMOVE_CORRUPTION = 0.2
        else:
            PR_REMOVE_CORRUPTION = 0.1

        current_corruption = self.y_corruption[k][hour]
        # do this x times, depending on how high corruption is
        ntimes = getNumTimesTryRemoveCorruption(current_corruption)
        randScores = drawProbabilities(ntimes)

        for score in randScores:
            if current_corruption <= 20_000:
                break
            else:
                if score < (PR_REMOVE_CORRUPTION * 100):
                    self._removeCorruption(k)
                    self.maybeDropDarkPrism(hour, current_corruption)


    def forgeCorruption(self, hour, legionType="gen0_common"):

        percentForgeable = percent_corr_forged_by_legion[legionType]

        if hour not in self.y_forgeable_corruption.keys():
            print("hour entry not in y_forgeable_corruption")
            return
        else:
            if hour not in self.y_crafted_corruption.keys():
                self.y_crafted_corruption[hour] = 0
            else:
                totalAmountForgeable = self.y_forgeable_corruption[hour]
                amountForged = percentForgeable * totalAmountForgeable

                self.y_forgeable_corruption[hour] -= amountForged
                self.y_crafted_corruption[hour] += amountForged
                self.y_total_circulating_corruption[hour] += amountForged


    def addAccountingEntriesForHour(self, hour):
        # check entry exists, add if need be

        # time-series
        if hour not in self.y_dark_prisms.keys():
            self.y_dark_prisms[hour] = default_initial_balances["y_dark_prisms"]

        if hour not in self.y_prisms.keys():
            self.y_prisms[hour] = default_initial_balances["y_prisms"]

        if hour not in self.y_forgeable_corruption.keys():
            self.y_forgeable_corruption[hour] = default_initial_balances["y_forgeable_corruption"]

        if hour not in self.y_crafted_corruption.keys():
            self.y_crafted_corruption[hour] = default_initial_balances["y_crafted_corruption"]

        # cumulative time-series
        if hour not in self.y_total_circulating_corruption.keys():
            if hour == 0:
                self.y_total_circulating_corruption[hour] = default_initial_balances["y_total_circulating_corruption"]
            else:
                self.y_total_circulating_corruption[hour] = self.y_total_circulating_corruption[hour-1]

        if hour not in self.y_dark_prisms_cumulative.keys():
            if hour == 0:
                self.y_dark_prisms_cumulative[hour] = default_initial_balances["y_dark_prisms_cumulative"]
            else:
                self.y_dark_prisms_cumulative[hour] = self.y_dark_prisms_cumulative[hour-1]

        if hour not in self.y_prisms_cumulative.keys():
            if hour == 0:
                self.y_prisms_cumulative[hour] = default_initial_balances["y_prisms_cumulative"]
            else:
                self.y_prisms_cumulative[hour] = self.y_dark_prisms_cumulative[hour-1]


    def _createPrism(self, hour=0, c=0):
        if hour not in self.y_prisms.keys():
            self.y_prisms[hour] = 1
        else:
            self.y_prisms[hour] = self.y_prisms[hour] + 1

        if hour not in self.y_prisms_cumulative.keys():
            self.y_prisms_cumulative[hour] = self.y_prisms_cumulative[hour-1] + 1
        else:
            self.y_prisms_cumulative[hour] = self.y_prisms_cumulative[hour] + 1


    def maybeDropDarkPrism(self, hour=0, c=0):
        PR_DROP_DARK_PRISM = self.getDarkPrismDropRate(c)
        score = np.random.uniform(0,100)
        # first create a Prism
        self._createPrism(hour, c)
        # then roll to see if a dark prism is created, increment if so
        if score < (PR_DROP_DARK_PRISM * 100):
            if hour not in self.y_dark_prisms.keys():
                self.y_dark_prisms[hour] = 1
                self.y_dark_prisms_cumulative[hour] = 1
            else:
                self.y_dark_prisms[hour] = self.y_dark_prisms[hour] + 1
                self.y_dark_prisms_cumulative[hour] = self.y_dark_prisms_cumulative[hour] + 1

            # Forge Corruption is Dark prism created
            self.forgeCorruption(hour)
            # Then maybe use Corruption against other harvesters
            self.maybeCastCorruption(hour)
        else:
            # no Dark Prism created from Prism, skip
            return None


    def calcHarvestersDmg(self, hour=0):
        # check corruption level for a building
        # incrementa dmg based on corruption level every tick
        for k in self.y_structures:
            if isHarvester(k):
                if hour == 0:
                    dmg_amount = 0
                else:
                    current_corruption = self.y_corruption[k][hour]
                    cLevel = getCorruptionLevel(current_corruption)
                    dmg_amount = getDmgAmount(cLevel, k)

                if len(self.y_harvester_dmg[k]) == 0:
                    self.y_harvester_dmg[k].append(dmg_amount)
                else:
                    prev_value = self.y_harvester_dmg[k][-1]
                    self.y_harvester_dmg[k].append(prev_value + dmg_amount)


    def maybeCastCorruption(self, hour=0):

        randomHarvester = drawRandomHarvester()
        currentCirculatingCorruption = self.y_total_circulating_corruption[hour]

        if currentCirculatingCorruption > castCorruptionParameters['high']['corruption_level']:
            maybeCastCorruption = np.random.uniform(0, 1) < castCorruptionParameters['high']['cast_probability']
            sendCorruption = castCorruptionParameters['high']['amt_corruption']

        elif currentCirculatingCorruption > castCorruptionParameters['medium']['corruption_level']:
            maybeCastCorruption = np.random.uniform(0, 1) < castCorruptionParameters['medium']['cast_probability']
            sendCorruption = castCorruptionParameters['high']['amt_corruption']

        elif currentCirculatingCorruption > castCorruptionParameters['low']['corruption_level']:
            maybeCastCorruption = np.random.uniform(0, 1) < castCorruptionParameters['low']['cast_probability']
            sendCorruption = castCorruptionParameters['high']['amt_corruption']
        else:
            maybeCastCorruption = False
            sendCorruption = 0

        # add some randomness
        sendCorruption = round(np.random.uniform(1, 1.5) * sendCorruption)

        if maybeCastCorruption:
            self.y_total_circulating_corruption[hour] -= sendCorruption
            self.y_corruption[randomHarvester][-1] += sendCorruption



castCorruptionParameters = {
    # low corruption levels
    "low": {
        "corruption_level": 1_000_000,
        "amt_corruption": 50_000,
        "cast_probability": 0.05,
    },
    # medium corruption levels
    "medium": {
        "corruption_level": 1_500_000,
        "amt_corruption": 200_000,
        "cast_probability": 0.1,
    },
    # high corruption levels
    "high": {
        "corruption_level": 2_000_000,
        "amt_corruption": 400_000,
        "cast_probability": 0.5,
    },
}



def drawRandomHarvester():
    return harvester_list[np.random.randint(0, 7)]


def drawProbabilities(ntimes=1):
    return [np.random.uniform(0,100) for x in range(ntimes)]


def isHarvester(k):
    return k in harvester_list


def getDmgAmount(cLevel, harvester):

    ## only for harvesters
    age = harvester_age[harvester]
    h = age * 2

    if cLevel == 6:
        n = 12 * h
    elif cLevel == 5:
        n = 10 * h
    elif cLevel == 4:
        n = 8 * h
    elif cLevel == 3:
        n = 6 * h
    elif cLevel == 2:
        n = 4 * h
    elif cLevel == 1:
        n = 2 * h
    else:
        n = 1 * h
    return n

def getCorruptionLevel(c):
    if c > 600_000:
        return 6
    elif c > 500_000:
        return 5
    elif c > 400_000:
        return 4
    elif c > 300_000:
        return 3
    elif c > 200_000:
        return 2
    elif c > 100_000:
        return 1
    else:
        return 0


def getNumTimesTryRemoveCorruption(c, k='harvester'):
    cLevel = getCorruptionLevel(c)
    n = 1
    ## this is an assumption, for simulation purposes only
    if isHarvester(k):
        if cLevel == 6:
            n = 12
        elif cLevel == 5:
            n = 8
        elif cLevel == 4:
            n = 6
        elif cLevel == 3:
            n = 4
        elif cLevel == 2:
            n = 2
        elif cLevel == 1:
            n = 1
        else:
            n = 0
    else:
        if cLevel == 6:
            n = 6
        elif cLevel == 5:
            n = 5
        elif cLevel == 4:
            n = 4
        elif cLevel == 3:
            n = 3
        elif cLevel == 2:
            n = 2
        elif cLevel == 1:
            n = 1
        else:
            n = 0

    return n