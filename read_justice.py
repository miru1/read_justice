#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import urllib
import time

from bs4 import BeautifulSoup

server = "https://or.justice.cz/ias/ui/"
url = "https://or.justice.cz/ias/ui/rejstrik-$firma?jenPlatne=PLATNE&polozek=50&typHledani=STARTS_WITH&ico="
# ico = "03308235"
output_file = codecs.open("testfile1.txt", "w", "utf-8")
in_file = open("svj.txt", "r")

for ico in in_file.readlines():
    # get search page
    response = urllib.urlopen(url + ico).read()
    # print response
    soup = BeautifulSoup(response, "html.parser")
    time.sleep(1) # čekej 2 sekundy

    # find link to company page
    try:
        company_page_link = soup.find("ul", class_="result-links noprint").li.a.get('href')
    except:
        print "Chyba pro: ",ico

    # print company_page_link


    # get search page
    company_page = urllib.urlopen(server + company_page_link[2:]).read()
    # print company_page
    company = BeautifulSoup(company_page, "html.parser")

    table_row_divs = company.find_all("div", class_="vr-child")

    for table_row_div in table_row_divs:
        try:
            prop = table_row_div.find("div", class_="div-cell").getText().replace("\t", "").replace("\r", "").replace("\n", "")
            print "property:", prop
            # hledane1 = unicode("Identifikační číslo: ","utf-8")
            # hledane2 = unicode("Spisová značka: ","utf-8")
            # hledane3 = unicode("Název: ","utf-8")
            # if prop==hledane1 or prop==hledane2 or prop==hledane3 :

            val = table_row_div.find("div", class_="div-cell w45mm").parent.findNext('div').findNext('div').findNext('div').getText().replace("\t", "").replace("\r", "").replace("\n", "")

            # unicode("předseda výboru: ", "utf-8"), \
            # unicode("člen výboru: ", "utf-8"), \
            # unicode("předseda výboru: ", "utf-8"), \

            hledane_radky=[unicode("Identifikační číslo: ","utf-8"), \
                           unicode("Spisová značka: ","utf-8"), \
                           unicode("Datum vzniku: ","utf-8"), \
                           unicode("Název: ","utf-8")]
            if prop in hledane_radky:
                # output_file.write(prop)
                print "value:", val
                output_file.write(val)
                output_file.write(";")

            else:
                print "nic:", val
        except AttributeError:
            # print "Something missing", table_row_div
            pass
    output_file.write("\n")
output_file.close()
