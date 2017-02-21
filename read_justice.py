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
in_file = open("svjk.txt", "r")
m_c = []

for ico in in_file.readlines():
    # get search page
    response = urllib.urlopen(url + ico).read()
    # print response
    soup = BeautifulSoup(response, "html.parser")
    time.sleep(1)  # čekej x sekund

    # find link to company page
    try:
        company_page_link = soup.find("ul", class_="result-links noprint").li.a.get('href')
    except:
        print ("Chyba pro: ", ico)

    # print company_page_link


    # get search page
    company_page = urllib.urlopen(server + company_page_link[2:]).read()
    # print company_page
    company = BeautifulSoup(company_page, "html.parser")

    table_row_divs = company.find_all("div", class_="vr-child")

    i = 0
    del m_c
    m_c = []
    m_pov = ""
    for table_row_div in table_row_divs:
        try:
            prop = table_row_div.find("div", class_="div-cell").getText().replace("\t", "").replace("\r", "").replace(
                "\n", "")
            val = table_row_div.find("div", class_="div-cell w45mm").parent.findNext('div').findNext('div').findNext(
                'div').getText().replace("\t", "").replace("\r", "").replace("\n", "")
            print "property:", prop, "=", val
            if prop == unicode("Identifikační číslo: ", "utf-8"):
                m_ic = val
            elif prop == unicode("Spisová značka: ", "utf-8"):
                m_sz = val
            elif prop == unicode("Název: ", "utf-8"):
                m_naz = val
            elif prop == unicode("Datum vzniku: ", "utf-8"):
                m_dv = val
            elif prop == unicode("Sídlo: ", "utf-8"):
                m_sidlo = val
            elif prop == unicode("předseda výboru: ", "utf-8"):
                m_pred = val
            elif prop == unicode("člen výboru: ", "utf-8"):
                i += 1
                m_c.append(val)
            elif prop == unicode("pověřený vlastník: ", "utf-8"):
                m_pov = val
            elif prop == unicode("místopředseda výboru: ", "utf-8"):
                m_mipred = val

        except AttributeError:
            # print "Something missing", table_row_div
            pass
        for
    rad = m_ic + ";" + m_sz + ";" + m_naz + ";" + m_dv + ";" + m_sidlo + ";" + m_pred + ";" + m_mipred + ";" + m_pov + ";" + m_c[1] + ";" + m_c[2] + ";" + m_c[3] + ";" + m_c[4] + ";kon;" + "\n"
    output_file.write(rad)
output_file.close()
