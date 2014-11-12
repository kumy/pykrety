# -*- coding: utf-8 -*-

"""
Parser around HTML from Geokrety.org
"""

import BeautifulSoup
import re

import Geokret


def parse_html_geokret(html):
    """
    Parse of Geokrety HTML page: /konkret.php

    :param html: the html full page
    :return: The Geokret
    """
    soup = BeautifulSoup.BeautifulSoup(html)
    tables = soup.findAll('table')

    geokret = Geokret.Geokret()

    infos = tables[0]
    details = tables[1]
    # links = tables[2]
    #carte = tables[3]
    #moves = tables[4] # table may not exists see 46684

    ### TABLE INFOS
    infos_tr = infos.findAll('tr')
    i = 0

    geokret.set_name(infos_tr[i].strong.text)

    matchObj = re.match(r'^GeoKret.*\((.+)\) by.*$', infos_tr[i].text)
    geokret.set_type(Geokret.GK_TYPES_REV[matchObj.group(1)])

    geokret.set_owner(infos_tr[i].a.text)
    geokret.set_owner(infos_tr[i].a.text)
    geokret.set_owner_id(infos_tr[i].a['href'].split('=')[1])
    i += 1

    geokret.set_id(int(infos_tr[i].findAll('td')[1].text.replace('GK', ''), 16))
    i += 1

    if infos_tr[i].findAll('td')[0].text == 'Tracking Code:':
        geokret.set_tracking_number(infos_tr[i].findAll('td')[1].text)
        i += 1

    geokret.set_distance(infos_tr[i].findAll('td')[1].text.replace(' km', ''))
    i += 1

    geokret.set_cache_count(infos_tr[i].findAll('td')[1].text)
    i += 2

    flags = []
    country = None
    for flag in infos_tr[i].findAll('td')[1].findAll():
        if flag.name == 'img':
            country = flag['alt']
        if flag.name == 'span':
            countrycount = flag.text.replace('(', '').replace(')', '')
            flags.append((country, countrycount))
    geokret.set_country_track(flags)
    i += 1

    # Rating...
    matchObj = re.match(r'^votes: (\d+), average rating: (.+)\. You .*$',
                        infos_tr[i].findAll('td')[1].find('span').text)
    geokret.set_cache_rating((matchObj.group(1), matchObj.group(2)))

    ### TABLE INFOS END



    ### TABLE DETAILS
    details_tr = details.findAll('tr')
    i = 1

    geokret.set_description(details_tr[i].findAll('td')[0].text)
    i += 2

    try:
        geokret.set_featured_image(
            details_tr[i].findAll('td')[0].findAll('span', attrs={'class': 'obrazek_hi'})[0].a['href'])
    except Exception, e:
        pass  # No featured image
    geokret.add_image(details_tr[i].findAll('td')[0].findAll('span', attrs={'class': 'obrazek'})[0].a['href'])
    ### TABLE DETAILS END


    #### TABLE MOVES
    #moves_tr = moves.findAll('tr')
    #i = 1
    #
    #pprint.pprint(moves_tr[i].findAll('td'))
    #
    #### TABLE MOVES END

    return geokret


def parse_html_owned(html):
    """
    Parse of Geokrety HTML page: /mypage.php

    :param html: the html full page
    :return: Geokret array
    """
    soup = BeautifulSoup.BeautifulSoup(html)
    mg0 = soup.findAll('tr', attrs={'class': u'mg0'})
    mg1 = soup.findAll('tr', attrs={'class': u'mg1'})
    gks = mg0 + mg1

    geokrety = []
    for gk in gks:
        geokret = Geokret.Geokret()
        tds = gk.findAll('td')

        try:
            geokret.set_spotted_type(tds[0].span['title'])
            geokret.set_id(tds[1].a['href'].split('=')[1])
            geokret.set_name(tds[1].span.text)
            geokret.set_distance(tds[4].text.replace('km', ''))
            geokret.set_cache_count(tds[5].text)

            try:
                geokret.set_tracking_number(tds[6].findAll('a')[1]['href'].split('=')[1])
            except IndexError:
                pass

            if tds[1].img:
                geokret.set_featured_image(tds[1].img['title'].split('|')[3])

            if tds[2].text:
                geokret.set_spotted_country(tds[2].img['alt'])
                geokret.set_spotted_cache_name(tds[2].a.text)
        except Exception, e:
            print "E: cannot parse %s ; %s" % (geokret.gkid(), e)

        geokrety.append(geokret)

    return geokrety


if __name__ == '__main__':
    html_file = 'geokret_details2.html'
    geokrety = parse_html_geokret(open(html_file, 'r'))
    print unicode(geokrety)
