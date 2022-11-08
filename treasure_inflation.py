import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from styles import colors

## setup CappedTreasureEmissions mechanism
## run simulations with vairous parameters


class MasterOfTreasureInflation:

    def __init__(self):
        rateMultiplier = 1.5
        recruitsT5 = 5000
        self.treasure_rates_per_month = {
            't1': 1000 * rateMultiplier,
            't2': 2000 * rateMultiplier,
            't3': 8000 * rateMultiplier,
            't4': 14000 * rateMultiplier,
            't5': 20000 * rateMultiplier + recruitsT5,
        }
        # Balances for net treasure fragments created and broken at a given point in time
        self.dropped_treasures = {
            0: {
                't1': 0,
                't2': 0,
                't3': 0,
                't4': 0,
                't5': 0,
            }
        }

        initialParam = 1
        self.treasures_in_pool = {
            # set initial treasure fragment amounts in pool for day 0
            0: {
                't1': 1000 * initialParam,
                't2': 2000 * initialParam,
                't3': 4000 * initialParam,
                't4': 6000 * initialParam,
                't5': 8000 * initialParam,
            }
        }


    def initNewDay(self, day):
        if day not in self.treasures_in_pool.keys():
            self.treasures_in_pool[day] = {
                # assume we increment days, we never jump ahead x days
                't1': self.treasures_in_pool[day-1]['t1'],
                't2': self.treasures_in_pool[day-1]['t2'],
                't3': self.treasures_in_pool[day-1]['t3'],
                't4': self.treasures_in_pool[day-1]['t4'],
                't5': self.treasures_in_pool[day-1]['t5']
            }
        else:
            print("day {} exists".format(day))

        if day not in self.dropped_treasures.keys():
            self.dropped_treasures[day] = {
                't1': self.dropped_treasures[day-1]['t1'],
                't2': self.dropped_treasures[day-1]['t2'],
                't3': self.dropped_treasures[day-1]['t3'],
                't4': self.dropped_treasures[day-1]['t4'],
                't5': self.dropped_treasures[day-1]['t5']
            }
        else:
            print("day {} exists".format(day))


    def treasureEmissionRateDaily(self, tier=5):
        return self.treasure_rates_per_month[tier] / 30


    def emitTreasureFragmentsPerDay(self, day=0):
        self.treasures_in_pool[day]['t1'] += self.treasureEmissionRateDaily('t1')
        self.treasures_in_pool[day]['t2'] += self.treasureEmissionRateDaily('t2')
        self.treasures_in_pool[day]['t3'] += self.treasureEmissionRateDaily('t3')
        self.treasures_in_pool[day]['t4'] += self.treasureEmissionRateDaily('t4')
        self.treasures_in_pool[day]['t5'] += self.treasureEmissionRateDaily('t5')


    def _getDynamicDropRate(self, day, num_legions_questing, tier):
        N = num_legions_questing
        k = self.treasures_in_pool[day][tier]
        return inverse_quad(N, k, s=1)


    def _dropLoot(self, day, tier):
        self.treasures_in_pool[day][tier] -= 1
        self.dropped_treasures[day][tier] += 1


    def tryDrawFromLootBox(self, day, N, section=1):
        # assume a single legion has completed a quest.
        # RNG roll to see if T5, T4 treasures drop,
        # then decrement k = treasures_in_pool if so.
        droprates = self.questingDropRates(day, N, section)

        if section == 1:
            t5_droprate = droprates['t5_droprate']
            t4_droprate = droprates['t4_droprate']

            if maybe_drop_loot(t5_droprate):
                self._dropLoot(day, 't5')

            if maybe_drop_loot(t4_droprate):
                self._dropLoot(day, 't4')

        elif section == 2:
            t5_droprate = droprates['t5_droprate']
            t4_droprate = droprates['t4_droprate']
            t3_droprate = droprates['t3_droprate']

            if maybe_drop_loot(t5_droprate):
                self._dropLoot(day, 't5')

            if maybe_drop_loot(t4_droprate):
                self._dropLoot(day, 't4')

            if maybe_drop_loot(t3_droprate):
                self._dropLoot(day, 't3')

        elif section == 3:
            t3_droprate = droprates['t3_droprate']
            t2_droprate = droprates['t2_droprate']
            t1_droprate = droprates['t1_droprate']

            if maybe_drop_loot(t3_droprate):
                self._dropLoot(day, 't3')

            if maybe_drop_loot(t2_droprate):
                self._dropLoot(day, 't2')

            if maybe_drop_loot(t1_droprate):
                self._dropLoot(day, 't1')
        else:
            print("Invalid section: {}".format(section))

        # print("Treasures in Pool: {}".format(self.treasures_in_pool))
        # print("Dropped Treasures: {}".format(self.dropped_treasures))



    def questingDropRates(self, day, num_legions_questing, section=1):

        N = num_legions_questing
        print("Day={} | Questors={} | Section={}".format(day, N, section))

        if section == 1:
            t5 = self._getDynamicDropRate(day, N, tier='t5')
            t4 = self._getDynamicDropRate(day, N, tier='t4')
            return {
                't5_droprate': t5,
                't4_droprate': t4
            }
        elif section == 2:
            t5 = self._getDynamicDropRate(day, N, tier='t5')
            t4 = self._getDynamicDropRate(day, N, tier='t4')
            t3 = self._getDynamicDropRate(day, N, tier='t3')
            return {
                't5_droprate': t5,
                't4_droprate': t4,
                't3_droprate': t3
            }
        elif section == 3:
            t3 = self._getDynamicDropRate(day, N, tier='t3')
            t2 = self._getDynamicDropRate(day, N, tier='t2')
            t1 = self._getDynamicDropRate(day, N, tier='t1')
            return {
                't3_droprate': t3,
                't2_droprate': t2,
                't1_droprate': t1
            }
        else:
            print("Section {} does not exist".format(section))



