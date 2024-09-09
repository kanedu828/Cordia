import random
from cordia.model.monster import Monster

def get_random_battle_text(kills: int, monster: str) -> str:
    no_kill_text = [
        f"Despite your best efforts, you could not defeat a **{monster}**. Try again!",
        f"You were quickly overwhelmed by a **{monster}**. Try again!",
        f"Your strikes were not enough to defeat a **{monster}**. Try again!",
        f"You were no match for a **{monster}**. Try again!"
    ]

    single_kill_text = [
        f"Using all your might, you defeat a **{monster}**",
        f"After an epic battle, you defeat a **{monster}**",
        f"After a hard fought battle, you defeat a **{monster}**",
        f"After an intense clash, you emerge victorious against a **{monster}**!",
        f"With a final blow, a **{monster}** falls to your might!"
    ]

    multi_kill_text = [
        f"With your might, you overpower and kill **{kills}** **{monster}**s",
        f"In a show of grandeur, you defeat **{kills}** **{monster}**s",
        f"With your overwhelming strength, you defeat **{kills}** **{monster}**s"
    ]

    if kills == 0:
        return random.choice(no_kill_text)
    
    if kills == 1:
        return random.choice(single_kill_text)
    
    return random.choice(multi_kill_text)
