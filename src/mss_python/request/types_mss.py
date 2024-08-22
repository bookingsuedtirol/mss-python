from __future__ import annotations
from dataclasses import dataclass, field
from enum import Enum, IntFlag
from typing import Literal
import xml.etree.ElementTree as ET
from abc import ABC

from .method_names import MethodName


def get_child_xml(value, field, root):
    field = field.replace("___", "-")
    match value:
        case None:
            return
        case int() | float():
            ET.SubElement(root, field).text = str(value)
        case str():
            if field == "tag":
                return
            ET.SubElement(root, field).text = value
        case list():
            for x in value:
                get_child_xml(x, field, root)
        case Enum():
            ET.SubElement(root, field).text = str(value.value)
        case _:
            root.append(value.to_xml())


class BaseType(ABC):
    def __init__(self, tag):
        self.tag = tag

    def to_xml(self) -> ET.Element:
        root = ET.Element(self.tag)
        # root.append(self.search.to_xml())

        for field_, value in vars(self).items():
            get_child_xml(value, field_, root)

        return root


@dataclass()
class Root(BaseType):
    header: Header
    request: Request
    version: str = "2.0"

    def __post_init__(self):
        super().__init__("root")


@dataclass()
class Header(BaseType):
    credentials: Credentials
    method: MethodName
    # method: str
    paging: Paging | None = field(default=None)

    def __post_init__(self):
        super().__init__("header")


@dataclass()
class Credentials(BaseType):
    user: str
    password: str
    source: str

    def __post_init__(self):
        super().__init__("credentials")


@dataclass()
class Paging:
    start: int
    limit: int


@dataclass
class Request(BaseType):
    search: Search
    options: Options | None = field(default=None)

    order: Order | None = field(default=None)

    data: Data | None = field(default=None)

    logging: Logging | None = field(default=None)

    def __post_init__(self):
        super().__init__("request")


@dataclass
class Search(BaseType):
    lang: list  # Literal["de", "it", "en", "es", "fr", "ru", "da"]
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

    id_ofchannel: Literal["hgv", "lts", "esy"] | None = field(default=None)

    transaction_id: str | None = field(default=None)

    booking_id: str | None = field(default=None)

    guest_email: str | None = field(default=None)

    pic_group_id: int | None = field(default=None)

    id_apt: int | None = field(default=None)

    root_id: list | None = field(default=None)  # list of ints

    pic_type: PictureType | None = field(default=None)

    select___avail: HotelFilters | None = field(default=None)
    select___rooms: HotelFilters | None = field(default=None)
    select___price: HotelFilters | None = field(default=None)
    avail_alert: Literal[0, 1] | None = field(default=None)
    rooms_alert: Literal[0, 1] | None = field(default=None)
    price_alert: Literal[0, 1] | None = field(default=None)

    coupon_code: str | None = field(default=None)
    total_price: int | None = field(default=None)
    arrival: str | None = field(default=None)
    departure: str | None = field(default=None)
    coupon_type: Literal["promotion", "voucher"] | None = field(default=None)

    def __post_init__(self):
        super().__init__("search")


