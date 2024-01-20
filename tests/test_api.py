from typing import List

import attr
import pytest

from oasix.api import make_openapi


@attr.s
class SearchQuery(object):
    q = attr.ib(type=str)


@attr.s
class SelectOption(object):
    value = attr.ib(type=int)
    label = attr.ib(type=str)


@pytest.mark.parametrize(
    ["raw_sch"],
    [
        [
            dict(
                query={"q": str},
                responses={
                    200: List[{"value": int, "label": str}],
                },
            )
        ],
        [
            dict(
                query=SearchQuery,
                responses={200: List[SelectOption]},
            )
        ],
    ],
)
def test_make_openapi(raw_sch):
    sch = make_openapi(**raw_sch)
    expected_schema = {
        "parameters": [
            {
                "name": "q",
                "in": "query",
                "schema": {"type": "string"},
            }
        ],
        "responses": {
            "200": {
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
                            },
                        }
                    }
                },
            }
        },
    }
    assert sch == expected_schema
