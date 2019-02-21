from python_wikibase.data_types.data_type import DataType


class GeoLocation(DataType):
    def __init__(self, py_wb, api, language):
        super().__init__(py_wb, api, language)
        self.latitude = None
        self.longitude = None
        self.altitude = None
        self.precision = 1 / 3600
        self.globe = None

    def unmarshal(self, data_value):
        coord_value = data_value["value"]
        self.latitude = coord_value["latitude"]
        self.longitude = coord_value["longitude"]
        self.altitude = coord_value["altitude"]
        self.precision = coord_value["precision"]
        self.globe = coord_value["globe"]
        return self

    def marshal(self):
        marshalled = {
            "latitude": self.latitude,
            "longitude": self.longitude,
            "precision": self.precision,
        }
        if self.altitude:
            marshalled["altitude"] = self.altitude
        if self.globe:
            marshalled["globe"] = self.globe
        return marshalled

    def create(self, latitude, longitude, altitude=None, precision=(1 / 3600), globe=None):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.precision = precision
        self.globe = globe
        return self
