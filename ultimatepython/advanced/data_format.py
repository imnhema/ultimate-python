import json
from csv import DictReader
from dataclasses import dataclass, fields
from io import StringIO
from xml.etree import ElementTree as ETree

# Module-level constants
_JSON_FILE = StringIO("""
[
    {
        "author": "John",
        "title": "Summer",
        "body": "Summer time is hot"
    },
    {
        "author": "Jane",
        "title": "Winter",
        "body": "Winter time is cold"
    }
]
""")
_XML_FILE = StringIO("""
<notepad>
    <note>
        <author>John</author>
        <title>Summer</title>
        <body>Summer time is hot</body>
    </note>
    <note>
        <author>Jane</author>
        <title>Winter</title>
        <body>Winter time is cold</body>
    </note>
</notepad>
""")
_CSV_FILE = StringIO("""
John,Summer,Summer time is hot
Jane,Winter,Winter time is cold
""")


@dataclass
class Note:
    """Note model."""
    author: str
    title: str
    body: str

    @classmethod
    def from_data(cls, data):
        """Create note from dictionary data."""
        return cls(**data)

    @classmethod
    def fields(cls):
        """Get field names to simplify parsing logic."""
        return tuple(field.name for field in fields(cls))


def main():
    # Let's use `json.load` to parse note data from the JSON file
    json_content = json.load(_JSON_FILE)
    json_notes = [Note.from_data(data) for data in json_content]
    assert all(isinstance(note, Note) for note in json_notes)

    # Let's use `Etree.parse` to parse note data from the XML file
    tree = ETree.parse(_XML_FILE)
    root_el = tree.getroot()
    xml_notes = []
    for note_el in root_el:
        xml_notes.append(Note.from_data({
            attr_name: note_el.findtext(attr_name)
            for attr_name in Note.fields()
        }))

    # Let's use `csv.DictReader` to parse note data from the CSV file
    csv_reader = DictReader(_CSV_FILE, fieldnames=Note.fields())
    csv_notes = [Note.from_data(row) for row in csv_reader]
    assert all(isinstance(note, Note) for note in csv_notes)

    # Note data is still the same between all three formats
    for json_note, xml_note, csv_note in zip(json_notes, xml_notes, csv_notes):
        assert json_note == xml_note == csv_note, f"{json_note} | {xml_note} | {csv_note}"


if __name__ == "__main__":
    main()