__author__ = 'xp'

import io
import re
import xml.sax

from typing import Any, List, Tuple, Optional
from xml.sax import make_parser, ContentHandler

from src.document import Document


re_spaceless = re.compile('\s+', re.MULTILINE)


class Node(object):
    def __init__(self, element: bool, parent: 'Optional[ElementNode]'):
        self.element = element
        self.parent = parent
        if parent is not None:
            parent.children.append(self)


class ElementNode(Node):
    def __init__(self, parent: 'Optional[ElementNode]', name: str, attrs):
        super().__init__(True, parent)
        self.name = name.lower()
        self.attributes = attrs
        self.children = []  # type: List[Node]

    def child(self, name) -> 'Optional[ElementNode]':
        for node in self.children:
            if isinstance(node, ElementNode) and node.name == name:
                return node
        return None

    def __str__(self):
        s = ''
        for node in self.children:
            s += str(node) + ' '
        return re_spaceless.sub(' ', str(s)).strip()


class ValueNode(Node):
    def __init__(self, parent: 'Optional[ElementNode]', value: Any):
        super().__init__(True, parent)
        value = re_spaceless.sub(' ', str(value))
        self.value = value.strip()

    def __str__(self):
        return self.value


class _Handler(ContentHandler):

    def __init__(self):
        super().__init__()
        self.stack = None  # type: List[ElementNode
        self.topNode = None  # type: Optional[ElementNode]
        self.docs = None  # type: List[Document]

    def startDocument(self):
        self.stack = []
        self.docs = []

    def endDocument(self):
        if len(self.stack) > 0:
            raise EOFError()

    def startElement(self, name: str, attrs):
        node = ElementNode(self.topNode, name, attrs)
        self.stack.append(node)
        self.topNode = node

    def characters(self, content: str):
        node = ValueNode(self.topNode, content)

    def endElement(self, name: str):
        if self.topNode.name != name.lower():
            raise AssertionError('found %s, should be %s' % (self.topNode.name, name))

        if self._check('doc'):
            id_node = self.topNode.child('docno')
            id = str(id_node)
            if id_node is not None:
                id_node.children.clear()

            title_node = self.topNode.child('title')
            title = str(title_node)
            if title_node is not None:
                title_node.children.clear()

            body = str(self.topNode)
            if len(body) > 0:
                doc = Document(id, title, body)
                self.docs.append(doc)

        self.stack.pop()
        self.topNode = self.stack[-1] if len(self.stack) > 0 else None

    def _index(self, name: str) -> int:
        for index, node in enumerate(self.stack):
            if node.name == name:
                return index
        return -1

    def _check(self, *args: str) -> bool:
        if self.topNode is None or self.topNode.name != args[-1]:
            return False

        pos = -1
        for name in args[:-1]:
            cur = self._index(name)
            if cur <= pos:
                return False
            pos = cur
        return True


class Parser(object):
    def __init__(self):
        self.docs = []  # type: List[Document]

    def load(self, text: str):
        text = '<root>' + text + '</root>'
        parser = make_parser()  # type: xml.sax.xmlreader.XMLReader
        handler = _Handler()
        parser.setFeature(xml.sax.handler.feature_namespaces, False)
        parser.setFeature(xml.sax.handler.feature_validation, False)
        parser.setFeature(xml.sax.handler.feature_external_ges, False)
        parser.setFeature(xml.sax.handler.feature_external_pes, False)
        parser.setContentHandler(handler)

        source = xml.sax.InputSource()
        source.setCharacterStream(io.StringIO(text))
        parser.parse(source)

        self.docs.extend(handler.docs)


if __name__ == '__main__':
    parser1 = Parser()
    with open('../assets/trecs/shakespeare-merchant.trec.1') as f:
        text1 = f.read()
        parser1.load(text1)
        doc1 = parser1.docs[0]
        assert doc1.number == 'SHK-MOV-0-0'
        assert doc1.title == 'THE MERCHANT OF VENICE'