class HotelFilters(Enum):
    OTA = "ota"
    EASI_CHANNEL = "easiChannel"
    ROTER_HAHN = "10ec953a9d700b9598580a52d3dcef6c"
    HOTEL_PARTNER = "2d9038f6a34c23280669f73ff531683c"
    FIVE_STELLE = "30fb54af1d0d231b01b778647cfd967c"
    ASA_LIGHT = "51c761e7b7b87dbeafe25a9b"
    ASA_HOTEL = "51c761e7b7b87dc3afe15afa"
    ROOM_CLOUD = "65ee9db4c37baedc1032cbd72c8caaaf"
    GS_DATAPROVIDER = "66461e9d7c481e44e632051c3d040a2b"
    HGV_TEST_CLIENT = "95f6a058-45ca-49df-874f-86f41e0bb29f"
    HGV_CLIENT_FOR_TRENTINO = "a47a9dd543e55f8b3ee7ce4cc88b6d57"
    HOTEL_NET_SOLUTIONS = "a57f0615b226609ae409c421ff118a8a"
    BEDDY = "a8513684c7683fd457f82818f5f15bbf"
    PCS_PHOENIX_XENUS = "AE1D2D8776B3FC1C;XENUS"
    AIDA = "AIbD6vqHlYHA17DA"
    AE_SMO = "ba098f2c86b942e58b6e7a89448f4063"
    MTS_ONLINE = "bdcec66dfe4e8ef9f5c7e71e4835204c"
    LTS_BOZEN = "be6bc64c94bbc062bcebfb40b4f93304"
    BOOKING_EXPERT = "BookingE47acfb09170e8"
    CASABLANCA = "CasaifeDZQQDaqvlblanca"
    APARTMENT4HOLIDAY = "ceaeed03a0711eec46582b689d16dc0b"
    CIAOBNB = "CiaoK2VAvAkFlCTcbnb"
    EASI_SUITE = "Easy68e9nMxChannel"
    EASI_SUITE_2 = "Easy68e9nMxChannel2"
    SCIDOO = "f0bdfb926c2a8d066a9d2ea3e632471c"
    ERICSOFT = "fcfb97bb1a8e608e5971928ac2032a68"
    HOTEL_SPIDER = "HoteltihPrvo8kMpbSpider"
    IPER_BOOKING = "iperbooking"
    KROSS_BOOKING = "Kross2XklTsfhbBooking"
    MM_ONE = "MMwRNWBeSQiABuONE"
    PASSEPARTOUT = "passPGkPyHnw3IbApartout"
    SEEKDA = "SEEK8XLyALKEzmpyp2DA"
    SIMPLE_BOOKING = "Simple89sKiOdS9PUcbooking"
    ANEXIS = "SiPaCbW2I921EpMedia"
    SMART_PRICING = "SmartqpukLfH5Kl1price"
    TEST_YANOVIS = "travelsuite"
    VERTICAL_BOOKING = "VertiexDH0x8XV7Booking"
    ALPINE_BITS_CERTIFICATION = "VwnIjABCertification78czDK6"
    WUBOOK = "Wub0Na0CxWovxdVook"


class PictureType(Enum):
    Hotel = "hotel"
    Gallery = "gallery"
    Profile = "profile"
    Roomgroup = "roomgroup"
    Pricelist = "pricelist"
    Special = "special"


@dataclass
class Options(BaseType):
    hotel_details: HotelDetails | None = field(default=None)
    offer_details: OfferDetails | None = field(default=None)

    picture_date: str | None = field(default=None)  # Date
    lts_bookable: Literal[0, 1, 2] | None = field(default=None)  # number, 0|1|2

    base_price: int | None = field(default=None)  # number, 0|1

    # field is in easychannel but not in nodejs
    only_available: Literal[0, 1] | None = field(default=None)  # 0 | 1

    # below fields are in nodejs but not in easychannel.it?
    room_details: RoomDetails | None = field(default=None)
    special_details: SpecialDetails | None = field(default=None)
    # pricelist_details: PriceListDetails | None = field(default=None)

    get_availability: Literal[0, 1] | None = field(default=None)  # 0 | 1
    get_restrictions: Literal[0, 1] | None = field(default=None)  # 0 | 1
    get_roomdetails: int | None = field(default=None)  # 0 | 1
    get_masterpackages: Literal[0, 1] | None = field(default=None)

    location_details: Literal[0, 1] | None = field(default=None)
    theme_details: Literal[0, 1] | None = field(default=None)

    service_details: ServiceDetails | None = field(default=None)

    def __post_init__(self):
        super().__init__("options")


class ServiceDetails(IntFlag):
    Headlines = 8
    Pictures = 32
    Descriptions = 256


