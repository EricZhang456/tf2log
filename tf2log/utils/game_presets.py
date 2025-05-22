"""Game presets enum."""

from enum import Enum


class GamePresets(Enum):
    """Game presets enum."""
    VANILLA = 1
    SEMI_VANILLA = 2
    CUSTOM = 3
    ALL = 4

    @classmethod
    def _missing_(cls, _):
        return cls.VANILLA
