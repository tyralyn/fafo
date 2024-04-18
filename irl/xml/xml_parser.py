from xml.etree import ElementTree as ET

SAMPLE_FILENAME="/Users/tyralyn/yen/fafo/fafo/irl/xml/xml.txt"

class XMLParser(object):
    def get_data_from_xml(self, input_xml):
        tree = ET.fromstring(input_xml)
        if len(tree.findall(r'Name')) > 1:
            raise XMLFoundTooManyElementsError()

        result = {
            'name': tree.findall(r'Name')[0].text,
            'strategies': [],
        }
        
        def parse_bool(bool_str):
            match_str = bool_str.casefold()
            match match_str:
                case "false":
                    return False
                case "true":
                    return True
                case _:
                    raise XMLBooleanParsingError()
                    
        def parse_int(int_str):
            try:
                result = int(int_str)
            except ValueError:
                raise XMLIntegerParsingError()
            return result
                    
        for element in tree.findall(r'TradingStrategies/TradingStrategy'):
            enabled_str = element.attrib['enabled']
            multiplier_str = int(element.findall(r'Multiplier')[0].text)
            
            result['strategies'].append({
                'enabled': parse_bool(enabled_str),
                'multiplier': parse_int(multiplier_str),
                'symbols': [symbol.text for symbol in element.findall(r'Symbols/Symbol')]
            })
            
        return result
    

f = open(SAMPLE_FILENAME, 'r')
f_contents_whole = f.read()

x = XMLParser()
print(x.get_data_from_xml(f_contents_whole))