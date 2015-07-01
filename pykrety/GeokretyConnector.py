# -*- coding: utf-8 -*-

"""
Abstraction around Geokrety.org.

It try to parse pages to extract values.
"""

import os
import csv
import requests
import urllib
import urllib2
import urlparse

from Geokret import Geokret, GK_CVS_COLUMNS
from parsers.GeokretyHTMLHandler import parse_html_owned, parse_html_geokret
from parsers.GeokretyXMLHandler import parse_xml_stream


URL = "https://geokrety.org"


def format_filename(s):
    """
    Take a string and return a valid filename constructed from the string.
    Uses a whitelist approach: any characters not present in valid_chars are
    removed. Also spaces are replaced with underscores.

    Note: this method may produce invalid filenames such as ``, `.` or `..`
    When I use this method I prepend a date string like '2009_01_15_19_46_32_'
    and append a file extension like '.txt', so I avoid the potential of using
    an invalid filename.

    https://gist.github.com/seanh/93666
    """
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ','_') # I don't like spaces in filenames.
    return filename


class GeokretyConnector(object):
    """
    Connector for geokrety.org.

    When retrieving multiple items, they will be stored in self.inventory
    """
    credentials = {'login': None, 'password': None}
    secid = None
    cookie = None
    inventory = []
    session = None
    connected = False

    def __init__(self, login, password):
        """
        Initialize the connector. Need credentials from Geokrety.org

        :param login: string
        :param password: string
        :return: None
        """
        self.session = requests.session()

        self.credentials['login'] = login
        self.credentials['password'] = password

    def connect_api(self):
        """
        Retrieve secid to be used by API calls

        :return: None
        """
        path = "/api-login2secid.php"
        data = urllib.urlencode(self.credentials)

        req = urllib2.Request(URL + path, data)
        response = urllib2.urlopen(req)
        if response.getcode() == requests.codes.ok:
            self.secid = response.read().rstrip('\n\r ')
        else:
            print 'E: Cannot connect'

    def connect_web(self):
        """
        Connect to Geokrety.org, store received cookies for future
        authenticated calls.

        :return: None
        """
        path = '/longin.php'
        params = {
            'login': self.credentials['login'],
            'haslo1': self.credentials['password'],
            'remember': '1',
        }

        response = self.session.post(
            URL + path, data=params, verify=False,
            allow_redirects=False)

        if response.status_code == requests.codes.found:
            # print response.text
            if self.session.cookies:
                print "Connected: %s" % response.status_code
                self.connected = True
            else:
                print "Not Connected: %s" % response.status_code
        else:
            print "Not Connected: %s" % response.status_code

    def get_inventory(self):
        """
        Retrieve the user inventory via API call.

        :return: None
        """
        if self.secid is None:
            print 'E: Must be connected'
            return

        path = '/export2.php?secid=%s&inventory=1' % self.secid
        self.inventory = parse_xml_stream(URL + path)

    def get_inventory_web(self, user_id=None):
        """
        Retrieve inventory for user_id.
        Parse the Web pages.

        :param user_id: int, optional, default to connected user
        :return: None
        """
        path = '/mypage.php?co=1&page=0'
        if user_id:
            path += '&userid=%d' % int(user_id)

        response = self.session.get(
            URL + path, verify=False,
            allow_redirects=False)

        if response.status_code == requests.codes.ok:
            self.inventory = parse_html_owned(response.text)
            print 'I: Geokrety inventory retrieved'
        else:
            print 'E: Failed to retrieve Geokrety inventory'

    def get_geokret_details_web(self, gk_id):
        """
        Retrieve full details for a Geokret.
        Parse the Web pages.

        :param gk_id: int, Geokret ID
        :return: None
        """
        path = '/konkret.php?id=%d&page=0' % gk_id

        response = self.session.get(
            URL + path, verify=False,
            allow_redirects=False)

        if response.status_code == requests.codes.ok:
            print 'I: Geokret details retrieved'
            return parse_html_geokret(response.text)
        else:
            print 'E: Failed to retrieve Geokret details'

    def update_geokret_web(self, geokret):
        """
        Update a Geokret, via form post.
        Authentication mandatory.

        :param geokret: Geokret object
        :return: None
        """
        path = '/edit.php'

        if not isinstance(geokret, Geokret):
            print 'E: geokret is not a Geokrety instance'
            return False

        if not self.connected:
            print 'E: you must be connected.'
            return False

        params = {
            'id': geokret.gk_id,
            'nazwa': geokret.name,
            'opis': geokret.description,
            'typ': geokret.type
        }

        response = self.session.post(URL + path, data=params, verify=False)
        if response.history:
            print "I: Geokret updated."
        else:
            print "E: Failed to updated Geokret."

    def upload_image_web(self, geokret, image_filename,
                         description=None, avatar=False):
        """
        Upload a picture for a Geokret.
        Authentication mandatory.

        :param geokret: Geokret object
        :param image_filename: image file to upload
        :param description: String, optional image description
        :param avatar: Boolean, set image as featured
        :return: None
        """
        if not isinstance(geokret, Geokret):
            print 'E: geokret is not a Geokrety instance'
            return False

        if not os.path.isfile(image_filename):
            print "E: file %s doesn't exists" % image_filename
            return False

        if not self.connected:
            print 'E: you must be connected.'
            return False

        path = '/imgup.php?typ=0&id=%d' % geokret.gk_id
        params = dict()

        if description:
            params['opis'] = description
        if avatar:
            params['avatar'] = 'true'

        with open(image_filename, 'rb') as filename:
            response = self.session.post(URL + path,
                                         data=params,
                                         files={'obrazek': (
                                             'cgeo.png', filename,
                                             'image/png',
                                             {'Expires': '0'}
                                         )},
                                         verify=False)
            if response.history:
                print "I: Geokret image uploaded."
            else:
                print "E: Failed to upload Geokret image."

    def create_geokret_web(self, geokret, logathome=False):
        """
        Create a new Geokret from a Geokret instance.
        Authentication mandatory.

        Todo: May upload pictures if some are defined...

        :param geokret: Geokret object
        :param logathome: Boolean, set the initial position to user's home
        :return: None
        """
        if not isinstance(geokret, Geokret):
            print 'E: geokret is not a Geokrety instance'
            return False

        if not self.connected:
            print 'E: you must be connected.'
            return False

        path = '/register.php'
        params = dict()
        params['nazwa'] = geokret.name
        params['typ'] = geokret.type
        params['opis'] = geokret.description
        if logathome:
            params['logAtHome'] = 1

        response = self.session.post(URL + path,
                                     data=params,
                                     verify=False)
        if response.history:
            print "I: Geokret created."
            geokret.set_id(response.url.split('=')[1])
            return geokret
        else:
            print "E: Failed to create Geokret."

    def write_csv(self, filename):
        """
        Export Geokret inventory as CSV.

        :param filename: String, output csv filename
        :return: None
        """
        if not filename:
            print "E: writefile(): no filename provided"
            return

        with open(filename, 'wb') as csvfile:
            writer = csv.DictWriter(csvfile, GK_CVS_COLUMNS, delimiter=';')
            writer.writeheader()
            for geokret in self.inventory:
                writer.writerow(geokret.__dict__)

    def read_csv(self, filename):
        """
        Import Geokret inventory from CSV.

        :param filename:  String, input csv filename
        :return: None
        """
        self.inventory = []

        if not filename:
            print "E: readfile(): no filename provided"
            return

        with open(filename, 'rb') as csvfile:
            reader = csv.DictReader(csvfile, GK_CVS_COLUMNS, delimiter=';')
            reader.next()
            for row in reader:
                geokret = Geokret(**row)
                self.inventory.append(geokret)

    def download_to_file(self, url, destination_directory):
        """
        Download specified url to the specified file

        :param url: relative path to download file
        :param destination: destination file
        :return: None
        """

        filename = format_filename(os.path.basename(urlparse.urlsplit(url).path))

        # make directories
        os.makedirs(os.path.dirname(destination_directory))

        # download the file
        with open(destination_directory + '/' + filename, 'wb') as handle:
            response = requests.get(url, stream=True)

            if not response.ok:
                raise "Failed to download: " + url

            for block in response.iter_content(1024):
                handle.write(block)



if __name__ == "__main__":
    print "Geokrety.org Connector Factory"

    login = "myusername"
    password = "mysuperpassword"
    gkConn = GeokretyConnector(login, password)
    #gkConn.connect_api()
    gkConn.connect_web()

    #gkConn.get_inventory()
    gkConn.get_inventory_web()

    #for gk in gkConn.inventory:
    #    print gk.gkid() + " -- " + unicode(gk)

    #gk46684 = gkConn.get_geokret_details_web(46684)
    #print gk46684
    #gkConn.update(gk46684)
    #gkConn.upload_image_web(gk46684, '/home/kumy/Bureau/cgeo.png',
    # description='python upload test', avatar=True)

    ##gkConn.create_geokret_web(gk46684, logathome=True)

    gkConn.write_csv('/tmp/pykrety-out.csv')
    #gkConn.read_csv('/tmp/pykrety-out.csv')

    for gk in gkConn.inventory:
        print gk.gkid() + " -- " + unicode(gk)