def randomizeChangeInLegionsQuesting(low=-10, high=10):
    return np.random.randint(low, high)

def incrementLegionsQuesting(amount=20):
    return amount

def decrementLegionsQuesting(amount=20):
    return -amount

LEGIONS_QUESTING = 4000


def maybe_drop_loot(pr_threshold):
    score = np.random.uniform(0,100)
    if score < (pr_threshold * 100):
        return True
    else:
        return False



def treasure_inflation_rate(
    N = 100,
    k = 100,
    b = 1,
    d = 0,
    f = lambda N,k: N/k
):
    """
        N: population size
        b: birth rate
        d: death rate
        k: carrying capacity (crafting population)
    """
    return (b * f(N, k) - d) * N

def treasure_drop_rate(N=100, k=100, s=1):
    return inverse_quad(N, k, s)

def linear(N=100, k=100):
    return (1 - N/k)

def inverse_linear(N=100, k=100):
    return 1 / (1 + N/k)

def inverse_quad(N=100, k=100, s=1):
    ONE = 100_000
    return ONE / (ONE + ((N*ONE)/(k*ONE*s))**2*ONE)

def inverse_exp(N=100, k=100):
    return np.exp(-np.log(2) * N / k)


ax1 = 1
ax2 = 1
FRAMES = 200


def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


