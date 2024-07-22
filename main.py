# import copy
import requests
import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
from os import getenv
import xml.dom.minidom

# from typing import Literal
from dataclasses import dataclass, field

from src.client import Client
from src.request.types_mss import Credentials


def make_xml_request(data: ET.Element, url: str, method: str) -> requests.Response:
    """
    Makes a post request to the given URL with the specified data and method name.

    data: ElementTree with the data required in the XML
    url: Service URL
    method: Method to be executed by the service
    """
    ET.SubElement(data.find("header"), "method").text = method
    return requests.post(
        url,
        data=ET.tostring(data, encoding="unicode"),
        headers={"Content-Type": "application/xml"},
    )


def get_base_xml() -> ET.Element:
    """
    Returns an XML (ElementTree) with the mandatory elements needed for the request.
    """
    load_dotenv()
    USER = getenv("MSS_SERVICE_USERNAME")
    PASSWORD = getenv("MSS_SERVICE_PASSWORD")
    SOURCE = getenv("MSS_SERVICE_SOURCE")
    temp = {}
    temp["user"] = USER
    temp["password"] = PASSWORD
    temp["source"] = SOURCE

    root = ET.Element("root")
    headers = ET.SubElement(root, "header")
    credentials = ET.SubElement(headers, "credentials")
    for x in temp:
        ET.SubElement(credentials, x).text = temp[x]

    ET.SubElement(
        ET.SubElement(ET.SubElement(root, "request"), "search"), "lang"
    ).text = "de"
    # return ET.ElementTree(root)
    return root


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


def validator(x):
    print("vali")
    if x not in ["yellow", "blue"]:
        raise ValueError(f"Invalid value: {x}")
    return x


@dataclass
class A:
    name2: str = field(default=None, metadata={"validaton": validator})
    name: str = field(default=None)


if __name__ == "__main__":
    # try:
    # resp = make_xml_request(get_base_xml(), getenv("MSS_SERVICE_URL"), "getHotelList")
    # root = ET.fromstring(resp.content)

    # print(is_valid(root, file=True, filename="./XML-samples/MSS_Hotel-List-1721202439420.xml"))

    # TODO testo klasen klient, implemento naj funxion qe tshtosh elementet te XML-ja (elements parameters at Clients constructor)

    credentials = Credentials(
        getenv("MSS_SERVICE_USERNAME"),
        getenv("MSS_SERVICE_PASSWORD"),
        getenv("MSS_SERVICE_SOURCE"),
    )
    client = Client(credentials, "de")
    # data = ET.Element("Header")
    # SubElement()
    resp = client.request(None, getenv("MSS_SERVICE_URL"), "getHotelList")

    print(is_valid(resp, "407513bfca11b0591f9574b025d4caca"))
