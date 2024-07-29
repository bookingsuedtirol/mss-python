import xml.etree.ElementTree as ET
from dotenv import load_dotenv

load_dotenv()
from os import getenv
import xml.dom.minidom

from src.client import Client
from src.request.types_mss import *
from src.request.methods import MethodName


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


def get_order_items():
    # order = Order(Direction.Ascending, Field.ValidityEnd)
    # options = Options(
    #     special_details=SpecialDetails.BasicInfo, offer_details=0, hotel_details=0
    # )  # HotelDetails.BasicInfo, OfferDetails.BasicInfo)
    # # logging = Logging(Step.Search)

    req = Request(
        Search(
            "de",
            "xxx",
            "agent",
            search_offer=SearchOffer(
                room=Room(
                    room_id=127,
                    room_type=RoomType.Room,
                    offer_id=41,
                    person=[18, 18, 5],
                )
            ),
        ),
        data=Data(
            Guest(
                firstname="Thomas",
                lastname="Alber",
                email="thomas.alber@yanovis.com",
                address=Address(),
            ),
            Company("Easymailer", "00123456", "123", Address()),
            Payment(PaymentMethod.AccommodationPayment, 0),
            "",
            Details([ExtraPrice(64, 1)]),
            Form(
                "http://demo.easymailer.it/success.htm",
                "http://demo.easymailer.it/failure.htm",
            ),
            Tracking(),
        ),
        # Options(room_details=1),
    )

    return req


def test1():
    # test getHotelList
    return Request(
        Search(
            "de",
            SearchOffer(
                "b",
                "c",
                Board.HalfBoard,
                [
                    Room(1, [18, 18], room_type=RoomType.All),
                    Room(2, [1], room_type=RoomType.All),
                    Room(3, [1], room_type=RoomType.All),
                ],
                typ=10,
            ),
        ),
        Options(picture_date="2000-01-01"),
    )


def test2(result_id):
    # test prepare booking
    search = Search(
        "de",  # on prepareBooking language apparently language isn't required?
        result_id=result_id,
        agent="someAgent",
        search_offer=SearchOffer(
            room=Room(room_id="roomid", offer_id="offerid", person=[18, 18])
        ),
    )

    data = Data(
        Guest("Rubin", "Canaj", "rcasfaf@asf.com"),
        form=Form(
            "http://easychannel.it/mss/docs/pay_view.php?VERSION=2.0",
            "http://easychannel.it/mss/docs/pay_view.php?VERSION=2.0",
        ),
    )

    return Request(search, data=data)


def test3():
    search = Search(
        "de",
        id=[9000],
        search_availability=SearchAvailability("2024-07-29", "2024-08-05"),
    )

    options = Options(
        get_availability=1,
        get_restrictions="v2",
        get_roomdetails=1,
        get_masterpackages=1,
    )

    return Request(search, options)


if __name__ == "__main__":
    # TODO function to add children to xml in client
    # Does order matter when sending XML? Reordering children gives different result ID.
    # what values must offer_id and room_id in prepareBooking have??

    credentials = Credentials(
        getenv("MSS_SERVICE_USERNAME"),
        getenv("MSS_SERVICE_PASSWORD"),
        getenv("MSS_SERVICE_SOURCE"),
    )
    lang = "de"
    client = Client(credentials, lang)

    # req = test2(
    #     "da4aaa48b52ce349f2e117b3137f985e"
    # )  # result id must have search.hotel defined, and the corresponding hotel must be bookable (hotel.bookable=1)

    req = test3()

    resp = client.request(
        getenv("MSS_SERVICE_URL"),
        MethodName.GetRoomAvailability,
        req,
        _print=True,  # , order_items, True
    )
