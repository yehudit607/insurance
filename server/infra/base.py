import abc
from dataclasses import dataclass
from enum import Enum
from functools import wraps

from dataclasses_json import dataclass_json, DataClassJsonMixin


class Choice(Enum):
    @classmethod
    def choices(cls):
        return tuple((field.name, field.value) for field in cls)

    @classmethod
    def values(cls):
        return [field.value for field in cls]

    @classmethod
    def has_value(cls, value):
        return value in cls.__members__.values()


@dataclass_json
@dataclass
class Falsy:
    """
    Used for determining whether a field was supplied to update/create DTOs.
    This is required since for many of the fields, None/empty strings/0/etc. are valid values
    that we wish to update.
    """

    def __bool__(self):
        return False

    # These functions are provided since we use Falsy for dict values as well.
    # The dataclass-json impl requires these functions on such values.
    @classmethod
    def keys(cls):
        return []

    @classmethod
    def values(cls):
        return []


MISSING = Falsy()


@dataclass_json
@dataclass
class OptionalFieldsMixin(abc.ABC):
    @classmethod
    def supplied(cls, attr):
        return attr is not MISSING


def dto_with_optional(cls_):
    @wraps(cls_)
    def wrap(cls):
        # Based on code in `dataclasses` and `dataclasses-json`
        cls.supplied = OptionalFieldsMixin.supplied
        return dataclass_json(dataclass(cls))

    return wrap(cls_)


@dataclass
class ModelToDtoMixin(DataClassJsonMixin):
    _field_override_mapping = {}

    @classmethod
    def from_record(cls, record_or_records, many: bool = False):
        if many:
            return [cls._from_record(record) for record in record_or_records]
        return cls._from_record(record_or_records)

    @classmethod
    def _from_record(cls, record):
        field_names = [f.name for f in fields(cls)]
        data = {
            field: getattr(record, cls._field_override_mapping.get(field, field))
            for field in field_names
        }
        return cls(**data)
