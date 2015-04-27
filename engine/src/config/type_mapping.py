from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from types import *


type_mapping = { # from_type => to_type => conversion function
    StringType: {
        ResourceType: lambda st: ResourceType.find_by_value(st),
        PositionType: lambda st: PositionType.find_by_value(st)
    }
}
