CORRUPTION_FLOWS_BASE_RATE  = 4000

corruption_rate = {
    "questing": CORRUPTION_FLOWS_BASE_RATE ,
    "crafting": CORRUPTION_FLOWS_BASE_RATE ,
    "summoning": CORRUPTION_FLOWS_BASE_RATE ,
    "forbidden_crafts": CORRUPTION_FLOWS_BASE_RATE ,
    'h1': CORRUPTION_FLOWS_BASE_RATE /3,
    'h2': CORRUPTION_FLOWS_BASE_RATE / 3,
    'h3': CORRUPTION_FLOWS_BASE_RATE / 3,
    'h4': CORRUPTION_FLOWS_BASE_RATE / 3,
    'h5': CORRUPTION_FLOWS_BASE_RATE / 3,
    'h6': CORRUPTION_FLOWS_BASE_RATE / 3,
    'h7': CORRUPTION_FLOWS_BASE_RATE / 3
}


### Corruption Removal Amounts

buildings_prism_small = 4000
buildings_prism_medium = 6000
buildings_prism_large = 8000

harvester_prism_recipe = 8000
harvester_bc_recipe = 12000

amount_corruption_removed = {
    "questing": buildings_prism_medium,
    "crafting": buildings_prism_medium,
    "summoning": buildings_prism_medium,
    "forbidden_crafts": buildings_prism_medium,
    'h1': harvester_prism_recipe,
    'h2': harvester_prism_recipe,
    'h3': harvester_prism_recipe,
    'h4': harvester_prism_recipe,
    'h5': harvester_prism_recipe,
    'h6': harvester_prism_recipe,
    'h7': harvester_prism_recipe,
}


dark_prism_drop_rates = {
    # level 6+
    6: 0.5,
    # level 5
    5: 0.35,
    # level 4
    4: 0.25,
    # level 3
    3: 0.15,
    # level 2
    2: 0.10,
    # level 1
    1: 0.05,
    # level 0
    0: 0,
}


percent_corr_forged_by_legion = {
    'gen0_1_1': 0.07, # 1/1 7%
    'gen0_rare': 0.03, # all-class 3%
    'gen0_uncommon': 0.02, # Assasin etc 2%
    'gen0_special': 0.0175, # includes riverman, Numeraire 1.75%
    'gen0_common': 0.015, # commons 1.5%
    'gen1_rare': 0.01, # 1.1%
    'gen1_uncommon': 0.0105, # 1.05%
    'gen1_common': 0.01, # 1%
}

# months
harvester_age = {
    "h1": 11,
    "h2": 10,
    "h3": 10,
    "h4": 6,
    "h5": 6,
    "h6": 2,
    "h7": 1,
}


default_initial_balances = {
    'y_dark_prisms': 0,
    'y_dark_prisms_cumulative': 0,
    'y_prisms': 0,
    'y_prisms_cumulative': 0,
    'y_forgeable_corruption': 100_000,
    'y_crafted_corruption': 0,
}

initial_corruption_balances = {
    "questing": 80_000,
    "crafting": 80_000,
    "summoning": 80_000,
    'h1': 80_000,
    'h2': 80_000,
    'h3': 80_000,
    'h4': 80_000,
    'h5': 80_000,
    'h6': 80_000,
    'h7': 80_000,
}

harvester_list = [
    'h1',
    'h2',
    'h3',
    'h4',
    'h5',
    'h6',
    'h7'
]