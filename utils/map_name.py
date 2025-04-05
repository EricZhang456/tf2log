import re

class MapName:
    gamemode_dict = {
        "ctf": "Capture the Flag",
        "cp": "Control Point",
        "tc": "Territorial Control",
        "pl": "Payload",
        "arena": "Arena",
        "plr": "Payload Race",
        "koth": "King of the Hill",
        "tr": "Training",
        "sd": "Special Delivery",
        "mvm": "Mann vs. Machine",
        "rd": "Robot Destruction",
        "pass": "PASS Time",
        "pd": "Player Destruction",
        "vsh": "Versus Saxton Hale",
        "zi": "Zombie Infection",
        "tow": "Tug of War",
    }

    ad_maps = (
        "cp_altitude",
        "cp_brew",
        "cp_carrier",
        "cp_fortezza",
        "cp_gravelpit_snowy",
        "cp_darkmarsh",
        "cp_dustbowl",
        "cp_ambush_event",
        "cp_egypt_final",
        "cp_frostwatch",
        "cp_gorge",
        "cp_gorge_event",
        "cp_gravelpit",
        "ctf_haarp",
        "cp_hadal",
        "cp_hardwood_final",
        "cp_junction_final",
        "cp_lavapit_final",
        "cp_manor_event",
        "cp_mercenarypark",
        "cp_mossrock",
        "cp_mountainlab",
        "cp_snowplow",
        "cp_spookeyridge",
        "cp_steel",
        "cp_sulfur",
        "cp_overgrown",
    )

    domination_maps = (
        "cp_standin_final",
    )

    mannpower_maps = (
        "ctf_foundry",
        "ctf_gorge",
        "ctf_hellfire",
        "ctf_thundermountain",
    )

    @classmethod
    def map_name_to_game_mode(cls, map_name: str) -> str | None:
        if map_name in cls.ad_maps:
            return r'Attack/Defend'
        elif map_name in cls.mannpower_maps:
            return "Mannpower"
        elif map_name in cls.domination_maps:
            return "Domination"
        else:
            game_mode_str = re.search(r'([a-zA-Z]+)_', map_name)
            if game_mode_str is None:
                return None
            else:
                game_mode = cls.gamemode_dict.get(game_mode_str.group(1))
                if game_mode is None:
                    return None
                else:
                    return game_mode

    @classmethod
    def map_name_to_readable_name(cls, map_name: str) -> str:
        game_mode_pattern = re.search(r'([a-zA-Z]+_)', map_name)
        readable_map_name = map_name
        if game_mode_pattern is not None:
            if re.search(r'[a-zA-Z]+_.*_(final*)', map_name) is not None:
                readable_map_name = re.sub(r'_final.*', '', readable_map_name)
            if cls.gamemode_dict.get(game_mode_pattern.group(1).removesuffix("_")) is not None:
                readable_map_name = readable_map_name.removeprefix(game_mode_pattern.group(1))
        return readable_map_name.replace("_", " ").title()
