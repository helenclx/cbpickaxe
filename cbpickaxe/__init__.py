"""
A library for data mining the game Cassette Beasts.
"""
from .animation import Animation, Frame, FrameTag
from .hoylake import Hoylake
from .item import Item
from .misc_types import Color
from .monster_form import Evolution, MonsterForm, TapeUpgrade
from .move import Move
from .translation_table import TranslationTable

__all__ = [
    "Animation",
    "Frame",
    "FrameTag",
    "Hoylake",
    "Item",
    "Color",
    "Evolution",
    "MonsterForm",
    "TapeUpgrade",
    "Move",
    "TranslationTable",
]
