import re

class MapUtils:
    GAMEMODE_DICT = {
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

    AD_MAPS = (
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

    DOMINATION_MAPS = (
        "cp_standin_final",
    )

    MANNPOWER_MAPS = (
        "ctf_foundry",
        "ctf_gorge",
        "ctf_hellfire",
        "ctf_thundermountain",
    )

    MAP_SPECIAL_NAMES = {
        "ctf_doublecross": "Double Cross",
        "ctf_doublecross_snowy": "Doublefrost",
        "ctf_helltrain_event": "Helltrain",
        "ctf_turbine_winter": "Turbine Center",
        "cp_canaveral_5cp": "Canaveral",
        "cp_sunshine_event": "Sinshine",
        "cp_gravelpit_snowy": "Coal Pit",
        "cp_ambush_event": "Erebus",
        "cp_gravelpit": "Gravel Pit",
        "cp_lavapit_final": "Lava Pit",
        "cp_manor_event": "Mann Manor",
        "cp_mercenarypark": "Mercenary Park",
        "cp_mountainlab": "Mountain Lab",
        "cp_degrootkeep": "DeGroot Keep",
        "cp_degrootkeep_rats": "Sandcastle",
        "pl_badwater": "Badwater Basin",
        "pl_breadspace": "Bread Space",
        "pl_cactuscanyon": "Cactus Canyon",
        "pl_fifthcurve_event": "Brimstone",
        "pl_goldrush": "Gold Rush",
        "pl_rumble_event": "Gravestone",
        "pl_sludgepit_event": "Ghoulpit",
        "pl_hasslecastle": "Hassle Castle",
        "pl_millstone_event": "Hellstone",
        "pl_coal_event": "Polar",
        "pl_precipice_event_final": "Precipice",
        "pl_thundermountain": "Thunder Mountain",
        "plr_bananabay": "Banana Bay",
        "plr_hacksaw_event": "Bonesaw",
        "plr_hightower_event": "Helltower",
        "arena_lumberyard_event": "Graveyard",
        "koth_bagel_event": "Cauldron",
        "koth_viaduct_event": "Eyeaduct",
        "koth_lakeside_event": "Ghost Fort",
        "koth_king": "Kong King",
        "koth_slaughter_event": "Laughter",
        "koth_undergrove_event": "Moldergrove",
        "koth_synthetic_event": "Sinthetic",
        "koth_sawmill_event": "Soul-Mill",
        "sd_doomsday_event": "Carnival of Carnage",
        "mvm_coaltown": "Coal Town",
        "ctf_thundermountain": "Thunder Mountain",
        "pd_cursed_cove_event": "Cursed Cove",
        "pd_pit_of_death_event": "Pit of Death",
        "pd_snowville_event": "SnowVille",
        "vsh_nucleus": "Nucleus VSH",
        "vsh_tinyrock": "Tiny Rock",
    }

    @classmethod
    def map_name_to_game_mode(cls, map_name: str) -> str | None:
        if map_name in cls.AD_MAPS:
            return "Attack/Defend"
        elif map_name in cls.MANNPOWER_MAPS:
            return "Mannpower"
        elif map_name in cls.DOMINATION_MAPS:
            return "Domination"
        else:
            game_mode_str = re.search(r'([a-zA-Z]+)_', map_name)
            if game_mode_str is None:
                return None
            else:
                game_mode = cls.GAMEMODE_DICT.get(game_mode_str.group(1))
                if game_mode is None:
                    return None
                else:
                    return game_mode

    @classmethod
    def map_name_to_readable_name(cls, map_name: str) -> str:
        if cls.MAP_SPECIAL_NAMES.get(map_name) is None:
            game_mode_pattern = re.search(r'([a-zA-Z]+_)', map_name)
            readable_map_name = map_name
            if game_mode_pattern is not None:
                if re.search(r'[a-zA-Z]+_.*_(final*)', map_name) is not None:
                    readable_map_name = re.sub(r'_final.*', '', readable_map_name)
                if cls.GAMEMODE_DICT.get(game_mode_pattern.group(1).removesuffix("_")) is not None:
                    readable_map_name = readable_map_name.removeprefix(game_mode_pattern.group(1))
            return readable_map_name.replace("_", " ").title()
        else:
            return cls.MAP_SPECIAL_NAMES.get(map_name)

    @staticmethod
    def resolve_workshop_map_name(map_name: str) -> str:
        if map_name.startswith("workshop/"):
            resolved_map_name = re.search(r'workshop/(.*)\.ugc[0-9]+', map_name)
            if resolved_map_name is not None:
                return resolved_map_name.group(1)
            else:
                return "Workshop Map"
        else:
            return map_name

    @staticmethod
    def get_workshop_map_id(map_name: str) -> str | None:
        if map_name.startswith("workshop/"):
            workshop_verbose_map_name = re.search(r'workshop/.*\.ugc([0-9]+)', map_name)
            workshop_concise_map_name = re.search(r'workshop/([0-9]+)', map_name)
            if workshop_verbose_map_name is not None:
                return workshop_verbose_map_name.group(1)
            elif workshop_concise_map_name is not None:
                return workshop_concise_map_name.group(1)
            else:
                return None
        else:
            return None
