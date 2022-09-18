
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation

from corruptionAccountant import CorruptionAccountant
from styles import brown, offwhite, grey, gold, darkblue, lightblue
from styles import line_styles, line_colors


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
    corrAccountant.emitForgeableCorruption(hour)
    corrAccountant.addAccountingEntriesForHour(hour)

    for k in corrAccountant.y_structures:

        corrAccountant.maybeRemoveCorruptionNTimes(hour, k)

        #### Plot 1 - Corruption in each BW structure
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

    #### Plot 3 - Amount of Corruption in forbidden crafts forgeable pool
    ax3.plot(
        hours,
        corrAccountant.y_forgeable_corruption.values(),
        label="Total Corruption Forgeable",
        color='royalblue',
        linestyle=":",
    )
    ax3.plot(
        hours,
        # corrAccountant.y_crafted_corruption.values(),
        corrAccountant.y_cumulative_crafted_corruption.values(),
        label="Cumulative Corruption Crafted",
        color='crimson',
        linestyle=":",
    )
    ax3.set(xlabel='hours', ylabel='Corruption Forged')

    ax1.set_title('Corruption in Buildings', size=10, color=gold)
    ax2.set_title('Prisms Burnt & Dark Prisms Created', size=10, color=gold)
    ax3.set_title('Cumulative Corruption Forged', size=10, color=gold)

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





