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


# def convert_numerics_to_strings(obj):
#     for attr, value in obj.__dict__.items():
#         if isinstance(value, (int, float)):
#             setattr(obj, attr, str(value))


# right now im filling XML's request/search parameters
# check this out for XML values  https://easychannel.it/mss/docs/index.php?VERSION=2.0&function=getHotelList&mode=0
def get_search_items(lang):
    # ids of hotels, js type is numbers[], what should it store?
    ids = ["10038"]  # or maybe a list instead?

    id_ofchannel = "hgv"

    # search hotel
    # with ET.Element("search_hotel") as search_hotel:
    #     ET.SubElement(search_hotel, "name").text = "hotel"
    #     ET.SubElement(search_hotel, "type").text = HotelType.Hotel
    #     search_hotel.append(Stars(1, 5))

    search_hotel = SearchHotel(
        "name", HotelType.Hotel, Stars("1", "5"), HotelFeature.Bar, HotelTheme.Family
    )

    search_location = SearchLocation(
        [], []
    )  # stores a list of numbers and list of strings

    search_offer = SearchOffer(
        "2024-07-23",
        "2024-07-30",
        Board.HalfBoard,
        [Room("1", ["18", "18"])],
        RoomFeature.Balcony,
        ["hgv", "bok", "htl"],
        SearchOfferType.NoReference,
        Rateplan("1", "hgv"),
    )

    # search_distance = SearchDistance()

    # room_type = RoomType.Apartment
    # feature_id =

    search_lts = SearchLts()

    return Search(
        lang,
        id=ids,
        search_hotel=search_hotel,
        search_location=search_location,
        search_offer=search_offer,
        search_lts=search_lts,
    )


if __name__ == "__main__":
    # TODO testo klasen klient, implemento naj funxion qe tshtosh elementet te XML-ja (elements parameters at Clients constructor)

    credentials = Credentials(
        getenv("MSS_SERVICE_USERNAME"),
        getenv("MSS_SERVICE_PASSWORD"),
        getenv("MSS_SERVICE_SOURCE"),
    )

    lang = "de"
    client = Client(credentials, lang)

    search_items = get_search_items(lang)
    resp = client.request(
        get_search_items(lang), getenv("MSS_SERVICE_URL"), "getHotelList"
    )

    # client.addSearch(search_items)

    # print(ET.tostring(search_items.to_xml(), "unicode"))

    # print(ET.tostring(resp[0], "unicode"))

    # print(is_valid(resp, "407513bfca11b0591f9574b025d4caca"))
    # print(is_valid(resp, "6ce97b163d6b035bfe90503e2e3b0da0")) #new
    print(is_valid(resp, "8b21849ef48659f7494383df17e4a962"))  # neww
