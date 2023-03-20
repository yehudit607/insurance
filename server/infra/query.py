from dataclasses import dataclass, field
from dataclasses_json import DataClassJsonMixin
from typing import Any, List, Optional, Type
from django.db.models import Q, Model
from enum import Enum

QUERY_OPS = {
    "EQ": "=",
    "NEQ": "!=",
    "IN": "in",
    "GT": ">",
    "GTE": ">=",
    "LT": "<",
    "LTE": "<=",
    "CONTAINS": "contains",
    "ICONTAINS": "icontains",
    "ISNULL": "isnull",
}

QueryOps = Enum(
    "QueryOps",
    {op: value for op, value in QUERY_OPS.items()}
    # Allow access through lowercase
    | {op.lower(): value for op, value in QUERY_OPS.items()}
    # Allow access through operator
    | {value: value for value in QUERY_OPS.values()},
)


@dataclass
class QueryDto(DataClassJsonMixin):
    field: str
    value: Any
    op: QueryOps = QueryOps["EQ"]


@dataclass
class FindRequestDto(DataClassJsonMixin):
    queries: List[QueryDto] = field(default_factory=list)
    offset: int = 0
    limit: Optional[int] = None
    order_by: Optional[str] = None
    include_deleted: bool = False

    def get_queryset(self, model: Type[Model], supported_query_fields: List[str]):
        filter_method = (
            model.objects.filter_with_deleted
            if self.include_deleted
            else model.objects.filter
        )
        qs = filter_method(self.__get_query(supported_query_fields))
        if self.order_by:
            qs = qs.order_by(self.order_by)

        if self.offset is not None and self.limit is not None:
            offset_to = self.offset + self.limit
            qs = qs[self.offset : offset_to]
        elif self.offset is not None:
            qs = qs[self.offset :]
        elif self.limit is not None:
            qs = qs[: self.limit]
        return qs

    def __get_query(self, supported_query_fields):
        query = Q()

        for q in self.queries:
            if q.field not in supported_query_fields:
                raise Exception(f"Unsupported filter: '{q.field}'")
            if q.op == QueryOps["EQ"]:
                query &= Q(**{q.field: q.value})
            elif q.op == QueryOps["NEQ"]:
                query &= ~Q(**{q.field: q.value})
            elif q.op == QueryOps["IN"]:
                query &= Q(**{q.field + "__in": q.value})
            elif q.op == QueryOps["GT"]:
                query &= Q(**{q.field + "__gt": q.value})
            elif q.op == QueryOps["GTE"]:
                query &= Q(**{q.field + "__gte": q.value})
            elif q.op == QueryOps["LT"]:
                query &= Q(**{q.field + "__lt": q.value})
            elif q.op == QueryOps["LTE"]:
                query &= Q(**{q.field + "__lte": q.value})
            elif q.op == QueryOps["CONTAINS"]:
                query &= Q(**{q.field + "__contains": q.value})
            elif q.op == QueryOps["ICONTAINS"]:
                query &= Q(**{q.field + "__icontains": q.value})
            elif q.op == QueryOps["ISNULL"]:
                query &= Q(**{q.field + "__isnull": q.value})
            else:
                raise Exception(f"Unsupported operator: '{q.op}")

        return query
