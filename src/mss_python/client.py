import requests
import xmltodict
import xml.etree.ElementTree as ET

from .request.methods import Method
from .request.types_mss import Root, BaseType, Credentials, Search, MethodName, Literal


# maybe recursion should be used instead of doing if checks?
def change_structure(root: Root, child: BaseType):
    if child.tag == "root":
        return child

    if child.tag == "request":
        root.request = child

    elif child.tag == "search":
        root.request.search = child

    elif child.tag == "order":
        root.request.order = child

    elif child.tag == "options":
        root.request.options = child

    elif child.tag == "logging":
        root.request.logging = child

    elif child.tag == "header":
        root.header = child

    return root


class Client:
    def __init__(
        self, cred: Credentials, lang: list, elements: list | None = None
    ) -> None:
        self.cred = cred
        self.lang = Search(lang)

    def request(
        self,
        url: str,
        method_name: MethodName,
        data: BaseType | None = None,
        _print: Literal[True, False] = False,
    ) -> dict:
        """
        Makes a post request to the given URL with the specified data and method name.

        data: ElementTree with the data required in the XML
        url: Service URL
        method: Method to be executed by the service
        """

        method = Method(method_name)

        root = method.get_base_xml(self.cred, self.lang)

        if data is not None:
            root = change_structure(root, data)

        if _print is True:
            print(ET.tostring(root.request.to_xml(), encoding="unicode"))

        response = requests.post(
            url,
            data=ET.tostring(root.to_xml(), encoding="unicode"),
            headers={"Content-Type": "application/xml"},
        )

        responseRoot = xmltodict.parse(response.content)
        error = responseRoot["root"]["header"]["error"]
        if int(error["code"]) > 0:
            raise Exception(
                f'MSS returned an error: code {error["code"]}, message: "{error["message"]}"'
            )

        return refine_response(responseRoot["root"], method_name)


def refine_response(resp: dict, meth: MethodName) -> dict:
    if meth == MethodName.GetHotelList:
        return refine_getHotelList(resp)

    return resp


def refine_getHotelList(resp: dict) -> dict:
    if resp["result"] is None:
        return resp
    elif "hotel" not in resp["result"] or resp["result"]["hotel"] is None:
        return resp
    elif not isinstance(resp["result"]["hotel"], list):
        resp["result"]["hotel"] = [resp["result"]["hotel"]]

    for hotel in resp["result"]["hotel"]:
        ensure_list_value(hotel, "pictures", "picture")
        ensure_list_value(hotel, "gallery", "picture")
        ensure_list_value(hotel, "features_view", "feature")
        ensure_list_value(hotel, "pos", "id_pos")

    return resp


def ensure_list_value(hotel: dict, parent_fld: str, child_fld: str) -> None:
    if parent_fld not in hotel:
        hotel[parent_fld] = {child_fld: []}
    elif not isinstance(hotel[parent_fld][child_fld], list):
        hotel[parent_fld][child_fld] = [hotel[parent_fld][child_fld]]
