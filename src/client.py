import requests
import xmltodict
from request.methods import *
from request.types_mss import *


# maybe recursion should be used instead of doing if checks
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
        # self.xml = get_base_xml(lang)
        # self.xml = xml_add(self.xml, elements)
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

        if data != None:
            root = change_structure(root, data)

        if _print == True:
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

        # import pdb

        # pdb.set_trace()

        return refine_response(responseRoot["root"], method_name)


def refine_response(resp: dict, meth: MethodName) -> dict:
    if meth == MethodName.GetHotelList:
        return refine_getHotelList(resp)

    return resp


def refine_getHotelList(resp: dict) -> dict:
    if resp["result"] == None:
        return resp
    elif "hotel" not in resp["result"] or resp["result"]["hotel"] == None:
        return resp
    elif type(resp["result"]["hotel"]) != list:
        resp["result"]["hotel"] = [resp["result"]["hotel"]]

    for x in resp["result"]["hotel"]:
        if "pictures" not in x:
            x["pictures"] = {"picture": []}
        elif type(x["pictures"]["picture"]) != list:
            x["pictures"]["picture"] = [x["pictures"]["picture"]]

        if "gallery" not in x:
            x["gallery"] = {"picture": []}
        elif type(x["gallery"]["picture"]) != list:
            x["gallery"]["picture"] = [x["gallery"]["picture"]]

        if "features_view" not in x:
            x["features_view"] = {"feature": []}
        elif type(x["features_view"]["feature"]) != list:
            x["features_view"]["feature"] = [x["features_view"]["feature"]]

        if "pos" not in x:
            x["pos"] = {"id_pos": []}
        elif type(x["pos"]["id_pos"]) != list:
            x["pos"]["id_pos"] = [x["pos"]["id_pos"]]

            # if "channel" not in x:
            #     x["channel"] = {"picture": []}
            # elif type(x["channel"]["picture"]) != list:
            #     x["channel"]["picture"] = [x["channel"]["picture"]]

    return resp
