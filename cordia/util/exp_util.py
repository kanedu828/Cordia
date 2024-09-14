import math

BASE_EXP = 15
GROWTH_FACTOR = 1.5
INITIAL_EXP = 25


def exp_to_level(exp: int) -> int:
    # Estimate the level by reversing the formula for the total exp to reach a level
    level = 1
    while True:
        exp_to_next_level = BASE_EXP * (level - 1) ** GROWTH_FACTOR + INITIAL_EXP
        if exp < exp_to_next_level:
            break
        exp -= exp_to_next_level
        level += 1

    return level


def level_to_exp(level: int) -> int:
    total_exp = 0
    for current_level in range(1, level):
        exp_to_next_level = (
            BASE_EXP * (current_level - 1) ** GROWTH_FACTOR + INITIAL_EXP
        )
        total_exp += exp_to_next_level

    return int(total_exp)


def percent_to_next_level(exp):
    """Calculate the percentage of experience left to the next level."""
    current_level = exp_to_level(exp)
    current_level_exp = level_to_exp(current_level)
    next_level_exp = level_to_exp(current_level + 1)

    exp_in_current_level = exp - current_level_exp
    exp_needed_for_next_level = next_level_exp - current_level_exp

    percent_complete = (exp_in_current_level / exp_needed_for_next_level) * 100

    return percent_complete
