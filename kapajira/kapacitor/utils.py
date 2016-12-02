import json
import keyword

from collections import abc


class AlertDataParser:
    @staticmethod
    def parse(alert_data):
        alert_dict = json.loads(alert_data)
        return AlertData(alert_dict)


class AlertData:
    """ A read-only façade for navigating a AlertNode JSON object
        using attribute notation
    """

    def __new__(cls, arg):
        if isinstance(arg, abc.Mapping):
            return super().__new__(cls)
        elif isinstance(arg, abc.MutableSequence):
            return [cls(item) for item in arg]
        else:
            return arg

    def __init__(self, mapping):
        self.__dict__['_data'] = {}
        for key, value in mapping.items():
            if keyword.iskeyword(key):
                key += '_'
            self._data[key] = value

    def __getattr__(self, name):
        if hasattr(self._data, name):
            return getattr(self._data, name)
        else:
            return AlertData(self._data[name])

    def __setattr__(self, key, value):
        raise AttributeError('Attributes are read only')
