import sys

# # Add the parent directory to the Python path
sys.path.append("../../src/")

from client import Client
from request.types_mss import *
from request.methods import MethodName


if __name__ == "__main__":
    credentials = Credentials(
        "MSS_SERVICE_USERNAME",
        "MSS_SERVICE_PASSWORD",
        "MSS_SERVICE_SOURCE",
    )
    lang = "de"
    client = Client(credentials, lang)

    req = Request(
        Search("de", id=["YOUR_HOTEL_ID_1", "YOUR_HOTEL_ID_2", "YOUR_HOTEL_ID_3"]),
        Options(HotelDetails.BasicInfo | HotelDetails.Coordinates),
    )

    try:

        resp = client.request(
            "MSS_SERVICE_URL",
            MethodName.GetHotelList,
            req,
        )

        hotel = resp["result"]["hotel"][0]

        print(type(hotel["name"]), hotel["name"])
        print(type(hotel["stars"]), hotel["stars"])

        print(type(hotel["geolocation"]["latitude"]), hotel["geolocation"]["latitude"])

    except Exception as e:
        print(e)
