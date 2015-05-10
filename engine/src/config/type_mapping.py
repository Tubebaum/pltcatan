import engine.src.lib.utils as utils
from engine.src.resource_type import ResourceType
from engine.src.position_type import PositionType
from types import *


type_mapping = { # from_type => to_type => conversion function
    StringType: {
        ResourceType: lambda st: ResourceType.find_by_value(st),
        PositionType: lambda st: PositionType.find_by_value(st)
    },
    NoneType: {
        FunctionType: lambda _: utils.noop,
        MethodType: lambda _: utils.Utils.noop
    }
}
