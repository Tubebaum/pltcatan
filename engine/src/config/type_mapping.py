from engine.src.resource_type import ResourceType
from types import *


type_mapping = { # from_type => to_type => conversion function
    StringType: {
        ResourceType: lambda st: ResourceType.find_by_value(st)
    }
}
