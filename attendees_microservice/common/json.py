from json import JSONEncoder
from datetime import datetime
from django.db.models import QuerySet


class QuerySetEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, QuerySet):
            return list(o)
        else:
            return super().default(o)


class DateEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, datetime):
            return o.isoformat()
        else:
            return super().default(o)


class ModelEncoder(DateEncoder, QuerySetEncoder, JSONEncoder):
    encoders = {}

    def default(self, o):
        # if the object to decode is the same class as what
        # is in the model property, then
        if isinstance(o, self.model):
            # create an empty dict that will hold the property names
            # as keys and the property values as values
            the_dictionary = {}
            # for each name in the properties list
            # if o has the attribute get_api_url
            #    then add its return value to the dictionary
            #    with the key "href"
            if hasattr(o, "get_api_url"):
                the_dictionary["href"] = o.get_api_url()
            for property in self.properties:
                # get the value of that property from the model
                # instance given just the property name
                value = getattr(o, property)
                if property in self.encoders:
                    encoder = self.encoders[property]
                    value = encoder.default(value)
                the_dictionary[property] = value
            the_dictionary.update(self.get_extra_data(o))
            return the_dictionary
        else:
            return super().default(o)

    def get_extra_data(self, o):
        return {}



