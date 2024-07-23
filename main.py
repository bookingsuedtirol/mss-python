# import copy
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
from os import getenv
import xml.dom.minidom

from src.client import Client
from src.request.types_mss import *


def write_xml(root, filename):
    # Format the XML output using xml.dom.minidom
    xml_str = xml.dom.minidom.parseString(ET.tostring(root)).toprettyxml(indent="  ")

    # Write the formatted XML to a file
    with open(filename, "w") as file:
        file.write(xml_str)


def is_valid(xml: ET.Element, id=None, filename=None, file=False, print=False):
    """
    Compares the XML resultId with the expected one
    """
    if not file:
        return xml.find("header").find("result_id").text == id

    with open(filename, "r") as file:
        xml_content = file.read()

    expectedResultId = ET.fromstring(xml_content).find("header").find("result_id")

    if print == True:
        write_xml(xml, "response.xml")

    return xml.find("header").find("result_id").text == expectedResultId.text


if __name__ == "__main__":
    # TODO testo klasen klient, implemento naj funxion qe tshtosh elementet te XML-ja (elements parameters at Clients constructor)

    credentials = Credentials(
        getenv("MSS_SERVICE_USERNAME"),
        getenv("MSS_SERVICE_PASSWORD"),
        getenv("MSS_SERVICE_SOURCE"),
    )

    lang = "de"
    client = Client(credentials, lang)

    resp = client.request(None, getenv("MSS_SERVICE_URL"), "getHotelList")

    # print(ET.tostring(resp[0], "unicode"))

    # print(is_valid(resp, "407513bfca11b0591f9574b025d4caca"))
    print(is_valid(resp, "6ce97b163d6b035bfe90503e2e3b0da0"))  # new
