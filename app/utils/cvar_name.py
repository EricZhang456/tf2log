class CvarName:
    stock_cvar_readable_name = {
        "mp_autoteambalance": "Auto Team Balance",
        "mp_scrambleteams_auto": "Auto Team Scramble",
        "mp_disable_respawn_times": "Disable Respawn Times",
        "mp_fadetoblack": "Fade to Black",
        "mp_falldamage": "Fall Damage Based on Distance",
        "mp_friendlyfire": "Friendly Fire",
        "mp_flashlight": "Flashlight",
        "sv_footsteps": "Footsteps",
        "mp_forceautoteam": "Force Auto-Assign Team",
        "mp_fraglimit": "Kill Limit",
        "mp_highlander": "Highlander Mode",
        "mp_holiday_nogifts": "Disable Holiday Gifts",
        "mp_match_end_at_timelimit": "Match End at Map End",
        "mp_maxrounds": "Round Limit",
        "mp_respawnwavetime": "Respawn Wave Time",
        "mp_scrambleteams_auto_windifference": "Auto Scramble Score Limit",
        "mp_stalemate_enable": "Sudden Death",
        "mp_stalemate_meleeonly": "Sudden Death Melee Only",
        "mp_timelimit": "Map Time Limit (in minutes)",
        "mp_tournament": "Tournament Mode",
        "mp_tournament_readymode": "Tournament Per-Player Ready",
        "mp_tournament_readymode_countdown": "Tournament Ready Countdown",
        "mp_tournament_readymode_min": "Tournament Ready Minimum Players",
        "mp_tournament_readymode_team_size": "Tournament Ready Minimum Players Per Team",
        "mp_windifference": "Score Difference Limit",
        "mp_windifference_min": "Min. Score for Score Difference Limit",
        "mp_winlimit": "Score Limit",
        "sv_accelerate": "Acceleration",
        "sv_airaccelerate": "Air Acceleration",
        "sv_wateraccelerate": "Water Acceleration",
        "sv_waterfriction": "Water Friction",
        "sv_alltalk": "Global Voice Chat",
        "sv_cheats": "Cheats",
        "sv_contact": "Admin Email",
        "sv_steamgroup": "Steam Group",
        "sv_friction": "Friction",
        "sv_gravity": "Gravity",
        "sv_maxspeed": "Max Speed",
        "sv_pausable": "Allow Game Pause",
        "sv_voiceenable": "Voice Chat",
        "sv_vote_quorum_ratio": "Vote Minimum Quorum",
        "tf_allow_player_name_change": "Allow Name Change",
        "tf_allow_player_use": "Allow +use",
        "tf_arena_first_blood": "Arena First Blood Crits",
        "tf_arena_max_streak": "Arena Auto Scramble Score Limit",
        "tf_arena_override_cap_enable_time": "Arena Cap Time Override",
        "tf_arena_change_limit": "Arena Class Change Limit",
        "tf_arena_force_class": "Arena Force Random Class",
        "tf_arena_preround_time": "Arena Pre-Round Timer",
        "tf_arena_round_time": "Arena Round Time Override",
        "tf_arena_use_queue": "Arena Spectator Queue",
        "tf_birthday": "Birthday Mode",
        "tf_bot_count": "Bot Count",
        "tf_classlimit": "Class Limit",
        "tf_ctf_bonus_time": "CTF Capture Crit Time",
        "tf_damage_disablespread": "Random Damage Spread Disabled",
        "tf_force_holidays_off": "Force Disable Holiday Mode",
        "tf_use_fixed_weaponspreads": "Fixed Weapon Spread",
        "tf_gravetalk": "Grave Talk",
        "tf_medieval_autorp": "Medieval Mode Text Chat Filter",
        "tf_playergib": "Player Gib",
        "tf_powerup_mode": "Mannpower Powerup",
        "tf_overtime_nag": "Overtime Announcer Nag",
        "tf_spec_xray": "Spectator Xray",
        "tf_spells_enabled": "Players Drop Halloween Spells",
        "tf_weapon_criticals": "Random Crits",
        "tf_weapon_criticals_melee": "Melee Random Crits",
        "tv_enable": "SourceTV",
    }

    sm_cvar_readable_name = {
        "metamod_version": "Metamod:Source Version",
        "sourcemod_version": "SourceMod Version",
        "sm_nextmap": "Next Map",
    }

    rules_cvar_bool = (
        "mp_autoteambalance",
        "mp_disable_respawn_times",
        "mp_fadetoblack",
        "mp_falldamage",
        "mp_flashlight",
        "mp_forceautoteam",
        "mp_friendlyfire",
        "mp_highlander",
        "mp_holiday_nogifts",
        "mp_match_end_at_timelimit",
        "mp_scrambleteams_auto",
        "mp_stalemate_enable",
        "mp_stalemate_meleeonly",
        "mp_tournament",
        "sv_alltalk",
        "sv_cheats",
        "sv_pausable",
        "sv_voiceenable",
        "tf_allow_player_use",
        "tf_arena_first_blood",
        "tf_arena_force_class",
        "tf_arena_use_queue",
        "tf_damage_disablespread",
        "tf_gravetalk",
        "tf_medieval_autorp",
        "tf_playergib",
        "tf_powerup_mode",
        "tf_spec_xray",
        "tf_use_fixed_weaponspreads",
        "tf_weapon_criticals",
        "tf_weapon_criticals_melee",
        "tv_enable",
    )

    rules_cvars_int = (
        "mp_fraglimit",
        "mp_maxrounds",
        "mp_scrambleteams_auto_windifference",
        "mp_timelimit",
        "mp_windifference_min",
        "mp_windifference",
        "mp_winlimit",
        "sv_accelerate",
        "sv_airaccelerate",
        "sv_friction",
        "sv_gravity",
        "tf_arena_max_streak",
        "tf_arena_override_cap_enable_time",
        "tf_classlimit",
        "tf_ctf_bonus_time",
    )

    rules_cvar_float = (
        "mp_respawnwavetime",
    )

    __rules_cvar_sort_target = (
        # Limits
        "mp_timelimit",
        "mp_match_end_at_timelimit",
        "mp_maxrounds",
        "mp_winlimit",
        "mp_windifference",
        "mp_windifference_min",
        "mp_scrambleteams_auto_windifference",
        "mp_fraglimit",
        # Typical Game Options
        "mp_autoteambalance",
        "mp_scrambleteams_auto",
        "sv_voiceenable",
        "sv_alltalk",
        "tf_gravetalk",
        "tf_weapon_criticals",
        "tf_weapon_criticals_melee",
        "tf_use_fixed_weaponspreads",
        "tf_damage_disablespread",
        "tf_classlimit",
        "mp_forceautoteam",
        "mp_stalemate_enable",
        "mp_stalemate_meleeonly",
        "mp_disable_respawn_times",
        "mp_respawnwavetime",
        "tf_playergib",
        "mp_tournament",
        "mp_highlander",
        # Custom Game Mode Options
        "mp_friendlyfire",
        "mp_fadetoblack",
        "mp_flashlight",
        "tf_arena_max_streak",
        "tf_arena_override_cap_enable_time",
        "tf_arena_first_blood",
        "tf_arena_force_class",
        "tf_arena_use_queue",
        "tf_ctf_bonus_time",
        # Exotic Game Options
        "sv_cheats",
        "tf_allow_player_use",
        "sv_pausable",
        "sv_gravity",
        "sv_accelerate",
        "sv_airaccelerate",
        "sv_friction",
        "mp_falldamage",
        # Misc
        "tf_force_holidays_off",
        "mp_holiday_nogifts",
        "tf_powerup_mode",
        "tf_medieval_autorp",
        "tf_spec_xray",
        "tv_enable",
    )

    @classmethod
    def __prune_rules_cvar_dict(cls, rules:dict) -> dict:
        return {key: rules[key] for key in cls.__rules_cvar_sort_target if key in cls.__rules_cvar_sort_target}

    @classmethod
    def rules_to_readable_dict(cls, rules: dict) -> dict:
        pruned_dict = cls.__prune_rules_cvar_dict(rules)
        readable_dict = {}
        for key, value in pruned_dict.items():
            if key in cls.rules_cvar_bool:
                readable_bool_value = "On" if int(value) == 1 else "Off"
                readable_dict.update({cls.stock_cvar_readable_name.get(key): readable_bool_value})
            elif key in cls.rules_cvars_int:
                readable_int_value = value if int(value) not in (0, -1) else "Off"
                readable_dict.update({cls.stock_cvar_readable_name.get(key): readable_int_value})
            elif key in cls.rules_cvar_float:
                readable_dict.update({cls.stock_cvar_readable_name.get(key): int(float(value))})
            else:
                continue
        return readable_dict
    
    @staticmethod
    def get_next_map(rules: dict) -> str | None:
        if rules.get("sm_nextmap") is not None:
            return rules.get("sm_nextmap")
        elif rules.get("nextlevel") is not None:
            return rules.get("nextlevel")
        else:
            return None
