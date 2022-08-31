
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation
import random


from colors import brown, offwhite, grey, gold, darkblue, lightblue
from colors import line_styles, line_colors


# initialize plot variables, overwritten on 1st pass of simulation
ax1 = 1
ax2 = 1
ax3 = 1

# Trove KPIs influence a harvester's mood, causing the harvester battlemap to favor particular collections
# Trove KPIs influence weather in a harvester game format

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

MAX_CORRUPTION = 1_000_000


def getDarkPrismDropRate(c):
    cLevel = getCorruptionLevel(c)
    if cLevel == 6:
        return 0.7
    if cLevel == 5:
        return 0.6
    if cLevel == 4:
        return 0.5
    if cLevel == 3:
        return 0.4
    if cLevel == 2:
        return 0.3
    if cLevel == 1:
        return 0.2
    else:
        return 0.2


def getNumTimesTryRemoveCorruption(c):
    cLevel = getCorruptionLevel(c)
    base_rate = 1
    if cLevel == 6:
        return base_rate * 64
    if cLevel == 5:
        return base_rate * 32
    if cLevel == 4:
        return base_rate * 16
    if cLevel == 3:
        return base_rate * 8
    if cLevel == 2:
        return base_rate * 4
    if cLevel == 1:
        return base_rate * 2
    else:
        return base_rate



