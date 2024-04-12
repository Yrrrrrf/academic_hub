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
    NAME = "Academic Hub"
    VERSION = "v0.1.0"
    AUTHOR = "Yrrrrrf"
    EMAIL = "fernandorezacampos@gmail.com"
    DESCRIPTION = "A simple Academic Hub management system for School and Library"