class HotelDetails(IntFlag):
    BasicInfo = 1
    Themes = 2
    HotelFacilities = 4
    ShortDescription = 8
    FullDescription = 16
    GeographicInformation = 32
    Coordinates = 64
    Address = 128
    Contacts = 256
    PaymentOptionsForOnlineBooking = 512
    PaymentOptionsAtHotel = 1024  #
    Logo = 2048
    HeaderImages = 4096
    Gallery = 8192
    HotelMatching = 16384
    GeographicalInformationAsText = 32768
    HotelReviews = 65536  # different name in GO
    DetailedHotelFacilities = 131072
    SalesPoint = 524288
    LtsSpecificParameters = 262144
    CouponServiceData = 16777216
    CheckInOut = 1048576
    SourceData = 2097152
    AccountData = 67108864
    RoomTypes = 134217728
    # Payment provider missing?


class OfferDetails(IntFlag):
    BasicInfo = 1
    RoomCode = 4
    RoomTitle = 8
    PriceDetails = 16
    RoomImages = 32
    RoomFacilitiesFilter = 64
    RoomDescription = 256
    IncludedServices = 1024
    AdditionalServices = 2048
    RoomFacilitiesDetails = 4096
    PriceImages = 8192
    Themes = 16384
    RoomFeatures = 32768
    CancelPolicies = 262144
    PaymentTerms = 1048576


class RoomDetails(IntFlag):
    BasicInfo = 4
    Title = 8
    RoomImages = 32
    RoomFacilitiesFilter = 64
    RoomDescription = 256
    RoomFacilitiesDetails = 4096
    RoomFeatures = 32768
    RoomNumbers = 65536


class SpecialDetails(IntFlag):
    BasicInfo = 1
    Title = 2
    Descriptions = 4
    Seasons = 8
    Images = 16
    Themes = 32
    IncludedServices = 64


@dataclass
class Order(BaseType):
    dir: Direction | None = field(default=None)
    field: Field | None = field(default=None)

    def __post_init__(self):
        super().__init__("order")


class Field(Enum):
    ValidityStart = "valid_start"
    ValidityEnd = "valid_end"
    Random = "rand"
    Stars = "stars"
    Name = "name"


class Direction(Enum):
    Ascending = "asc"
    Descending = "desc"


@dataclass
class Data(BaseType):
    guest: Guest | None = field(default=None)
    company: Company | None = field(default=None)
    payment: Payment | None = field(default=None)
    note: str | None = field(default=None)
    details: Details | None = field(default=None)
    form: Form | None = field(default=None)
    tracking: Tracking | None = field(default=None)
    # insurance: Ins
    storno_reason: StornoReason | None = field(default=None)
    storno_reason_text: str | None = field(default=None)

    special: list | None = field(default=None)  # list of specials

    def __post_init__(self):
        super().__init__("data")


@dataclass
class Special(BaseType):
    offer_id: int
    action: Literal["update", "delete"]
    time_modified: str  # ISO 8601 Date
    reset_participants: Literal[0, 1] | None = field(default=None)

    def __post_init__(self):
        super().__init__("special")


class StornoReason(Enum):
    Unknown = 0
    GuestNotAvailable = 1
    AccomodationRequestedToCancel = 2
    GuestAnotherDestination = 3
    GuestAnotherAccomodation = 4
    Other = 99


@dataclass
class Logging(BaseType):
    step: str | None = field(default=None)

    def __post_init__(self):
        super().__init__("logging")


class Step(Enum):
    Search = "search"
    SearchOffer = "search_offer"
    SearchDetails = "search_details"
    View = "view"
    ViewOffer = "view_offer"
    Step1 = "step_1"
    Step2 = "step_2"
    Step3 = "step_3"
    Step4 = "step_4"


@dataclass
class SearchHotel(BaseType):
    name: str | None = field(default=None)
    type: HotelType | None = field(default=None)
    stars: Stars | None = field(default=None)
    feature: HotelFeature | None = field(default=None)
    theme: HotelTheme | None = field(default=None)

    def __post_init__(self):
        super().__init__("search_hotel")


class HotelType(Enum):
    Hotel = "1"
    SkiSchool = "2"
    Residence = "4"
    Appartment = "16"
    FarmVacation = "32"
    MountainInn = "64"
    CampingSite = "128"
    HolidayHome = "256"
    YouthHostel = "512"
    Guesthouse = "1024"
    Refuge = "2048"
    Garni = "4096"
    Inn = "8192"


