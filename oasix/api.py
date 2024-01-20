import typing
from typing import Type

import attr


def make_openapi(
    query: Type | dict | None = None,
    body=None,
    form=None,
    responses: dict[int, Type] = None,
):
    spec = {}
    if query or body or form:
        parameters = []
        if query:
            if attr.has(query):
                query = _attrs_to_type_dict(query)

            if isinstance(query, dict):
                for key, type_ in query.items():
                    parameters.append(
                        {
                            "in": "query",
                            "name": key,
                            "schema": {"type": _type_to_openapi(type_)},
                        }
                    )

        spec["parameters"] = parameters

        if responses:
            spec_responses = {}
            for status, resp in responses.items():
                schema = {}
                if typing.get_origin(resp) is list:
                    schema["type"] = "array"
                    schema["items"] = {}

                    list_arg = typing.get_args(resp)[0]
                    if attr.has(list_arg):
                        list_arg = _attrs_to_type_dict(list_arg)

                    if isinstance(list_arg, dict):
                        schema["items"]["type"] = "object"
                        schema["items"]["properties"] = (properties := {})
                        for key, type_ in list_arg.items():
                            properties[key] = {"type": _type_to_openapi(type_)}

                spec_responses[str(status)] = {
                    "content": {"application/json": {"schema": schema}}
                }

            spec["responses"] = spec_responses

        return spec


def _attrs_to_type_dict(attrs_cls):
    type_dict = attr.fields_dict(attrs_cls)
    type_dict = {key: field.type for key, field in type_dict.items()}
    return type_dict


def _type_to_openapi(type):
    """
    >>> _type_to_openapi(int)
    'integer'
    """
    if type is str:
        return "string"
    if type is int:
        return "integer"
