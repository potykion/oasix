from typing import List

import attr
import pytest

from oasix.api import Schema, Req, MakeOpenApi


@attr.s
class SearchQuery(object):
    q = attr.ib(type=str)


@attr.s
class SelectOption(object):
    value = attr.ib(type=int)
    label = attr.ib(type=str)


@pytest.mark.parametrize(
    [
        "raw_sch",
    ],
    [
        [
            Schema(
                req=Req(
                    query=SearchQuery,
                ),
                resp={200: List[SelectOption]},
            )
        ],
        [
            Schema(
                req={
                    "query": {"q": str},
                },
                resp={
                    200: List[{"value": int, "label": str}],
                },
            )
        ],
    ],
)
def test_MakeOpenApi(raw_sch):
    sch = MakeOpenApi()(raw_sch)
    expected_schema = {
        "parameters": [
            {
                "name": "q",
                "in": "query",
                "schema": {"type": "integer"},
            }
        ],
        "responses": {
            "200": {
                "description": "A list of objects",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "value": {"type": "integer"},
                                    "label": {"type": "string"},
                                },
                                "required": ["value", "label"],
                            },
                        }
                    }
                },
            }
        },
    }
    assert sch == expected_schema
