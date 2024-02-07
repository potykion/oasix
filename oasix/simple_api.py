import typing
from typing import Any, Optional


def make_swagger(
    form=None,  # type: dict[str, Any] | None
    headers=None,  # type: dict[str, Any] | None
):
    # type: (...) -> dict
    """
    https://github.com/flasgger/flasgger?tab=readme-ov-file#using-dictionaries-as-raw-specs
    https://github.com/swagger-api/swagger.io/blob/wordpress/docs/spec-explained/basic-structure.md
    https://github.com/swagger-api/swagger.io/blob/wordpress/docs/spec-explained/parameters.md
    https://github.com/OAI/OpenAPI-Specification/blob/main/versions/2.0.md#fixed-fields-7

    >>> actual = make_swagger(
    ...     form=dict(
    ...         device_token=Optional[str],
    ...         device_token_hms=Optional[str],
    ...     ),
    ...     headers={
    ...         "Client-Id": str,
    ...         "User-Agent": str,
    ...     },
    ... )
    >>> expected = {
    ...   "parameters": [
    ...       {"in": "formData", "name": "device_token", "type": "string"},
    ...       {"in": "formData", "name": "device_token_hms", "type": "string"},
    ...       {"in": "header", "name": "Client-Id", "type": "string", "required": True},
    ...       {"in": "header", "name": "User-Agent", "type": "string", "required": True},
    ...   ]
    ... }
    >>> actual == expected
    True
    """
    schema = {}

    if form or headers:
        schema["parameters"] = []
    if form:
        schema["parameters"].extend(_parse_params(form, "formData"))
    if headers:
        schema["parameters"].extend(_parse_params(headers, "header"))

    return schema


def _parse_params(raw_params, in_):
    """
    >>> parsed = _parse_params(dict(
    ...         device_token=Optional[str],
    ...         device_token_hms=Optional[str],
    ...     ), "formData")
    >>> exp = [
    ...       {"in": "formData", "name": "device_token", "type": "string"},
    ...       {"in": "formData", "name": "device_token_hms", "type": "string"},
    ... ]
    >>> parsed == exp
    True
    """
    parsed_params = []
    for field, field_type in raw_params.items():
        param = {
            "in": in_,
            "name": field,
        }

        type_and_meta = _map_py_type_to_swag(field_type)
        param.update(type_and_meta)

        parsed_params.append(param)
    return parsed_params


def _map_py_type_to_swag(py_type):
    """
    >>> _map_py_type_to_swag(str)
    {'type': 'string', 'required': True}
    >>> _map_py_type_to_swag(Optional[str])
    {'type': 'string'}
    """
    if py_type is str:
        return {"type": _map_simple_py_type_to_swag(py_type), "required": True}
    is_optional = (
        typing.get_origin(py_type) is typing.Union
        and len(typing.get_args(py_type)) == 2
        and any((t is type(None)) for t in typing.get_args(py_type))
    )
    if is_optional:
        return {"type": _map_simple_py_type_to_swag(_get_optional_type(py_type))}


def _map_simple_py_type_to_swag(simple_py_type):
    if simple_py_type is str:
        return "string"


def _get_optional_type(optional_union):
    """
    >>> _get_optional_type(Optional[str])
    <class 'str'>
    """
    return next(type for type in typing.get_args(optional_union) if type is not None)