class HotelFeature(Enum):
    Garage = "1"
    Elevator = "2"
    Restaurant = "4"
    Gym = "8"
    Wellness = "16"
    Spa = "32"
    Breakfast = "64"
    Buffet = "128"
    OutdoorPool = "256"
    IndoorPool = "512"
    Bar = "1024"
    BarrierFree = "2048"
    Wlan = "4096"
    ShuttleService = "8192"
    Childcare = "16384"
    SmallPetsAllowed = "32768"
    BeautyFarm = "65536"
    CentralLocation = "262144"
    CoveredParking = "524288"
    OpenParking = "1048576"
    Massages = "2097152"
    Sauna = "4194304"
    SteamBath = "8388608"
    PublicBar = "16777216"
    DogsAllowed = "33554432"


class HotelTheme(Enum):
    Family = "1"
    Wellness = "2"
    Hiking = "4"
    Motorcycle = "8"
    Bike = "16"
    Golf = "32"
    Riding = "64"
    Romantic = "128"
    Ski = "256"
    Meeting = "512"
    CrossCountrySkiing = "1024"
    Culture = "2048"
    Snowshoeing = "4096"


@dataclass
class SearchLocation(BaseType):
    location: list | None = field(default=None)  # number[], Location ID
    location_lts: list | None = field(default=None)  # string[], LTS Location RID

    def __post_init__(self):
        super().__init__("search_location")


@dataclass
class SearchDistance:
    latitude: float  # number
    longitude: float  # number
    radius: int  # number


@dataclass
class SearchOffer(BaseType):
    arrival: str | None = field(default=None)  # Date YYYY-MM-DD
    departure: str | None = field(default=None)  # Date YYYY-MM-DD
    service: Board | None = field(default=None)
    room: list | None = field(default=None)  # Room[]
    feature: RoomFeature | None = field(default=None)
    channel_id: list | None = field(default=None)  # string[]
    typ: SearchOfferType | None = field(default=None)
    rateplan: Rateplan | None = field(default=None)

    # features from easychange missing?

    def __post_init__(self):
        super().__init__("search_offer")


class SearchOfferType(Enum):
    DefaultPricelist = "10"
    PeopleAge = "20"
    PeopleNumber = "21"
    Staying = "22"
    BookingDate = "23"
    Weekday = "24"
    NoReference = "25"
    SpecialPeopleAge = "50"
    SpecialPeopleNumber = "51"
    SpecialStaying = "52"
    SpecialBookingDate = "53"
    SpecialWeekday = "54"
    SpecialNoReference = "55"


class Board(Enum):
    Without = 1
    Breakfast = 2
    HalfBoard = 3
    FullBoard = 4
    AllInclusive = 5


class RoomFeature(IntFlag):
    Balcony = 1
    Terrace = 2
    MiniBar = 4
    Safe = 8
    TV = 16
    Satellite = 32
    Wlan = 64
    Internet = 128
    BarrierFree = 512


@dataclass
class SearchLts(BaseType):
    A0Ene: int | None = field(default=None)  # number
    A0MTV: int | None = field(default=None)  # number
    A0Rep: int | None = field(default=None)  # number

    def __post_init__(self):
        super().__init__("search_lts")


@dataclass
class SearchSpecial(BaseType):
    offer_id: list | None = field(default=None)  # number[]
    date_from: str | None = field(default=None)  # Date YYYY-MM-DD
    date_to: str | None = field(default=None)  # Date YYYY-MM-DD
    theme: list | None = field(default=None)  # array of SpecialTheme
    validity: Validity | None = field(default=None)
    typ: SearchSpecialType | None = field(default=None)
    premium: SearchSpecialPremium | None = field(default=None)

    poi_id: list | None = field(default=None)
    poi_cat: list | None = field(default=None)
    status: Literal[0, 1] | None = field(default=None)

    def __post_init__(self):
        super().__init__("search_special")


class SearchSpecialType(Enum):
    PriceLists = 0
    Packages = 1
    Specials = 2
    ShortLongStays = 4


