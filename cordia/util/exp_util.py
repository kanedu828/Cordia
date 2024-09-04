import math

def exp_to_level(exp):
        """Convert experience points to level."""
        base_exp = 5  # Base experience required for level 1
        level = math.floor(math.sqrt((exp + base_exp) / 5))
        return max(1, level)  # Ensure that the minimum level is 1

def level_to_exp(level):
    """Convert level to the total experience required to reach that level."""
    base_exp = 5  # Base experience for level 1
    exp = 5 * (level ** 2) - base_exp
    return exp

def percent_to_next_level(exp):
    """Calculate the percentage of experience left to the next level."""
    current_level = exp_to_level(exp)
    current_level_exp = level_to_exp(current_level)
    next_level_exp = level_to_exp(current_level + 1)
    
    exp_in_current_level = exp - current_level_exp
    exp_needed_for_next_level = next_level_exp - current_level_exp
    
    percent_complete = (exp_in_current_level / exp_needed_for_next_level) * 100
    
    return percent_complete