from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum
from typing import Literal
import xml.etree.ElementTree as ET

# from methods import Method


@dataclass()
class Root:
    header: Header
    request: Request
    version: str = "2.0"

    def to_xml(self):
        root = ET.Element("root")
        # ET.SubElement(root,"") #version??
        root.append(self.header.to_xml())
        root.append(self.request.to_xml())

        return root


@dataclass()
class Header:
    credentials: Credentials
    method: str = Literal[
        "getHotelList",
        "getSpecialList",
        "getRoomList",
        "getPriceList",
        "getRoomAvailability",
        "getHotelPictures",
        "getHotelPictureGroups",
        "prepareBooking",
        "getBooking",
        "createInquiry",
        "getUserSources",
    ]
    # method: str
    paging: Paging | None = field(default=None)

    def to_xml(self) -> ET.Element:
        root = ET.Element("header")
        root.append(self.credentials.to_xml())
        ET.SubElement(root, "method").text = self.method

        return root


@dataclass()
class Credentials:
    user: str
    password: str
    source: str

    def to_xml(self) -> ET.Element:
        root = ET.Element("credentials")
        ET.SubElement(root, "user").text = self.user
        ET.SubElement(root, "password").text = self.password
        ET.SubElement(root, "source").text = self.source

        return root


@dataclass()
class Paging:
    start: int
    limit: int


@dataclass
class Request:
    search: Search
    options: Options | None = field(default=None)

    order: Order | None = field(default=None)

    data: Data | None = field(default=None)

    logging: Logging | None = field(default=None)

    def to_xml(self) -> ET.Element:
        root = ET.Element("request")
        # root.append(self.search.to_xml())

        for field, value in vars(self).items():
            if value != None:
                if type(value) == int or type(value) == str:
                    ET.SubElement(root, field).text = value
                else:
                    root.append(value.to_xml())

        return root


@dataclass
class Search:
    lang: str = Literal["de", "it", "en", "es", "fr", "ru", "da"]
    result_id: str | None = field(default=None)

    agent: str | None = field(default=None)

    id: list | None = field(default=None)  # number[]

    search_hotel: SearchHotel | None = field(default=None)

    search_location: SearchLocation | None = field(default=None)

    search_distance: SearchDistance | None = field(default=None)

    search_offer: SearchOffer | None = field(default=None)

    search_lts: SearchLts | None = field(default=None)

    search_special: SearchSpecial | None = field(default=None)

    search_availability: SearchAvailability | None = field(default=None)

    search_pricelist: SearchPriceList | None = field(default=None)

    in_: int | None = field(default=None)  # number[]

    id_ofchannel: str | None = field(default=None)

    transaction_id: str | None = field(default=None)

    booking_id: str | None = field(default=None)

    guest_email: str | None = field(default=None)

    pic_group_id: int | None = field(default=None)

    def to_xml(self) -> ET.Element:
        root = ET.Element("search")
        # ET.SubElement(root, "lang").text = self.lang

        for field, value in vars(self).items():
            if value != None:
                if type(value) == int or type(value) == str:
                    ET.SubElement(root, field).text = value
                else:
                    root.append(value.to_xml())

        return root


@dataclass
class Options:
    hotel_details: HotelDetails | None = field(default=None)
    offer_details: OfferDetails | None = field(default=None)
    room_details: RoomDetails | None = field(default=None)
    special_details: SpecialDetails | None = field(default=None)
    pricelist_details: PriceListDetails | None = field(default=None)
    picture_date: str | None = field(default=None)
    lts_bookable: int | None = field(default=None)  # number
    get_availability: Literal[0, 1] | None = field(default=None)  # 0 | 1
    get_restrictions: Literal[0, 1] | None = field(default=None)  # 0 | 1
    get_roomdetails: int | None = field(default=None)  # 0 | 1
    base_price: int | None = field(default=None)  # number


