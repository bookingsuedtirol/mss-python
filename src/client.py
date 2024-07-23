import requests
from os import getenv
import xml.etree.ElementTree as ET
from src.request.methods import *
from src.request.types_mss import *

# TODO types which were created must somehow be able to build the XML tree


class Client:
    def __init__(
        self, cred: Credentials, lang: str, elements: list | None = None
    ) -> None:
        # self.xml = get_base_xml(lang)
        # self.xml = xml_add(self.xml, elements)
        self.cred = cred
        self.lang = Search(lang)

    def request(self, data: ET.Element, url: str, method_name: str) -> ET.Element:
        """
        Makes a post request to the given URL with the specified data and method name.

        data: ElementTree with the data required in the XML
        url: Service URL
        method: Method to be executed by the service
        """

        method = Method.get_method(method_name)

        # ET.SubElement(data.find("header"), "method").text = method
        xml = method.get_base_xml(self.cred, self.lang)

        response = requests.post(
            url,
            data=ET.tostring(xml, encoding="unicode"),
            headers={"Content-Type": "application/xml"},
        )

        root = ET.fromstring(response.content)
        error = root.find("header").find("error")
        if int(error.find("code").text) > 0:
            raise Exception(
                f'MSS returned an error: code {error.find("code").text}, message: "{error.find("message").text}"'
            )

        return root
