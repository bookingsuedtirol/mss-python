from __future__ import annotations
from abc import ABC, abstractmethod

# from os import getenv
import xml.etree.ElementTree as ET
from src.request.types_mss import *  # might need change


class Method(ABC):
    def __init__(self, name: str, meth: Method) -> None:
        self.name = name
        self.method = meth

    @abstractmethod
    def get_base_xml(self, cred: Credentials, lang: Search):
        pass

    def get_method(name: str) -> Method:
        # if str=="getHotelList":
        return GetHotelList()


class GetHotelList(Method):
    def __init__(self) -> None:
        super().__init__("getHotelList", self)

    def get_base_xml(self, cred: Credentials, lang: Search) -> ET.Element:
        """
        Returns an XML (ElementTree) with the mandatory elements needed for the request.

        cred: XML Credentials Element (username, password, source)

        lang: XML Search Element with the language element defined
        """

        # USER = getenv("MSS_SERVICE_USERNAME")
        # PASSWORD = getenv("MSS_SERVICE_PASSWORD")
        # SOURCE = getenv("MSS_SERVICE_SOURCE")
        # temp = {}
        # temp["user"] = USER
        # temp["password"] = PASSWORD
        # temp["source"] = SOURCE

        # root = ET.Element("root")
        # headers = ET.SubElement(root, "header")
        # credentials = ET.SubElement(headers, "credentials")
        # for x in temp:
        #     ET.SubElement(credentials, x).text = temp[x]

        # ET.SubElement(
        #     ET.SubElement(ET.SubElement(root, "request"), "search"), "lang"
        # ).text = lang
        # # return ET.ElementTree(root)
        header = Header(cred, self.name)
        req = Request(lang)
        root = Root(header, req)
        return root.to_xml()
