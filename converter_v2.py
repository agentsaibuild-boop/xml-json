import xml.etree.ElementTree as ET
import json
import os
import glob

def parse_element(element):
    result = {}
    if element.attrib:
        result["@attributes"] = element.attrib
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

def xml_to_json(xml_file):
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
        data = {root.tag: parse_element(root)}
        json_file = xml_file.replace(".xml", ".json")
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"\n✅ Готово! Резултат: {json_file}")
        print("\n--- Преглед ---")
        print(json.dumps(data, indent=4, ensure_ascii=False))
    except ET.ParseError as e:
        print(f"\n❌ Грешка: XML файлът е невалиден! {e}")
    except FileNotFoundError:
        print(f"\n❌ Грешка: Файлът не е намерен!")

def convert_all():
    xml_files = glob.glob("*.xml")
    if not xml_files:
        print("\n❌ Няма XML файлове в папката!")
        return
    print(f"\nНамерени {len(xml_files)} XML файла:")
    for f in xml_files:
        print(f"  → {f}")
        xml_to_json(f)

def menu():
    while True:
        print("\n=============================")
        print("   XML → JSON Конвертор v2")
        print("=============================")
        print("1. Конвертирай конкретен файл")
        print("2. Конвертирай всички XML в папката")
        print("3. Изход")
        print("=============================")
        choice = input("Избери опция (1/2/3): ")

        if choice == "1":
            filename = input("Въведи името на XML файла: ")
            if not filename.endswith(".xml"):
                filename += ".xml"
            xml_to_json(filename)
        elif choice == "2":
            convert_all()
        elif choice == "3":
            print("\nДовиждане! 👋")
            break
        else:
            print("\n❌ Невалидна опция, опитай отново!")

menu()