"""Game presets enum."""

from enum import Enum


class GamePresets(Enum):
    """Game presets enum."""
    VANILLA = 1
    SEMI_VANILLA = 2
    CUSTOM = 3
    MVM = 4
    ALL = 5

    @classmethod
    def _missing_(cls, _):
        return cls.VANILLA
