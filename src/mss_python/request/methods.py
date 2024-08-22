from __future__ import annotations

from .method_names import MethodName
from .types_mss import Credentials, Search, Root, Header, Request


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
