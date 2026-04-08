import json

class IExporter:
    def export(self, data: list) -> str:
        """Метод, який мають реалізувати всі експортери"""
        pass

class JsonExporter(IExporter):
    def export(self, data: list) -> str:
        return json.dumps(data, ensure_ascii=False, indent=4)

class LegacyExternalXmlGenerator:
    def generate_weird_xml(self, dict_data: list) -> str:
        xml = '<?xml version="1.0" encoding="UTF-8"?>\n<hotels>\n'
        for item in dict_data:
            xml += f'  <hotel name="{item["name"]}" rating="{item["star_rating"]} stars"/>\n'
        xml += '</hotels>'
        return xml

class XmlAdapter(IExporter):
    def __init__(self):
        self._legacy_generator = LegacyExternalXmlGenerator()

    def export(self, data: list) -> str:
        return self._legacy_generator.generate_weird_xml(data)

class ExporterFactory:
    @staticmethod
    def get_exporter(format_type: str) -> IExporter:
        """Фабричний метод: вирішує, який об'єкт створити на основі параметра"""
        if format_type == 'json':
            return JsonExporter()
        elif format_type == 'xml':
            return XmlAdapter()
        else:
            raise ValueError(f"Формат {format_type} не підтримується!")