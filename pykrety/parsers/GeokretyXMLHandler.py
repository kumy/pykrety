# -*- coding: utf-8 -*-

"""
Parser around XML from Geokrety.org API
"""

import xml.sax

from pykrety import Geokret


class GeokretyXMLHandler(xml.sax.ContentHandler):
    """
    Parse of Geokrety XML from API
    """
    content = ''
    geokret = None
    geokrety = []

    def startElement(self, name, attrs):
        """
        Match a begin element.

        :param name: string
        :param attrs: dict
        :return: None
        """
        if name == "geokret":
            self.geokret = Geokret.Geokret()
            self.geokrety.append(self.geokret)
            for (key, value) in attrs.items():
                if key == 'id':
                    self.geokret.set_id(value)
                if key == 'dist':
                    self.geokret.set_distance(value)
                if key == 'nr':
                    self.geokret.set_tracking_number(value)
                if key == 'type':
                    self.geokret.set_type(value)
                if key == 'waypoint':
                    self.geokret.set_spotted_cache_name(value)
                if key == 'image':
                    self.geokret.add_image(value)
        if name == "owner":
            for (key, value) in attrs.items():
                if key == 'owner':
                    self.geokret.set_owner(value)
        if name == "type":
            for (key, value) in attrs.items():
                if key == 'type':
                    self.geokret.set_type(value)

    def endElement(self, name):
        """
        Match end element.

        :param name: string
        :return: None
        """
        if name == 'geokret':
            if self.content:
                self.geokret.set_name(self.content)

        if name == 'name':
            self.geokret.set_name(self.content)

        if name == 'description':
            self.geokret.set_description(self.content)

        if name == 'owner':
            self.geokret.set_owner(self.content)

        if name == 'datecreated':
            self.geokret.set_date_released(self.content)

        if name == 'distancetravelled':
            self.geokret.set_distance(self.content)

        if name == 'image':
            self.geokret.set_spotted_type(self.content)

        if name == 'waypoint':
            self.geokret.set_spotted_type(self.content)
            self.geokret.set_spotted_cache_name(self.content)

    def characters(self, content):
        """
        Match element content.

        :param content: string
        :return: None
        """
        self.content = content.rstrip('\n\r ')


def parse_xml_file(xml_filename):
    """
    Parse from xml filename.

    :param xml_filename: String
    :return: The GeokretyXMLHandler
    """
    return parse_xml_stream(open(xml_filename, 'rb'))


def parse_xml_stream(stream):
    """
    Parse from xml stream.

    :param stream: file object
    :return: The GeokretyXMLHandler
    """
    parser = xml.sax.make_parser()
    handler = GeokretyXMLHandler()
    parser.setContentHandler(handler)
    parser.parse(stream)
    return handler.geokrety


if __name__ == '__main__':
    xml_file = 'geokret141_xml.xml'
    parse_xml_file(xml_file)
