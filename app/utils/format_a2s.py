import a2s

class FormatA2S:
    @staticmethod
    def info(server_ip: str, server_port=27015) -> dict:
        server_address = (server_ip, server_port)
        server_info_raw = a2s.info(server_address)
        server_info = {
            "protocol": server_info_raw.protocol,
            "version": server_info_raw.version,
            "name": server_info_raw.server_name,
            "map": server_info_raw.map_name,
            "folder": server_info_raw.folder,
            "game": server_info_raw.game,
            "player_count": server_info_raw.player_count,
            "max_players": server_info_raw.max_players,
            "bot_count": server_info_raw.bot_count,
            "server_type": server_info_raw.server_type,
            "platform": server_info_raw.platform,
            "password": server_info_raw.password_protected,
            "vac": server_info_raw.vac_enabled,
            "ping": server_info_raw.ping,
            "appid": server_info_raw.app_id,
            "edf": server_info_raw.edf,
        }

        if server_info_raw.keywords:
            server_info["tags"] = list(filter(None, server_info_raw.keywords.split(",")))
        
        optional_attrs = ("port", "steam_id", "stv_port", "stv_name", "game_id")
        for item in optional_attrs:
            if getattr(server_info_raw, item) is not None:
                server_info.update({item: getattr(server_info_raw, item)})

        return server_info

    @staticmethod
    def rules(server_ip: str, server_port=271015) -> dict:
        server_address = (server_ip, server_port)
        return a2s.rules(server_address)

    @staticmethod
    def players(server_ip: str, server_port=27015) -> list[dict]:
        server_address = (server_ip, server_port)
        server_players = []
        server_players_raw = a2s.players(server_address)

        for item in server_players_raw:
            player = {"index": item.index, "name": item.name, "score": item.score, "time": item.duration}
            server_players.append(player)

        return server_players
