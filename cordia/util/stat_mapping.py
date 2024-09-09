def get_stat_modifier(stat: str):
    stat_type_mapping = {
        "boss_damage": "%",
        "crit_chance": "%",
        "penetration": "%",
        "combo_chance": "%",
        "strike_radius": "",
        "attack_cooldown": "s",
        "spell_cooldown": "s",
        "magic_penetration": "%",
    }
    return stat_type_mapping.get(stat, "")


def get_stat_emoji(stat: str):
    emoji_mapping = {
        # Main stats
        "strength": "💪",
        "persistence": "🔋",
        "intelligence": "🧠",
        "efficiency": "⚡️",
        "luck": "🍀",
        # Special Stats
        "damage": "💥",
        "crit_chance": "🎯",
        "boss_damage": "👹",
        "penetration": "🗡️",
        "combo_chance": "🥊",
        "strike_radius": "🎆",
        "attack_cooldown": "🕒",
        # Spells
        "spell_damage": "💥",
        "scaling_multiplier": "🎚️",
        "spell_cooldown": "🕒",
        "magic_penetration": "🌠",
        "spell_strike_radius": "🎆",
    }
    return emoji_mapping.get(stat, "")
