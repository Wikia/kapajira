import json
from collections import abc


class AlertDataParser:
    @classmethod
    def parse(cls, alert_data):
        alert_dict = json.loads(alert_data)
        return AlertData(alert_dict)


class AlertData:
    """ A read-only façade for navigating a AlertNode JSON object
        using attribute notation
    """

    def __init__(self, mapping):
        self._data = dict(mapping)

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            return AlertData.build(self._data[name])

    @classmethod
    def build(cls, obj):
        if isinstance(obj, abc.Mapping):
            return cls(obj)

        elif isinstance(obj, abc.MutableSequence):
            return [cls.build(item) for item in obj]
        else:
            return obj