class HotelDetails(Enum):
    BasicInfo = (1,)
    Themes = (2,)
    HotelFacilities = (4,)
    ShortDescription = (8,)
    FullDescription = (16,)
    GeographicInformation = (32,)
    Coordinates = (64,)
    Address = (128,)
    Contacts = (256,)
    PaymentOptionsForOnlineBooking = (512,)
    PaymentOptionsAtHotel = (1024,)
    Logo = (2048,)
    HeaderImages = (4096,)
    Gallery = (8192,)
    HotelMatching = (16384,)
    GeographicalInformationAsText = (32768,)
    HotelNavigatorData = (65536,)
    DetailedHotelFacilities = (131072,)
    SalesPoint = (524288,)
    LtsSpecificParameters = (262144,)
    CheckInOut = (1048576,)
    SourceData = (2097152,)


class OfferDetails(Enum):
    BasicInfo = (1,)
    RoomCode = (4,)
    RoomTitle = (8,)
    PriceDetails = (16,)
    RoomImages = (32,)
    RoomFacilitiesFilter = (64,)
    RoomDescription = (256,)
    IncludedServices = (1024,)
    AdditionalServices = (2048,)
    RoomFacilitiesDetails = (4096,)
    PriceImages = (8192,)
    Themes = (16384,)
    RoomFeatures = (32768,)
    CancelPolicies = (262144,)
    PaymentTerms = (1048576,)


class PriceListDetails(Enum):
    BaseData = (1,)
    Headlines = (8,)
    Seasons = (4194304,)


class RoomDetails(Enum):
    BasicInfo = (4,)
    Title = (8,)
    RoomImages = (32,)
    RoomFacilitiesFilter = (64,)
    RoomDescription = (256,)
    RoomFacilitiesDetails = (4096,)
    RoomFeatures = (32768,)
    RoomNumbers = (65536,)


class SpecialDetails(Enum):
    BasicInfo = (1,)
    Title = (2,)
    Descriptions = (4,)
    Seasons = (8,)
    Images = (16,)
    Themes = (32,)
    IncludedServices = (64,)


@dataclass
class Order:
    dir: str | None = field(default=None)
    field: str | None = field(default=None)


@dataclass
class Data:
    guest: Guest | None = field(default=None)
    company: Company | None = field(default=None)
    payment: Payment | None = field(default=None)
    note: str | None = field(default=None)
    details: Details | None = field(default=None)
    form: Form | None = field(default=None)
    tracking: Tracking | None = field(default=None)


@dataclass
class Logging:
    step: str | None = field(default=None)


@dataclass
class SearchHotel:
    name: str | None = field(default=None)
    type: HotelType | None = field(default=None)
    stars: Stars | None = field(default=None)
    feature: HotelFeature | None = field(default=None)
    theme: HotelTheme | None = field(default=None)


class HotelType(Enum):
    Hotel = (1,)
    SkiSchool = (2,)
    Residence = (4,)
    Appartment = (16,)
    FarmVacation = (32,)
    MountainInn = (64,)
    CampingSite = (128,)
    HolidayHome = (256,)
    YouthHostel = (512,)
    Guesthouse = (1024,)
    Refuge = (2048,)
    Garni = (4096,)
    Inn = (8192,)


class HotelFeature(Enum):
    Garage = (1,)
    Elevator = (2,)
    Restaurant = (4,)
    Gym = (8,)
    Wellness = (16,)
    Spa = (32,)
    Breakfast = (64,)
    Buffet = (128,)
    OutdoorPool = (256,)
    IndoorPool = (512,)
    Bar = (1024,)
    BarrierFree = (2048,)
    Wlan = (4096,)
    ShuttleService = (8192,)
    Childcare = (16384,)
    SmallPetsAllowed = (32768,)
    BeautyFarm = (65536,)
    CentralLocation = (262144,)
    CoveredParking = (524288,)
    OpenParking = (1048576,)
    Massages = (2097152,)
    Sauna = (4194304,)
    SteamBath = (8388608,)
    PublicBar = (16777216,)
    DogsAllowed = (33554432,)


