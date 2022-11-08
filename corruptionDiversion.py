


base_rate = 2000

corruption_rate = {
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

# num_legions = 22_000


def divertCorruptionBetweenBuildings():

    # legions who ended up in each destination
    ldestination_questing = 0
    ldestination_crafting = 0
    ldestination_summoning = 0
    ldestination_h1 = 10_000
    ldestination_h2 = 4_000
    ldestination_h3 = 2_000
    ldestination_h4 = 0

    max_rate = base_rate * 2

    total_legions = ldestination_questing \
        + ldestination_crafting \
        + ldestination_summoning \
        + ldestination_h1 \
        + ldestination_h2 \
        + ldestination_h3 \
        + ldestination_h4

    print("total_legions: {}".format(total_legions))

    l_questing = ldestination_questing / total_legions
    l_crafting = ldestination_crafting / total_legions
    l_summoning = ldestination_summoning / total_legions
    l_h1 = ldestination_h1 / total_legions
    l_h2 = ldestination_h2 / total_legions
    l_h3 = ldestination_h3 / total_legions
    l_h4 = ldestination_h4 / total_legions


    corruption_rate = {
        "questing": base_rate * (1 + l_questing),
        "crafting": base_rate * (1 + l_crafting),
        "summoning": base_rate * (1 + l_summoning),
        'h1': base_rate/3 * (1 + l_h1),
        'h2': base_rate/3 * (1 + l_h2),
        'h3': base_rate/3 * (1 + l_h3),
        'h4': base_rate/3 * (1 + l_h4),
        # 'h5': base_rate/4,
        # 'h6': base_rate/4,
        # 'h7': base_rate/4,
        # 'h8': base_rate/4,
        # 'h9': base_rate/4,
    }
    return corruption_rate

c = divertCorruptionBetweenBuildings()