class SearchSpecialPremium(IntFlag):
    FamilyHotelsPremium = 2
    VinumHotelsPremium = 4
    SüdtirolBalancePremium = 8
    VitalpinaDurchatmen = 16
    VitalpinaWohlfühlen = 32
    VitalpinaErnährung = 64
    VitalpinaAktiv = 128
    VitalpinaPremium = 256
    BikehotelsMountainbike = 512
    BikehotelsBikeTouringEBike = 1024
    BikehotelsRoadbike = 2048
    BikehotelsPremium = 4096
    ArchitectureDays = 8192
    VinumHotels = 16384
    FamilyHotels = 32768
    FamilyHotelsNatureDetective = 65536
    FamilyHotelsNatureDetectiveWinter = 131072


class SpecialTheme(Enum):
    ThemeIDHiking = 1
    ThemeIDCyclingMountainbike = 2
    ThemeIDFamily = 3
    ThemeIDWellnessHealth = 4
    ThemeIDFoodAndDrink = 5
    ThemeIDGolf = 6
    ThemeIDCulture = 7
    ThemeIDMotorsport = 8
    ThemeIDCarFreeHolidays = 9
    ThemeIDSkiSnowboard = 10
    ThemeIDSummerActivities = 11
    ThemeIDEvents = 12
    ThemeIDChristmasMarkets = 13
    ThemeIDActiveWinter = 14
    ThemeIDVitalpina = 15
    ThemeIDVitalpinaBreathe = 16
    ThemeIDBikeHotelsEBike = 17
    ThemeIDBikeHotelsFreeride = 18
    ThemeIDBikeHotelsMountainbike = 20
    ThemeIDBikeHotelsBikeTours = 21
    ThemeIDBikeHotelsRacingBike = 22
    ThemeIDFamilyHotels = 23
    ThemeIDFamilyHotelsNatureDetective = 24
    ThemeIDFamilyHotel = 26
    ThemeIDNatureDetectivSummer = 27
    ThemeIDNatureDetectivWinter = 28
    ThemeIDEcologicHoliday = 79
    ThemeIDHorseBackRiding = 80
    ThemeIDLuxuryHoliday = 81
    ThemeIDPetsFriendlyHoliday = 82
    ThemeIDRoadBike = 83
    ThemeIDRomanticHoliday = 84
    ThemeIDWine = 85
    ThemeIDBicycleTouring = 86
    ThemeIDEBike = 87

    ## These values were theme_bit
    # Hiking = 1
    # Cycling = 2
    # Family = 4
    # Wellness = 8
    # Food = 16
    # Golf = 32
    # Culture = 64
    # Motorsport = 128
    # CarFree = 256
    # SkiSnowboard = 512
    # SummerActivities = 1024
    # Events = 2048
    # ChristmasMarkets = 4096
    # ActiveWinter = 8192
    # Vitalpina = 16384
    # VitalpinaBreathe = 32768
    # BikeHotelsEBike = 65536
    # BikeHotelsFreeride = 131072
    # BikeHotelsMountainbike = 524288
    # BikeHotelsBikeTours = 1048576
    # BikeHotelsRacingBike = 2097152
    # FamilyHotels = 4194304
    # FamilyHotelsNatureDetective = 8388608
    # FamilyHotel = 33554432
    # FamilyHotelsNatureDetectiveSummer = 67108864
    # FamilyHotelsNatureDetectiveWinter = 134217728


@dataclass
class SearchAvailability(BaseType):
    date_from: str  # Date YYYY-MM-DD
    date_to: str  # Date YYYY-MM-DD
    offer_id: list | None = field(default=None)  # number[]
    room_id: list | None = field(default=None)  # number[]
    duration: int | None = field(default=None)
    room: Room | None = field(default=None)

    def __post_init__(self):
        super().__init__("search_availability")


@dataclass
class SearchPriceList(BaseType):
    date_from: str | None = field(default=None)  # Date YYYY-MM-DD
    date_to: str | None = field(default=None)  # Date YYYY-MM-DD
    service: Board | None = field(default=None)
    room_id: list | None = field(default=None)  # number[]
    typ: SearchSpecialType | None = field(default=None)

    def __post_init__(self):
        super().__init__("search_pricelist")


