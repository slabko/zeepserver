import lxml
import zeep.loader
from zeep.settings import Settings


def operation_name(document):
    return lxml.etree.QName(document[0][0].tag).localname


def parse_xml(data):
    return zeep.loader.parse_xml(data, None, settings=Settings())
