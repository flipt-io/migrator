from enum import Enum
from pydantic import BaseModel

class Variant(BaseModel):
    key: str 
    name: str | None
    description: str | None

class FlagType(Enum):
    variant = 'FLAG_TYPE_VARIANT'
    boolean = 'FLAG_TYPE_BOOLEAN'

class Flag(BaseModel):
    key: str
    name: str
    description: str | None
    enabled: bool
    type: FlagType = FlagType.variant
    variants: list[Variant] | None

class ConstraintComparisonType(Enum):
    string = 'STRING_COMPARISON_TYPE'
    number = 'NUMBER_COMPARISON_TYPE'
    boolean = 'BOOLEAN_COMPARISON_TYPE'
    datetime = 'DATETIME_COMPARISON_TYPE'

class Constraint(BaseModel):
    property: str
    operator: str
    value: str
    type: ConstraintComparisonType = ConstraintComparisonType.string

class SegmentMatchType(Enum):
    all = 'MATCH_TYPE_ALL'
    any = 'MATCH_TYPE_ANY'

class Segment(BaseModel):
    key: str
    name: str | None
    description: str | None
    match_type: SegmentMatchType = SegmentMatchType.all
    constraints: list[Constraint] | None

class Document(BaseModel):
    flags: list[Flag] | None
    segments: list[Segment] | None

class Documents(BaseModel):
    namespaces: dict[str, Document] | None