import datetime

import attr
from adlkit_internal.common.utils import get_new_uid


@attr.s(slots=True)
class DataPoint(object):
    source_name = attr.ib(converter=str)
    source_type = attr.ib(converter=str)
    index = attr.ib(converter=str)

    data_set_list = attr.ib()

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)


@attr.s(slots=True)
class LabelInstance(object):
    data_point_uid = attr.ib(converter=str)
    label_uid = attr.ib(converter=str)

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)


@attr.s(slots=True)
class Label(object):
    name = attr.ib(converter=str)
    comment = attr.ib(converter=str, default='')
    is_origin = attr.ib(type=bool, default=False)

    uid = attr.ib(default=attr.Factory(get_new_uid), converter=str)
    timestamp = attr.ib(default=attr.Factory(datetime.datetime.utcnow), type=datetime.datetime)
