import xml.etree.ElementTree as ET
import requests

class DataLoader:
    def __init__(self, url):
        self.url = url

    def fetch_data(self):
        response = requests.get(self.url)
        if response.status_code == 200:
            return response.content
        else:
            raise Exception(f"Невозможно получить данные {self.url}")

    def parse_xml(self, variant_number):
        xml_data = self.fetch_data()
        root = ET.fromstring(xml_data)

        for variant in root.findall('variant'):
            if int(variant.get('number')) == variant_number:
                D = float(variant.get('D'))
                fmin = float(variant.get('fmin'))
                fmax = float(variant.get('fmax'))
                return (D, fmin, fmax)

        raise ValueError("Номер варианта не найден в XML данных.")
