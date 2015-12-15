from lxml import etree

from settings import SCHEMA_FILE


def readXML(xmlfilename):
    try:
        with open(xmlfilename, 'r') as f:
           return etree.fromstring(f.read(), xmlparser)

    except etree.XMLSchemaError:
        return False
    except etree.XMLSyntaxError:
        return False
    except IOError as e:
        return False


with open(SCHEMA_FILE, 'r') as f:
    schema_root = etree.XML(f.read())

schema = etree.XMLSchema(schema_root)
xmlparser = etree.XMLParser(schema=schema)
