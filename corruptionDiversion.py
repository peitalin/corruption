
from parameters import corruption_rate


def divertCorruptionBetweenBuildings():

    # legions who ended up in each destination
    ldestination_h1 = 10_000
    ldestination_h2 = 10_000
    ldestination_h3 = 10_000
    ldestination_h4 = 0
    ldestination_h5 = 0
    ldestination_h6 = 0
    ldestination_h7 = 0

    max_rate = base_rate * 2

    total_legions = ldestination_h1 \
        + ldestination_h2 \
        + ldestination_h3 \
        + ldestination_h4 \
        + ldestination_h5 \
        + ldestination_h6 \
        + ldestination_h7

    print("total_legions: {}".format(total_legions))

    l_h1 = ldestination_h1 / total_legions
    l_h2 = ldestination_h2 / total_legions
    l_h3 = ldestination_h3 / total_legions
    l_h4 = ldestination_h4 / total_legions
    l_h5 = ldestination_h5 / total_legions
    l_h6 = ldestination_h6 / total_legions
    l_h7 = ldestination_h7 / total_legions

    crypts_altered_corruption_rate = {
        'h1': base_rate/3 * (1 + l_h1),
        'h2': base_rate/3 * (1 + l_h2),
        'h3': base_rate/3 * (1 + l_h3),
        'h4': base_rate/3 * (1 + l_h4),
        'h5': base_rate/3 * (1 + l_h5),
        'h6': base_rate/3 * (1 + l_h6),
        'h7': base_rate/3 * (1 + l_h7),
    }
    return crypts_altered_corruption_rate

c = divertCorruptionBetweenBuildings()


