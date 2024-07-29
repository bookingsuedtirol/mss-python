from __future__ import annotations

# from abc import ABC, abstractmethod

# from os import getenv
import xml.etree.ElementTree as ET
from src.request.types_mss import *  # might need change


class MethodName(Enum):
    GetHotelList = "getHotelList"
    GetHotelListByFilter = "getHotelListByFilter"
    GetSpecialList = "getSpecialList"
    GetRoomList = "getRoomList"
    GetWidgetConfig = "getWidgetConfig"
    GetPriceList = "getPriceList"
    GetAvailability = "getAvailability"
    GetRoomAvailability = "getRoomAvailability"
    GetDayAvailability = "getDayAvailability"
    PrepareBooking = "prepareBooking"
    GetBooking = "getBooking"
    CancelBooking = "cancelBooking"
    CreateInquiry = "createInquiry"
    GetUserSources = "getUserSources"
    GetLocationList = "getLocationList"
    GetMasterpackagesList = "getMasterpackagesList"
    NotifyMasterpackages = "notifyMasterpackages"
    GetThemeList = "getThemeList"
    GetLastminuteQuotations = "getLastminuteQuotations"
    GetHotelPictures = "getHotelPictures"
    GetHotelPictureGroups = "getHotelPictureGroups"
    GetOptionalServices = "getOptionalServices"
    ValidateCoupon = "validateCoupon"


class Method:  # (ABC):
    def __init__(self, name: MethodName):
        self.name = name

    def get_base_xml(self, cred: Credentials, lang: Search) -> ET.Element:
        """
        Returns an XML (ElementTree) with the mandatory elements needed for the request.

        cred: XML Credentials Element (username, password, source)

        lang: XML Search Element with the language element defined
        """

        header = Header(cred, self.name)
        req = Request(lang)
        root = Root(header, req)
        return root  # .to_xml()

    # @abstractmethod
    # def get_base_xml(self, cred: Credentials, lang: Search):
    #     pass

    # def get_method(name: str) -> Method:
    #     match name:
    #         case "getHotelList":
    #             return GetHotelList()
    #         case "getHotelListByFilter":
    #             return GetHotelListByFilter()
    #         case _:
    #             raise TypeError(f"{name} is not a valid method name")


# class GetHotelList(Method):
#     def __init__(self) -> None:
#         super().__init__("getHotelList", self)

#     def get_base_xml(self, cred: Credentials, lang: Search) -> ET.Element:
#         """
#         Returns an XML (ElementTree) with the mandatory elements needed for the request.

#         cred: XML Credentials Element (username, password, source)

#         lang: XML Search Element with the language element defined
#         """

#         header = Header(cred, self.name)
#         req = Request(lang)
#         root = Root(header, req)
#         return root  # .to_xml()


# class GetHotelListByFilter(Method):
#     def __init__(self) -> None:
#         super().__init__("getHotelListByFilter", self)

#     def get_base_xml(self, cred: Credentials, lang: Search) -> ET.Element:
#         """
#         Returns an XML (ElementTree) with the mandatory elements needed for the request.

#         cred: XML Credentials Element (username, password, source)

#         lang: XML Search Element with the language element defined
#         """

#         header = Header(cred, self.name)
#         req = Request(lang)
#         root = Root(header, req)
#         return root  # .to_xml()