y_structures = [
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

## Array of y-axis data points
y_corruption = {
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
corruption_rate = {
    "questing": base_rate,
    "crafting": base_rate,
    "summoning": base_rate,
    "forbidden_crafts": base_rate,
    'h1': base_rate,
    'h2': base_rate,
    'h3': base_rate,
    'h4': base_rate,
    'h5': base_rate,
    'h6': base_rate,
    'h7': base_rate,
    'h8': base_rate,
    'h9': base_rate,
}


amount_corruption_removed = {
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


y_prisms = {
    0: 0,
}

y_dark_prisms = {
    0: 0,
}

y_forged_corruption = {
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


## x-axis is days
days = []
# each frame is 1 hr
FRAMES = 1000

# class CorruptionAccountant:
#     """Corruptiong minting/breaking accounting history object """

#     def __init__(self):
#         # Balances for net treasures created and broken at a given point in time
#         self.created_treasures = {
#             't1': 0,
#             't2': 0,
#             't3': 0,
#             't4': 0,
#             't5': 0,
#         }
#         self.broken_treasures = {
#             't1': 0,
#             't2': 0,
#             't3': 0,
#             't4': 0,
#             't5': 0,
#         }


def emitCorruption():
    # 14_400 a day = 100_800 a week
    global y_corruption

    for k in y_structures:
        rate = corruption_rate[k]
        if len(y_corruption[k]) > 0:
            prev_value = y_corruption[k][-1]
            y_corruption[k].append(prev_value + rate)
        else:
            y_corruption[k].append(rate)


def _removeCorruption(k):
    global y_corruption
    prev_value = y_corruption[k][-1]
    y_corruption[k][-1] = prev_value - amount_corruption_removed[k]
    print('{} corruption level: {}'.format(k, y_corruption[k][-1]))


def maybeRemoveCorruption(day, corruption, k):
    PR_REMOVE_CORRUPTION = 0.5
    # do this x times, depending on how high corruption is
    for i in range(0, getCorruptionLevel(corruption)):

        score = np.random.uniform(0,100)
        if score < (PR_REMOVE_CORRUPTION * 100):
            return None
        else:
            _removeCorruption(k)
            maybeDropDarkPrism(day, corruption)


def addEntryForDay(day):
    # check entry exists, add if need be
    if day not in y_dark_prisms.keys():
        y_dark_prisms[day] = 0

    if day not in y_prisms.keys():
        y_prisms[day] = 0


def _createPrism(day=0, c=0):
    if day not in y_prisms.keys():
        y_prisms[day] = 1
    else:
        y_prisms[day] = y_prisms[day] + 1

def maybeDropDarkPrism(day=0, c=0):
    PR_DROP_DARK_PRISM = getDarkPrismDropRate(c)
    score = np.random.uniform(0,100)
    # first create a Prism
    _createPrism(day, c)
    # then roll to see if a dark prism is created, increment if so
    if score < (PR_DROP_DARK_PRISM * 100):
        if day not in y_dark_prisms.keys():
            y_dark_prisms[day] = 1
        else:
            y_dark_prisms[day] = y_dark_prisms[day] + 1
    else:
        return None
    # print(y_dark_prisms)



def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


def simulation_fn(i):

    day = i # each i-frame is 1 days
    days.append(day)

    # clear plots to redraw
    ax1.clear()
    ax2.clear()
    ax3.clear()

    emitCorruption()
    addEntryForDay(day)

    for k in y_structures:

        current_corruption = y_corruption[k][-1]
        maybeRemoveCorruption(day, current_corruption, k)

        #### Plot 1 - corruption
        ax1.plot(
            days,
            y_corruption[k],
            label="{k}".format(k=k),
            color=line_colors[k],
        )

        # ax2.plot(
        #     days,
        #     y_prisms[k],
        #     # label="Harvester {} {:.2f}x boost | Share {:.2%}".format(h.id + 1, current_boost, current_emissions_pct_share['emission_share']),
        #     # color=line_colors[h.id],
        #     # linestyle=line_styles[h.id],
        # )

        # ax2.plot(
        #     days,
        #     y_dark_prisms[k],
        #     # label='Harvester {} 1/{}m: {:.2%}% APR MAGIC'.format(h.id + 1, AUM_CAP_HARVESTER, current_user_magic_yield),
        #     # color=line_colors[h.id],
        # )

        # ax3.plot(
        #     days,
        #     y_forged_corruption[k],
        #     # label='Harvester {} 1/{}m: {:.2%}% APR MAGIC'.format(h.id + 1, AUM_CAP_HARVESTER, current_user_magic_yield),
        #     # color=line_colors[h.id],
        # )



    # ### Atlas Boosts
    # #### Plot 1 - Harvester Boosts
    # ax1.plot([], label="Atlas with {}x default boost (configurable)".format(ATLAS_MINE_BONUS), color='red')
    # ax1.set(xlabel='', ylabel='Boost Multiplier')

    ## Plot 2 - Dark Prisms created

    ax2.plot(
        days,
        y_prisms.values(),
        label="Prisms",
        color='royalblue',
        linestyle="--",
    )

    ax2.plot(
        days,
        y_dark_prisms.values(),
        label="Dark Prisms",
        color='crimson',
        linestyle="--",
    )
    ax2.set(xlabel='', ylabel='#Dark Prisms')

    # # plot 2 y-ticks
    # yticks_pct = [0, 0.2, 0.4, 0.6, 0.8, 1]
    # yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    # ax2.set_yticks(yticks_pct, color=gold)
    # ax2.set_yticklabels(yticks_label, fontsize=7, color=gold)

    # #### Plot 3 - Users MAGIC yield in the Mine (APR)
    # ax3.plot(
    #     days,
    #     y_user_magic_yield['atlas'],
    #     # label='Atlas: 1m/{:.0f}m: {:.2%}% APR MAGIC'.format(expected_atlas_aum, atlas_user_magic_yield),
    #     # color='crimson',
    #     # linestyle="--",
    # )
    # # plot 3 y-ticks
    # yticks_pct = [0, 0.5, 1, 1.5, 2]
    # yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    # ax3.set_yticks(yticks_pct, color=gold)
    # ax3.set_yticklabels(yticks_label, fontsize=7, color=gold)

    ax1.set_title('Corruption', size=10)
    # ax2.set_title('', size=10, color=gold)
    # ax3.set_title('', size=10, color=gold)

    # ax2.set_ylabel('', color=gold)
    # ax2.set_xlabel('', color=gold)

    # ax3.set_ylabel('', color=gold)
    # ax3.set_xlabel('day {}'.format(day), color=gold)

    # # ax1.grid(color='black', alpha=0.1)
    # ax2.grid(color=gold, alpha=0.1)
    # ax3.grid(color=gold, alpha=0.1)

    # ax2.spines['bottom'].set_color(gold)
    # ax2.spines['top'].set_color(gold)
    # ax2.spines['left'].set_color(gold)
    # ax2.spines['right'].set_color(gold)
    # ax2.xaxis.label.set_color(gold)
    # ax2.tick_params(axis='x', colors=gold)
    # ax2.tick_params(axis='y', colors=gold)

    # ax3.spines['bottom'].set_color(gold)
    # ax3.spines['top'].set_color(gold)
    # ax3.spines['left'].set_color(gold)
    # ax3.spines['right'].set_color(gold)
    # ax3.xaxis.label.set_color(gold)
    # ax3.tick_params(axis='x', colors=gold)
    # ax3.tick_params(axis='y', colors=gold)

    ax1.legend(bbox_to_anchor=(1.3, 1.1), loc="upper right")
    ax2.legend(
        bbox_to_anchor=(1.2, 0.5),
        loc="lower center",
        # labelcolor=grey,
        # edgecolor=darkblue,
        # facecolor=darkblue
    )

    # ax3.legend(bbox_to_anchor=(1.47, 1), loc="lower center",
    #     labelcolor=grey,
    #     edgecolor=darkblue,
    #     facecolor=darkblue
    # )







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





