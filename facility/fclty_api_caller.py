import requests
from bs4 import BeautifulSoup
import xmltodict
from pickle import *


class FcltyCaller:
    def __init__(self):
        data = {}
        with open("secret_data.pickle", "rb") as sd:
            data = load(sd)
        self.service_key = data.get("service_key")

    def get_id_list(self, row):
        url = "http://www.kopis.or.kr/openApi/restful/prfplc"
        params = {
            'service': self.service_key,
            'cpage': 1,
            'rows': row
        }
        response = requests.get(url, params=params).text

        xmlobj = BeautifulSoup(response, 'lxml-xml')

        list = [id.string for id in xmlobj.find_all("mt10id")]

        return list

    def get_facility(self, fclty_id):
        url = "http://www.kopis.or.kr/openApi/restful/prfplc/{0}".format(
            fclty_id)
        params = {
            'service': self.service_key
        }

        response = requests.get(url, params=params).text
        xmlobj = BeautifulSoup(response, 'lxml-xml').find("db")
        data = {}
        data["facility_id"] = xmlobj.find("mt10id").string
        data["facility_name"] = xmlobj.find("fcltynm").string
        data["facility_telno"] = xmlobj.find(
            "telno").string if xmlobj.find("telno").string != ' ' else None
        data["facility_relateurl"] = xmlobj.find(
            "relateurl").string if xmlobj.find("relateurl").string != ' ' else None
        data["facility_address"] = xmlobj.find("adres").string
        data["facility_latitude"] = float(xmlobj.find("la").string)
        data["facility_longitude"] = float(xmlobj.find("lo").string)

        return data