@dataclass
class Guest(BaseType):
    firstname: str
    lastname: str
    email: str
    gender: str | None = field(default=None)
    prefix: str | None = field(default=None)
    phone: str | None = field(default=None)
    address: Address | None = field(default=None)
    newsletter: Literal[0, 1] | None = field(default=None)  # 0 | 1

    def __post_init__(self):
        super().__init__("guest")


@dataclass
class Company(BaseType):
    name: str | None = field(default=None)
    taxnumber: str | None = field(default=None)
    recipient_code: str | None = field(default=None)
    address: Address | None = field(default=None)

    def __post_init__(self):
        super().__init__("company")


@dataclass
class Payment(BaseType):
    method: PaymentMethod | None = field(default=None)
    invoice: Literal[0, 1] | None = field(default=None)  # 0 | 1

    def __post_init__(self):
        super().__init__("payment")


class PaymentMethod(IntFlag):
    CreditCardDeposit = 1
    CreditCardAsSecurity = 2
    CreditCardPayment = 8
    BankTransferDeposit = 4
    BankTransferPayment = 16
    AccommodationPayment = 32


@dataclass
class Details(BaseType):
    extr_price: list | None = field(default=None)  # ExtraPrice[]

    def __post_init__(self):
        super().__init__("Details")


@dataclass
class ExtraPrice(BaseType):
    price_id: int | None = field(default=None)  # number
    price_amount: int | None = field(default=None)  # number

    def __post_init__(self):
        super().__init__("extra_price")


@dataclass
class Form(BaseType):
    url_success: str | None = field(default=None)
    url_failure: str | None = field(default=None)

    def __post_init__(self):
        super().__init__("form")


@dataclass
class Tracking(BaseType):
    partner: str | None = field(default=None)
    media: str | None = field(default=None)
    campaign: str | None = field(default=None)
    companyinfo: str | None = field(default=None)

    def __post_init__(self):
        super().__init__("tracking")


@dataclass
class Stars(BaseType):
    min: Literal[1, 2, 3, 3.5, 4, 4.5, 5] | None = field(
        default=None
    )  # number, min can be 1, values are 1, 2, 3, 3.5, 4, 4.5, 5
    max: Literal[1, 2, 3, 3.5, 4, 4.5, 5] | None = field(
        default=None
    )  # number, max can be 5

    def __post_init__(self):
        super().__init__("stars")


@dataclass
class Address(BaseType):
    street: str | None = field(default=None)
    zipcode: str | None = field(default=None)
    city: str | None = field(default=None)
    country: str | None = field(default=None)

    def __post_init__(self):
        super().__init__("address")


@dataclass
class Room(BaseType):
    room_seq: int | None = field(default=None)  # number
    person: list | None = field(
        default=None
    )  # number[], 1..n Persons and their age (store only age inside tags)
    offer_id: int | None = field(default=None)  # number
    room_id: int | None = field(default=None)  # number
    service: Board | None = field(default=None)
    room_type: RoomType | None = field(default=None)

    def __post_init__(self):
        super().__init__("room")


class RoomType(Enum):
    All = 0
    Room = 1
    Apartment = 2
    Campsite = 4


@dataclass
class Rateplan(BaseType):
    code: str  # | None = field(default=None)
    source: str  # | None = field(default=None)

    def __post_init__(self):
        super().__init__("rateplan")


@dataclass
class Validity(BaseType):
    valid: Literal[0, 1]  # 0 | 1
    offers: Literal[0, 1] | None = field(default=None)  # 0 | 1
    arrival: str | None = field(default=None)  # Date YYYY-MM-DD
    departure: str | None = field(default=None)  # Date YYYY-MM-DD
    service: Board | None = field(default=None)
    room: list | None = field(default=None)  # Room[]

    def __post_init__(self):
        super().__init__("validity")


def getHotelList_base_xml(root: Root, header: Header):
    xml = '<?xml version="1.0" encoding="utf-8"?>'
    xml += root.version
    xml += header.credentials
    return xml
