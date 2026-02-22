import xml.etree.ElementTree as ET
import json

def xml_to_json(xml_file, json_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    
    def parse_element(element):
        result = {}
        
        # Атрибути
        if element.attrib:
            result["@attributes"] = element.attrib
        
        # Деца
        children = list(element)
        if children:
            for child in children:
                child_data = parse_element(child)
                if child.tag in result:
                    if not isinstance(result[child.tag], list):
                        result[child.tag] = [result[child.tag]]
                    result[child.tag].append(child_data)
                else:
                    result[child.tag] = child_data
        else:
            return element.text or ""
        
        return result
    
    data = {root.tag: parse_element(root)}
    
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    
    print(f"Готово! JSON файлът е записан в: {json_file}")

# Стартиране
xml_to_json("input.xml", "output.json")