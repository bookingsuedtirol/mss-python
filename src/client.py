import requests
import xmltodict
from src.request.methods import *
from src.request.types_mss import *


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
        self, cred: Credentials, lang: str, elements: list | None = None
    ) -> None:
        # self.xml = get_base_xml(lang)
        # self.xml = xml_add(self.xml, elements)
        self.cred = cred
        self.lang = Search(lang)

    def request(
        self,
        url: str,
        method_name: str,
        data: ET.Element | None = None,
        _print: True | False = False,
    ) -> ET.Element:
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

        return responseRoot["root"]
