import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import plot
from matplotlib.animation import FuncAnimation



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
FRAMES = 100


def init_plot(i=0):
    # do nothing, prevents FuncAnim calling initialization twice
    return


def draw_legion_paths(i):

    num_craftor = 8 + i * 8 # each i-frame is 8 craftors
    num_summoners = 16 + i * 16 # each i-frame is 8 craftors

    # clear plots to redraw
    ax2.clear()
    ax1.clear()
    # ax2.clear()

    colors = [
        'crimson',
        'mediumorchid',
        'royalblue',
        'black',
    ]

    N = np.linspace(0, 2000, 2001)
    N_k200 = [n/200 for n in N]
    N_k400 = [n/400 for n in N]
    N_k800 = [n/800 for n in N]

    growth_rate_1 = [treasure_inflation_rate(N=n, k=200, f=treasure_drop_rate) for n in N]
    growth_rate_2 = [treasure_inflation_rate(N=n, k=400, f=treasure_drop_rate) for n in N]
    growth_rate_3 = [treasure_inflation_rate(N=n, k=800, f=treasure_drop_rate) for n in N]

    success_rate_1 = [treasure_drop_rate(N=n, k=200) for n in N]
    success_rate_2 = [treasure_drop_rate(N=n, k=400) for n in N]
    success_rate_3 = [treasure_drop_rate(N=n, k=800) for n in N]

    # array index for the growth_rate of current num_summoners
    index_growth_num_summoners = np.argmin(np.abs(np.subtract(N, num_summoners)))

    legion_birth_yvalue = {
        '1': growth_rate_1[index_growth_num_summoners],
        '2': growth_rate_2[index_growth_num_summoners],
        '3': growth_rate_3[index_growth_num_summoners],
    }
    success_rate_yvalue = {
        '1': success_rate_1[index_growth_num_summoners],
        '2': success_rate_2[index_growth_num_summoners],
        '3': success_rate_3[index_growth_num_summoners],
    }

    ############## PLOTS ##################

    ####### change in summoning success rate, vs population
    ax1.plot(N, success_rate_1 , color=colors[0])
    ax1.plot(N, success_rate_2 , color=colors[1])
    ax1.plot(N, success_rate_3 , color=colors[2])

    ax2.set(xlabel='#summoners', ylabel='Number of legions born/period (~7days) ')
    ax1.set(xlabel='#summoners', ylabel='Summoning Success Rate')

    ax1.plot([num_summoners], [success_rate_yvalue['1']],
        label=r"Pr(summon|craftors=200): %{:.1%}".format(success_rate_yvalue['1']),
        color=colors[0], linestyle="-", marker="*")

    ax1.plot([num_summoners], [success_rate_yvalue['2']],
        label=r"Pr(summon|craftors=400): %{:.1%}".format(success_rate_yvalue['2']),
        color=colors[1], linestyle="-", marker="*")

    ax1.plot([num_summoners], [success_rate_yvalue['3']],
        label=r"Pr(summon|craftors=800): %{:.1%}".format(success_rate_yvalue['3']),
        color=colors[2], linestyle="-", marker="*")

    ####### change in growth rate, vs population
    ax2.plot(N, growth_rate_1, color=colors[0])
    ax2.plot([num_summoners], [legion_birth_yvalue['1']],
        label="200 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['1']),
        color=colors[0], marker="*")

    ax2.plot(N, growth_rate_2, color=colors[1])
    ax2.plot([num_summoners], [legion_birth_yvalue['2']],
        label="400 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['2']),
        color=colors[1], marker="*")

    ax2.plot(N, growth_rate_3, color=colors[2])
    ax2.plot([num_summoners], [legion_birth_yvalue['3']],
        label="800 Craftors => {:.0f} Legions Born/period".format(legion_birth_yvalue['3']),
        color=colors[2], marker="*")

    ########################

    ax2.axvline(x=num_summoners, color='black', linestyle=':', alpha=0.5)
    ax1.axvline(x=num_summoners, color='black', linestyle=':', alpha=0.5)

    ax2.set_title('Legions Birth Rate per Period (~7days) | {} Summoners'.format(num_summoners), size=10)
    ax1.set_title('%Summon Success Rate | {} Summoners'.format(num_summoners), size=10)

    ax2.legend()
    ax1.legend()

    ax1.legend(bbox_to_anchor=(1.42, 1), loc="upper right")
    ax2.legend(bbox_to_anchor=(1.48, 1), loc="upper right")

    ax2.grid(which='minor', alpha=0.2)
    ax2.grid(which='major', alpha=0.4)
    ax1.grid(which='minor', alpha=0.2)
    ax1.grid(which='major', alpha=0.4)






def run_legion_growth_simulation():

    global fig
    global ax2
    global ax1

    fig, (ax1, ax2) = plt.subplots(2)
    fig.suptitle('Dynamic Legion Summoning Rates')
    fig.set_size_inches(12, 9)

    ani = FuncAnimation(
        fig,
        draw_legion_paths,
        frames=FRAMES,
        interval=100,
        repeat=False,
        init_func=init_plot,
    )

    plt.subplots_adjust(left=0.08, right=0.7, top=0.9, bottom=0.1, hspace=0.4)
    plt.show()

run_legion_growth_simulation()




