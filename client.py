import requests
from os import getenv
import xml.etree.ElementTree as ET


def make_xml_request(data: ET.Element, url: str, method: str) -> requests.Response:
    """
    Makes a post request to the given URL with the specified data and method name.

    data: ElementTree with the data required in the XML
    url: Service URL
    method: Method to be executed by the service
    """
    return requests.post(
        url,
        data=ET.tostring(data, encoding="unicode"),
        headers={"Content-Type": "application/xml"},
    )


def get_base_xml(lang: str) -> ET.Element:
    """
    Returns an XML (ElementTree) with the mandatory elements needed for the request.
    """
    USER = getenv("MSS_SERVICE_USERNAME")
    PASSWORD = getenv("MSS_SERVICE_PASSWORD")
    SOURCE = getenv("MSS_SERVICE_SOURCE")
    temp = {}
    temp["user"] = USER
    temp["password"] = PASSWORD
    temp["source"] = SOURCE

    root = ET.Element("root")
    headers = ET.SubElement(root, "header")
    credentials = ET.SubElement(headers, "credentials")
    for x in temp:
        ET.SubElement(credentials, x).text = temp[x]

    ET.SubElement(
        ET.SubElement(ET.SubElement(root, "request"), "search"), "lang"
    ).text = lang
    # return ET.ElementTree(root)
    return root


# def xml_add(root, elements):
#     """
#     Add new elements to an XML Element

#     root = Target XML
#     elements = list of elements to be added
#     """
#     for x in elements:
#         for y in root:
#         if root.find(element) is None:


class Client:
    def __init__(self, lang, elements: list | None = None) -> None:
        self.xml = get_base_xml(lang)
        # self.xml = xml_add(self.xml, elements)

    def request(self, data: ET.Element, url: str, method: str) -> ET.Element:
        """
        Makes a post request to the given URL with the specified data and method name.

        data: ElementTree with the data required in the XML
        url: Service URL
        method: Method to be executed by the service
        """
        ET.SubElement(data.find("header"), "method").text = method
        response = requests.post(
            url,
            data=ET.tostring(data, encoding="unicode"),
            headers={"Content-Type": "application/xml"},
        )

        root = root = ET.fromstring(response.content)
        error = root.find("header").find("error")
        if int(error.find("code").text) > 0:
            raise Exception(
                f'MSS returned an error: code {error.find("code").text}, message: "{error.find("message").text}"'
            )

        return root

    def add_child_xml(self, child: ET.Element | None, parent: ET.Element | None = None):
        # print(child.tag)

        if parent is None:
            parent = self.xml

        if child is None:
            print("Exists")
            return

        if len(child[:]) == 0:
            print("Exists")
            return

        for x in parent:
            print("loop")
            if x.tag == child.tag:
                print(x.tag)
                self.add_child_xml(x, child[0])

        parent.append(child)
        print("Appended")
