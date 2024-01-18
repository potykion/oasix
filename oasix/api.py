from typing import Type, Union, Optional

import attr


@attr.s
class Req(object):
    query = attr.ib(type=Optional[Union[dict, Type]], default=None)
    json = attr.ib(type=Optional[Union[dict, Type]], default=None)
    form = attr.ib(type=Optional[Union[dict, Type]], default=None)


@attr.s
class Schema(object):
    req = attr.ib(type=Optional[Req], default=None)
    resp = attr.ib(type=Optional[dict], default=None)


class MakeOpenApi:
    def __call__(self, sch):
        ...
