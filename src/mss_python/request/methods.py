from __future__ import annotations
import xml.etree.ElementTree as ET
from request.types_mss import *  # might need change


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
    GetInquiry = "getInquiry"
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


class Method:
    def __init__(self, name: MethodName):
        self.name = name

    def get_base_xml(self, cred: Credentials, lang: Search) -> Root:
        """
        Returns an XML (ElementTree) with the mandatory elements needed for the request.

        cred: XML Credentials Element (username, password, source)

        lang: XML Search Element with the language element defined
        """

        header = Header(cred, self.name)
        req = Request(lang)
        root = Root(header, req)
        return root
