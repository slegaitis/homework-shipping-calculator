from enum import Enum


class Size(Enum):
    SMALL = 'S'
    MEDIUM = 'M'
    LARGE = 'L'


class Providers(Enum):
    LP = 'LP'
    MR = 'MR'
    UNKNOWN = 'Ignored'
