
import numpy as np



class CorruptionAccountant:
    """ Corruption minting/breaking accounting history object """


    def __init__(self):
        self.max_corruption = 1_000_000
        self.y_structures = [
            "questing",
            "crafting",
            "summoning",
            "forbidden_crafts",
            # "smolvasion",
            # "bridgehammer",
            'h1',
            'h2',
            'h3',
            'h4',
            'h5',
            'h6',
            'h7',
            'h8',
            'h9',
        ]
        self.y_corruption = {
            "questing": [],
            "crafting": [],
            "summoning": [],
            "forbidden_crafts": [],
            'h1': [],
            'h2': [],
            'h3': [],
            'h4': [],
            'h5': [],
            'h6': [],
            'h7': [],
            'h8': [],
            'h9': [],
        }
        # base rate per hour
        base_rate = 4000
        self.corruption_rate = {
            "questing": base_rate,
            "crafting": base_rate,
            "summoning": base_rate,
            "forbidden_crafts": base_rate,
            'h1': base_rate/3,
            'h2': base_rate/3,
            'h3': base_rate/3,
            'h4': base_rate/3,
            'h5': base_rate/3,
            'h6': base_rate/3,
            'h7': base_rate/3,
            'h8': base_rate/3,
            'h9': base_rate/3,
        }
        # Each time you remove corruption, you remove 4000 corruption.
        # So this requires 1 Prism per building per hour.

        # For Questing, Summoning, Crafting, 3x Harvesters, this equals:
        # • 4 prisms per hour:
        # • 96 Prisms/day
        # • 672 Prisms/week.

        # Each Prism crafted breaks an expected 0.61 T5 Treasure.

        # This is equal to:
        # • ~410 T5 Treasures/week
        # • ~5k T5 Fragments/week

        # Which is roughly equal to all T5 fragments emitted once the capped Treasure emissions are in place (20k/month)

        self.amount_corruption_removed = {
            "questing": 4000,
            "crafting": 4000,
            "summoning": 4000,
            "forbidden_crafts": 4000,
            'h1': 4000,
            'h2': 4000,
            'h3': 4000,
            'h4': 4000,
            'h5': 4000,
            'h6': 4000,
            'h7': 4000,
            'h8': 4000,
            'h9': 4000,
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
        self.y_cumulative_crafted_corruption = {
            0: 0,
        }


    def getCorruptionLevel(self, c):
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


    def getDarkPrismDropRate(self, c):
        cLevel = self.getCorruptionLevel(c)
        if cLevel == 6:
            return 0.5
        if cLevel == 5:
            return 0.35
        if cLevel == 4:
            return 0.25
        if cLevel == 3:
            return 0.15
        if cLevel == 2:
            return 0.1
        if cLevel == 1:
            return 0.05
        else:
            return 0


    def getNumTimesTryRemoveCorruption(self, c):
        cLevel = self.getCorruptionLevel(c)
        base_rate = 1
        n = base_rate
        ## this is an assumption, for simulation purposes only
        if cLevel == 6:
            n = base_rate * 6
        elif cLevel == 5:
            n = base_rate * 5
        elif cLevel == 4:
            n = base_rate * 4
        elif cLevel == 3:
            n = base_rate * 3
        elif cLevel == 2:
            n = base_rate * 2
        elif cLevel == 1:
            n = base_rate * 1
        else:
            n = base_rate
        return n


    def emitCorruption(self, hour, initial_corruption_balance=90_000):
        # 1800 a hour = 302_400 a week per building
        for k in self.y_structures:

            if hour == 0:
                rate = initial_corruption_balance
            else:
                rate = self.corruption_rate[k]

            if len(self.y_corruption[k]) > 0:
                prev_value = self.y_corruption[k][-1]
                self.y_corruption[k].append(prev_value + rate)
            else:
                self.y_corruption[k].append(rate)


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
        PR_REMOVE_CORRUPTION = 0.5
        # PR_REMOVE_CORRUPTION = 1
        current_corruption = self.y_corruption[k][hour]
        # do this x times, depending on how high corruption is
        ntimes = self.getNumTimesTryRemoveCorruption(current_corruption)
        randScores = [np.random.uniform(0,100) for x in range(ntimes)]

        for score in randScores:
            if current_corruption <= 20_000:
                break
            else:
                if score < (PR_REMOVE_CORRUPTION * 100):
                    self._removeCorruption(k)
                    self.maybeDropDarkPrism(hour, current_corruption)


    def forgeCorruption(self, hour, legionType="gen0_common"):

        percentForgedByLegion = {
            'gen0_1_1': 0.07, # 1/1 7%
            'gen0_rare': 0.03, # all-class 3%
            'gen0_uncommon': 0.02, # Assasin etc 2%
            'gen0_special': 0.0175, # includes riverman, Numeraire 1.75%
            'gen0_common': 0.015, # commons 1.5%
            'gen1_rare': 0.01, # 1.1%
            'gen1_uncommon': 0.0105, # 1.05%
            'gen1_common': 0.01, # 1%
        }

        percentForgeable = percentForgedByLegion[legionType]

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
                self.y_cumulative_crafted_corruption[hour] += amountForged


    def addAccountingEntriesForHour(self, hour):
        # check entry exists, add if need be

        # time-series
        if hour not in self.y_dark_prisms.keys():
            self.y_dark_prisms[hour] = 0

        if hour not in self.y_prisms.keys():
            self.y_prisms[hour] = 0

        if hour not in self.y_forgeable_corruption.keys():
            self.y_forgeable_corruption[hour] = 0

        if hour not in self.y_crafted_corruption.keys():
            self.y_crafted_corruption[hour] = 0

        # cumulative time-series
        if hour not in self.y_cumulative_crafted_corruption.keys():
            if hour == 0:
                self.y_cumulative_crafted_corruption[hour] = 0
            else:
                self.y_cumulative_crafted_corruption[hour] = self.y_cumulative_crafted_corruption[hour-1]

        if hour not in self.y_dark_prisms_cumulative.keys():
            if hour == 0:
                self.y_dark_prisms_cumulative[hour] = 0
            else:
                self.y_dark_prisms_cumulative[hour] = self.y_dark_prisms_cumulative[hour-1]

        if hour not in self.y_prisms_cumulative.keys():
            if hour == 0:
                self.y_prisms_cumulative[hour] = 0
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

            self.forgeCorruption(hour)
        else:
            # no Dark Prism created from Prism, skip
            return None