class HotelTheme(Enum):
    Family = (1,)
    Wellness = (2,)
    Hiking = (4,)
    Motorcycle = (8,)
    Bike = (16,)
    Golf = (32,)
    Riding = (64,)
    Romantic = (128,)
    Ski = (256,)
    Meeting = (512,)
    CrossCountrySkiing = (1024,)
    Culture = (2048,)
    Snowshoeing = (4096,)


@dataclass
class SearchLocation:
    location: list | None = field(default=None)  # number[]
    location_lts: list | None = field(default=None)  # string[]


@dataclass
class SearchDistance:
    latitude: int | None = field(default=None)  # number
    longitude: int | None = field(default=None)  # number
    radius: int | None = field(default=None)  # number


@dataclass
class SearchOffer:
    arrival: str | None = field(default=None)  # Date
    departure: str | None = field(default=None)  # Date
    service: Board | None = field(default=None)
    feature: RoomFeature | None = field(default=None)
    channel_id: list | None = field(default=None)  # string[]
    room: list | None = field(default=None)  # Room[]
    typ: SearchOfferType | None = field(default=None)
    rateplan: Rateplan | None = field(default=None)


class SearchOfferType(Enum):
    DefaultPricelist = (10,)
    PeopleAge = (20,)
    PeopleNumber = (21,)
    Staying = (22,)
    BookingDate = (23,)
    Weekday = (24,)
    NoReference = (25,)
    SpecialPeopleAge = (50,)
    SpecialPeopleNumber = (51,)
    SpecialStaying = (52,)
    SpecialBookingDate = (53,)
    SpecialWeekday = (54,)
    SpecialNoReference = (55,)


class Board(Enum):
    Without = (1,)
    Breakfast = (2,)
    HalfBoard = (3,)
    FullBoard = (4,)
    AllInclusive = (5,)


class RoomFeature(Enum):
    Balcony = (1,)
    Terrace = (2,)
    MiniBar = (4,)
    Safe = (8,)
    TV = (16,)
    Satellite = (32,)
    Wlan = (64,)
    Internet = (128,)
    BarrierFree = (512,)


@dataclass
class SearchLts:
    A0Ene: int | None = field(default=None)  # number
    A0MTV: int | None = field(default=None)  # number
    A0Rep: int | None = field(default=None)  # number


@dataclass
class SearchSpecial:
    offerId: list | None = field(default=None)  # number[]
    date_from: str | None = field(default=None)  # Date
    date_to: str | None = field(default=None)  # Date
    theme: SpecialTheme | None = field(default=None)
    validity: Validity | None = field(default=None)
    typ: SearchSpecialType | None = field(default=None)
    premium: SearchSpecialPremium | None = field(default=None)


class SearchSpecialType(Enum):
    PriceLists = (0,)
    Packages = (1,)
    Specials = (2,)
    ShortLongStays = (4,)


class SearchSpecialPremium(Enum):
    FamilyHotelsPremium = (2,)
    VinumHotelsPremium = (4,)
    SüdtirolBalancePremium = (8,)
    VitalpinaDurchatmen = (16,)
    VitalpinaWohlfühlen = (32,)
    VitalpinaErnährung = (64,)
    VitalpinaAktiv = (128,)
    VitalpinaPremium = (256,)
    BikehotelsMountainbike = (512,)
    BikehotelsBikeTouringEBike = (1024,)
    BikehotelsRoadbike = (2048,)
    BikehotelsPremium = (4096,)
    ArchitectureDays = (8192,)
    VinumHotels = (16384,)
    FamilyHotels = (32768,)
    FamilyHotelsNatureDetective = (65536,)
    FamilyHotelsNatureDetectiveWinter = (131072,)


