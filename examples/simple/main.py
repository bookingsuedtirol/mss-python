from src.mss_python.client import Client
from src.mss_python.request.types_mss import (
    Credentials,
    Request,
    Search,
    Options,
    HotelDetails,
)
from src.mss_python.request.methods import MethodName


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