def simulate_fn(i):

    day = i
    section = 2 # questing section

    global LEGIONS_QUESTING
    if day > 50 and day <= 150:
        LEGIONS_QUESTING += incrementLegionsQuesting()
        LEGIONS_QUESTING += randomizeChangeInLegionsQuesting()
    elif day > 150 and day <= 200:
        LEGIONS_QUESTING += decrementLegionsQuesting()
        LEGIONS_QUESTING += randomizeChangeInLegionsQuesting()

    N = LEGIONS_QUESTING

    # clear plots to redraw
    ax1.clear()
    ax2.clear()

    ####### Evolve State: Treasures in Pool
    m.initNewDay(day=day)
    m.emitTreasureFragmentsPerDay(day=day)
    ## then foreach legion questing, attempt to remove treasures from pool
    for l in range(N):
        m.tryDrawFromLootBox(day, N, section)


    ###############################################################
    ## First plot the full range of the drop rates
    ## full plots for droprates, varying k = number of treasures in pool
    I = np.linspace(0, 12000, 12001)
    droprate_graph_bottom = [treasure_drop_rate(N=i, k=100) for i in I]
    droprate_graph_top = [treasure_drop_rate(N=i, k=20000) for i in I]

    if section == 2 or section == 1:
        droprate_graph_1 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t5']) for i in I]
        droprate_graph_2 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t4']) for i in I]
        droprate_graph_3 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t3']) for i in I]
    elif section == 3:
        droprate_graph_1 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t3']) for i in I]
        droprate_graph_2 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t2']) for i in I]
        droprate_graph_3 = [treasure_drop_rate(N=i, k=m.treasures_in_pool[day]['t1']) for i in I]

    ax1.plot(I, droprate_graph_top , color='black', alpha=0.6, linestyle="--", label='upper bound')
    ax1.plot(I, droprate_graph_1 , color=colors[0])
    ax1.plot(I, droprate_graph_2 , color=colors[1])
    ax1.plot(I, droprate_graph_3 , color=colors[2])
    ax1.plot(I, droprate_graph_bottom , color='black', alpha=0.6, linestyle="-.", label='lower bound')

    ax2.set(xlabel='#legions', ylabel='Number of legions ')
    ax1.set(xlabel='#legions', ylabel='Treasure Droprate')
    ###################################################################



    ## Plot current droprate [specific point]
    droprates = m.questingDropRates(day=day, num_legions_questing=N, section=section)

    if section == 2 or section == 1:
        t5_in_pool = m.treasures_in_pool[day]['t5']
        t4_in_pool = m.treasures_in_pool[day]['t4']
        t3_in_pool = m.treasures_in_pool[day]['t3']

        t5_droprate = droprates['t5_droprate']
        t4_droprate = droprates['t4_droprate']
        t3_droprate = droprates['t3_droprate']

        ax1.plot([N], [t5_droprate],
            label=r"Pr(T5 | k={:.0f}) = {:.1%}".format(t5_in_pool, t5_droprate),
            color=colors[0], linestyle="-", marker="*")

        ax1.plot([N], [t4_droprate],
            label=r"Pr(T4 | k={:.0f}) = {:.1%}".format(t4_in_pool, t4_droprate),
            color=colors[1], linestyle="-", marker="*")

        ax1.plot([N], [t3_droprate],
            label=r"Pr(T3 | k={:.0f}) = {:.1%}".format(t3_in_pool, t3_droprate),
            color=colors[2], linestyle="-", marker="*")

    elif section == 3:
        t3_in_pool = m.treasures_in_pool[day]['t3']
        t2_in_pool = m.treasures_in_pool[day]['t2']
        t1_in_pool = m.treasures_in_pool[day]['t1']

        t3_droprate = droprates['t3_droprate']
        t2_droprate = droprates['t2_droprate']
        t1_droprate = droprates['t1_droprate']

        ax1.plot([N], [t3_droprate],
            label=r"Pr(T3 | k={:.0f}) = {:.1%}".format(t3_in_pool, t3_droprate),
            color=colors[0], linestyle="-", marker="*")

        ax1.plot([N], [t2_droprate],
            label=r"Pr(T2 | k={:.0f}) = {:.1%}".format(t2_in_pool, t2_droprate),
            color=colors[1], linestyle="-", marker="*")

        ax1.plot([N], [t1_droprate],
            label=r"Pr(T1 | k={:.0f}) = {:.1%}".format(t1_in_pool, t1_droprate),
            color=colors[2], linestyle="-", marker="*")

    # ####### change in growth rate, vs population
    # ax2.plot(N, growth_rate_1, color=colors[0])
    # ax2.plot([num_summoners], [legion_birth_yvalue['1']],
    #     label="200 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['1']),
    #     color=colors[0], marker="*")

    # ax2.plot(N, growth_rate_2, color=colors[1])
    # ax2.plot([num_summoners], [legion_birth_yvalue['2']],
    #     label="400 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['2']),
    #     color=colors[1], marker="*")

    # ax2.plot(N, growth_rate_3, color=colors[2])
    # ax2.plot([num_summoners], [legion_birth_yvalue['3']],
    #     label="800 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['3']),
    #     color=colors[2], marker="*")

    ########################

    # ax1.axvline(x=N, color='black', linestyle=':', alpha=0.5)
    # ax2.axvline(x=N, color='black', linestyle=':', alpha=0.5)

    ax1.set_title('Variable Treasure Drop Rates | Day {} | {} Legions'.format(day, N), size=10)
    # ax2.set_title('Legions Birth Rate per Period (~7days) | {} Summoners'.format(N), size=10)

    ax1.legend()
    # ax2.legend()

    ax1.legend(bbox_to_anchor=(1.42, 1), loc="upper right")
    # ax2.legend(bbox_to_anchor=(1.48, 1), loc="upper right")

    ax1.grid(which='minor', alpha=0.2)
    ax1.grid(which='major', alpha=0.4)
    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.4)

    yticks_pct = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    yticks_label = ["{:.0%}".format(b) for b in yticks_pct]
    ax1.set_yticks(yticks_pct)
    ax1.set_yticklabels(yticks_label, fontsize=7)






def simulate_capped_treasure_emissions():

    global fig
    global ax2
    global ax1

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Variable Treasure Drop Rates')
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        simulate_fn,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.4)
    plt.show()




masterOfInflation = MasterOfTreasureInflation()
m = masterOfInflation
# # m.initNewDay(1)
# # m.initNewDay(2)

# m.questingDropRates(day=1, num_legions_questing=1000)
# m.treasures_in_pool

simulate_capped_treasure_emissions()




