import json

code_file = open('dicts/Code.txt.concept', 'r')
json_text = json.load(code_file)
code_file.close()

message = """#include <stdio.h>

int main() {
    printf("Hello, World!");
    return 0;
}"""

SCHEMA = ['']


class JsonHandler:

    def __init__(self, file_path):
        self.file_path = file_path
        
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
    
    def _write_json(self):
        file = open(self.file_path, 'w')
        json.dump(self.contents, file, indent=4)

    def add_json_entry(self, entry_text, write: bool = False):
        entry_text = self._preprocess_code(entry_text)
        if self.contents and entry_text:
            self.contents.append({'entry_number' : len(self.contents), 'entry_text' : entry_text})

        if write:
            self._write_json()

    def remove_entry(self, number, write: bool = False):
        if number > len(self.contents)-1:
            return
        
        self.contents.pop(number)

        if write:
            self._write_json()
        
    def __str__(self):
        return str(json.dumps(self.contents, indent=4))


handler = JsonHandler('dicts/Code.txt.concept')

handler.add_json_entry(message)
handler.remove_entry(4)

print(handler)
