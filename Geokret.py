# -*- coding: utf-8 -*-

"""
Represent a Geokret
"""

# Geokrety Types IDs
GK_TYPE_TRADITIONAL = 0
GK_TYPE_BOOK = 1
GK_TYPE_HUMAN = 2
GK_TYPE_COIN = 3
GK_TYPE_STAMP = 4

# Geokrety Types conversion
GK_TYPES = {
    GK_TYPE_TRADITIONAL: u'Traditional',
    GK_TYPE_BOOK: u'Book/CD/DVD',
    GK_TYPE_HUMAN: u'Human',
    GK_TYPE_COIN: u'Coin',
    GK_TYPE_STAMP: u'Stamp'
}

# Geokrety Types reverse conversion
GK_TYPES_REV = {
    u'Traditional': GK_TYPE_TRADITIONAL,
    u'Book/CD/DVD': GK_TYPE_BOOK,
    u'Human': GK_TYPE_HUMAN,
    u'Coin': GK_TYPE_COIN,
    u'Stamp': GK_TYPE_STAMP,
}

# Geokrety description max chars
GK_DESCRIPTION_MAX = 5120

# Geokrety columns for csv exports
GK_CVS_COLUMNS = [
    "gk_id",
    "tracking_number",
    "name",
    "description",
    "imagehi",
    "images",
    "owner",
    "ownerid",
    "datecreated",
    "distance",
    "state",
    "type",
    "spotted_name",
    "spotted_type",
    "spotted_country",
    "country_track",
    "cache_count",
    "cache_rating",
]


class Geokret(object):
    """
    Object helper for representing a single Geokret
    """

    gk_id = 0
    tracking_number = None
    name = None
    description = None
    imagehi = None
    images = []
    owner = None
    ownerid = 0
    datecreated = None
    distance = None
    state = None
    type = None
    spotted_name = None
    spotted_type = None
    spotted_country = None
    country_track = []
    cache_count = 0
    cache_rating = None


    def __init__(self, **kwargs):
        """
        :param kwargs: dict, representing a Geokret
        :return: None
        """
        self.__dict__.update(kwargs)

    def gkid(self):
        """
        :return: Geokret ID converted to GKxxxx format
        """
        return ("GK%04x" % int(self.gk_id)).upper()

    def set_id(self, gk_id):
        """
        Set the Geokret ID
        :param gk_id: int, The Geokret ID
        :return: None
        """
        self.gk_id = int(gk_id)

    def set_tracking_number(self, tracking_number):
        """
        Set the Geokret Tracking Number
        :param tracking_number: string, The Geokret Tracking Number
        :return: None
        """
        self.tracking_number = tracking_number

    def set_name(self, name):
        """
        Set the Geokret Name
        :param name: String, The Geokret Name
        :return: None
        """
        self.name = name

    def set_type(self, gk_type):
        """
        Set the Geokret Type
        :param gk_type: int, The Geokret Type
        :return: None
        """
        self.type = gk_type

    def set_description(self, description):
        """
        Set the Geokret Description
        :param description: String, The Geokret Description
        :return: None
        """
        self.description = description[:GK_DESCRIPTION_MAX]

    def set_owner(self, owner):
        """
        Set the Geokret Owner Name
        :param owner: String, Geokret Owner Name
        :return: None
        """
        self.owner = owner

    def set_owner_id(self, ownerid):
        """
        Set the Geokret Owner ID
        :param ownerid: int, Owner ID
        :return: None
        """
        self.ownerid = int(ownerid)

    def set_date_released(self, datecreated):
        """
        Set the Geokret Creation date
        :param datecreated: string, creation date
        :return: None
        """
        self.datecreated = datecreated

    def set_distance(self, distance):
        """
        Set the Geokret distance
        :param distance: int, distance
        :return: None
        """
        self.distance = distance

    def set_featured_image(self, image):
        """
        Set the Geokret Featured image
        :param image: String, image name
        :return: None
        """
        self.imagehi = "http://geokrety.org/obrazki/" + image

    def add_image(self, image):
        """
        Append the Geokret Others Images.
        :param image: String, image
        :return: None
        """
        self.images.append("http://geokrety.org/obrazki/" + image)

    def set_spotted_cache_name(self, spotted_name):
        """
        Set the Geokret Spotted Cache ID
        :param spotted_name: String, cache ID
        :return: None
        """
        self.spotted_name = spotted_name

    def set_spotted_type(self, spotted_type):
        """
        Set the Geokret current Spotted status
        :param spotted_type: String, status
        :return: None
        """
        self.spotted_type = spotted_type

    def set_spotted_country(self, spotted_country):
        """
        Set the Geokret current Spotted country
        :param spotted_country: String, country initials
        :return: None
        """
        self.spotted_country = spotted_country

    def set_country_track(self, country_track):
        """
        Set the Geokret Country history
        :param country_track: Array of tuples, [(String:country, int:count)]
        :return: None
        """
        self.country_track = country_track

    def set_cache_count(self, cache_count):
        """
        Set the Geokret Cache Count Visited
        :param cache_count: int, visited cache count
        :return: None
        """
        self.cache_count = cache_count

    def set_cache_rating(self, cache_rating):
        """
        Set the Geokret Rating
        :param cache_rating: tuple, (int:vote count, float:score)
        :return: None
        """
        self.cache_rating = cache_rating

    def __str__(self):
        """
        return Geokret string representation
        :return: String
        """
        gkid = self.gkid()
        return u"<__Geokrety__: %s %s: %s>" % (
            self.name,
            gkid,
            str(self.__dict__))


if __name__ == "__main__":
    GKDEF = {
        "id": 18,
        "name": "Kret Name",
        "description": "Kret Long Description",
        "images": []
    }

    GEOKRET = Geokret(**GKDEF)
    print GEOKRET
