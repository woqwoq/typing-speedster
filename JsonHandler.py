import json

message = """def __init__(self, file_path, schema, schema_preprocess):
        self.file_path = file_path

        self.schema = schema
        self.schema_preprocess = schema_preprocess

        self.contents = self._parse_json(file_path)"""

SCHEMA = ['entry_desc', 'entry_text']
SCHEMA_PREPROCESS = [False, True]


class JsonHandler:

    def __init__(self, file_path, schema, schema_preprocess):
        self.file_path = file_path

        self.schema = schema
        self.schema_preprocess = schema_preprocess

        self.contents = self._parse_json(file_path)


    def _parse_json(self, file_path):
        file = open(file_path, 'r')
        contents = json.load(file)
        file.close()

        return contents

    def _split_keep_delimiter(self, txt, delimiter):
        return [line + delimiter for line in txt.split(delimiter) if line]

    def _remove_last_newline(self, arr):
        if arr:
            arr[-1] = arr[-1].rstrip('\n')

        return arr

    def _preprocess_code(self, code: str):
        if not code:
            return code
        
        code = code.replace("    ", "\t")
        code_lines = self._split_keep_delimiter(code, '\n')
        code_lines = self._remove_last_newline(code_lines)

        return code_lines
    
    def _preprocess_if_applicable(self, entry_data):        
        for i in range(len(entry_data)):
            if self.schema_preprocess[i]:
                entry_data[i] = self._preprocess_code(entry_data[i])
        
        return entry_data
    
    def write_json(self):
        file = open(self.file_path, 'w')
        json.dump(self.contents, file, indent=4)

    def _assemble_entry(self, entry_data):
        if len(entry_data) != len(self.schema):
            return None

        entry_data = self._preprocess_if_applicable(entry_data)

        entry = {}
        for i in range(len(self.schema)):
            entry[self.schema[i]] = entry_data[i]

        return entry

    def add_json_entry(self, entry_data, write: bool = False):
        entry = self._assemble_entry(entry_data)
        if entry:
            self.contents.append(entry)

        if write:
            self.write_json()

    def remove_entry(self, number, write: bool = False):
        if number > len(self.contents)-1:
            return
        
        self.contents.pop(number)

        if write:
            self.write_json()
        
    def __str__(self):
        return str(json.dumps(self.contents, indent=4))


handler = JsonHandler('dicts/Code.txt.concept', SCHEMA, SCHEMA_PREPROCESS)

handler.add_json_entry(["c code", message])

print(handler)
