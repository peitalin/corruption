
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from colors import brown, offwhite, grey, gold, darkblue, lightblue
from colors import line_styles, line_colors


# initialize plot variables, overwritten on 1st pass of simulation
ax1 = 1
ax2 = 1
ax3 = 1

# Trove KPIs influence a harvester's mood, causing the harvester battlemap to favor particular collections
# Trove KPIs influence weather in a harvester game format





## x-axis is hours
hours = []
# each frame is 1 hr
FRAMES = 1000

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
        base_rate = 6000
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
        self.y_claimable_corruption = {
            "total": []
        }
        self.y_claimed_corruption = {
            "total": []
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

        print("N : ", n)
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


    def addPrismEntryForHour(self, hour):
        # check entry exists, add if need be
        if hour not in self.y_dark_prisms.keys():
            self.y_dark_prisms[hour] = 0

        if hour not in self.y_prisms.keys():
            self.y_prisms[hour] = 0

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
        else:
            return None






def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


corrAccountant = CorruptionAccountant()


def simulation_fn(i):

    hour = i # each i-frame is 1 hr
    hours.append(hour)

    # clear plots to redraw
    ax1.clear()
    ax2.clear()
    ax3.clear()

    corrAccountant.emitCorruption(hour)
    corrAccountant.addPrismEntryForHour(hour)

    for k in corrAccountant.y_structures:

        corrAccountant.maybeRemoveCorruptionNTimes(hour, k)

        #### Plot 1 - corruption
        ax1.plot(
            hours,
            corrAccountant.y_corruption[k],
            alpha=0.5,
            label="{k}".format(k=k),
            color=line_colors[k],
        )


    ## Plot 2 - Prisms Burnt, and Dark Prisms created
    ax2.plot(
        hours,
        corrAccountant.y_prisms.values(),
        label="Prisms Burnt",
        color='royalblue',
        linestyle="--",
    )
    ax2.plot(
        hours,
        corrAccountant.y_dark_prisms.values(),
        label="Dark Prisms",
        color='crimson',
        linestyle="--",
    )
    ax2.set(xlabel='', ylabel='#Prisms and #Dark_Prisms')

    #### Plot 3 - Users MAGIC yield in the Mine (APR)
    ax3.plot(
        hours,
        corrAccountant.y_prisms_cumulative.values(),
        label="Total Prisms Burnt",
        color='royalblue',
        linestyle=":",
    )
    ax3.plot(
        hours,
        corrAccountant.y_dark_prisms_cumulative.values(),
        label="Total Dark Prisms Made",
        color='crimson',
        linestyle=":",
    )
    ax3.set(xlabel='hours', ylabel='#Prisms and #Dark_Prisms')

    ax1.set_title('Corruption in Buildings', size=10, color=gold)
    ax2.set_title('Prisms Burnt & Dark Prisms Created', size=10, color=gold)
    ax3.set_title('Cumulative Prisms & Dark Prisms', size=10, color=gold)

    ax1.legend(bbox_to_anchor=(1.3, 1.1), loc="upper right")
    ax2.legend(
        bbox_to_anchor=(1.2, 0.5),
        loc="lower center",
    )
    ax3.legend(bbox_to_anchor=(1.2, 0.5), loc="lower center")







def run_corruption_simulation():

    global fig
    global ax1
    global ax2
    global ax3

    # fig, (ax1, ax2, ax3) = plt.subplots(3, facecolor=darkblue)
    # fig.suptitle(''.format(), color=gold)

    fig, (ax1, ax2, ax3) = plt.subplots(3)
    fig.suptitle(''.format())
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        simulation_fn,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.3)
    # ax2.set_facecolor(lightblue)
    # ax3.set_facecolor(lightblue)

    plt.show()


run_corruption_simulation()





