# Global Settings for the application

# ? Imports -------------------------------------------------------------------------------------

from enum import Enum
from dataclasses import dataclass

# ? Globals -------------------------------------------------------------------------------------

@dataclass
class Config(Enum):
    """
    Project Config
    """
    # App info
    NAME = "Library Inventory Manager"
    VERSION = "v0.1.0"
    AUTHOR = "Yrrrrrf"
    EMAIL = "fernandorezacampos@gmail.com"
    DESCRIPTION = "A library inventory manager (LIM) for managing books, authors, publishers, and libraries"