class SpecialTheme(Enum):
    Hiking = (1,)
    Cycling = (2,)
    Family = (4,)
    Wellness = (8,)
    Food = (16,)
    Golf = (32,)
    Culture = (64,)
    Motorsport = (128,)
    CarFree = (256,)
    SkiSnowboard = (512,)
    SummerActivities = (1024,)
    Events = (2048,)
    ChristmasMarkets = (4096,)
    ActiveWinter = (8192,)
    Vitalpina = (16384,)
    VitalpinaBreathe = (32768,)
    BikeHotelsEBike = (65536,)
    BikeHotelsFreeride = (131072,)
    BikeHotelsMountainbike = (524288,)
    BikeHotelsBikeTours = (1048576,)
    BikeHotelsRacingBike = (2097152,)
    FamilyHotels = (4194304,)
    FamilyHotelsNatureDetective = (8388608,)
    FamilyHotel = (33554432,)
    FamilyHotelsNatureDetectiveSummer = (67108864,)
    FamilyHotelsNatureDetectiveWinter = (134217728,)


@dataclass
class SearchAvailability:
    date_from: str | None = field(default=None)  # Date
    date_to: str | None = field(default=None)  # Date
    offer_id: list | None = field(default=None)  # number[]
    room_id: list | None = field(default=None)  # number[]


@dataclass
class SearchPriceList:
    date_from: str | None = field(default=None)  # Date
    date_to: str | None = field(default=None)  # Date
    service: Board | None = field(default=None)
    room_id: list | None = field(default=None)  # number[]
    typ: SearchSpecialType | None = field(default=None)


@dataclass
class Guest:
    gender: str | None = field(default=None)
    prefix: str | None = field(default=None)
    firstname: str | None = field(default=None)
    lastname: str | None = field(default=None)
    email: str | None = field(default=None)
    phone: str | None = field(default=None)
    address: Address | None = field(default=None)
    newsletter: Literal[0, 1] | None = field(default=None)  # 0 | 1


@dataclass
class Company:
    name: str | None = field(default=None)
    taxnumber: str | None = field(default=None)
    recipient_code: str | None = field(default=None)
    address: Address | None = field(default=None)


@dataclass
class Payment:
    method: PaymentMethod | None = field(default=None)
    invoice: Literal[0, 1] | None = field(default=None)  # 0 | 1


class PaymentMethod(Enum):
    CreditCardDeposit = (1,)
    CreditCardAsSecurity = (2,)
    CreditCardPayment = (8,)
    BankTransferDeposit = (4,)
    BankTransferPayment = (16,)
    AccommodationPayment = (32,)


@dataclass
class Details:
    extr_price: list | None = field(default=None)  # ExtraPrice[]


@dataclass
class ExtraPrice:
    price_id: int | None = field(default=None)  # number
    price_amount: int | None = field(default=None)  # number


@dataclass
class Form:
    url_success: str | None = field(default=None)
    url_failure: str | None = field(default=None)


@dataclass
class Tracking:
    partner: str | None = field(default=None)
    media: str | None = field(default=None)
    campaign: str | None = field(default=None)
    companyinfo: str | None = field(default=None)


@dataclass
class Stars:
    min: int | None = field(default=None)  # number
    max: int | None = field(default=None)  # number


@dataclass
class Address:
    street: str | None = field(default=None)
    zipcode: str | None = field(default=None)
    city: str | None = field(default=None)
    country: str | None = field(default=None)


@dataclass
class Room:
    offer_id: int | None = field(default=None)  # number
    room_id: int | None = field(default=None)  # number
    service: Board | None = field(default=None)
    room_type: RoomType | None = field(default=None)
    room_seq: int | None = field(default=None)  # number
    person: list | None = field(default=None)  # number[]


class RoomType(Enum):
    All = (0,)
    Room = (1,)
    Apartment = (2,)


@dataclass
class Rateplan:
    code: str | None = field(default=None)
    source: str | None = field(default=None)


@dataclass
class Validity:
    valid: Literal[0, 1] | None = field(default=None)  # 0 | 1
    offers: Literal[0, 1] | None = field(default=None)  # 0 | 1
    arrival: str | None = field(default=None)  # Date
    departure: str | None = field(default=None)  # Date
    service: Board | None = field(default=None)
    room: list | None = field(default=None)  # Room[]


def getHotelList_base_xml(root: Root, header: Header):
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml += root.version
    xml += header.credentials
    return xml
