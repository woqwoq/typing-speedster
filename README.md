## Demo
![](https://github.com/woqwoq/typing-speedster/blob/main/demo/Public_Release_Demo_1.gif)

## TODO
### **Fixes** 
- ~~Fix the WPM calculation formula tweakery~~✅
- ~~Fix the default difficulty to app's default difficulty~~✅
- ~~Fix cursor not displaying on newline char~~✅
- ~~Fix keyboard input moving after the first results~~✅
- Fix perforamnce issues with KeypressDisplay: They're back...
- ~~Fix accepting a completely unmatching text~~✅ Now final WPM is affected by accuracy
- Fix results graph showing RAW WPM instead of real?

### **Best Practices** 
- ~~Move border styling from python to css~~✅
- ~~Encapsulate keyboard input from high-level typing-test functionality~~✅
- Add dynamic config
- ~~Add scroallable container to attempt entry's tooltip~~❌Not doable
- ~~Cleanup ResultsScreen~~✅
- ~~Change `Code.txt` and `Lyrics.txt` to JSON~~✅

### **Features** 
- Replace unmatched char to what it should be
- ~~Add hit-ratio influence for the formulas~~✅
- Add different modes x
- ~~Add themes~~✅
- Add custom text
- Add stats (eror/key heatmaps)
- Add json database for attempts/stats
- Add command palette for the custom text
- Add punctuation and capital letter mode
- Add signs and capitals ONLY mode

## Project structure
```
.
├── core            - Core utilities and logic modules (e.g., text generation, difficulty handling)
├── dicts           - Text dictionaries used for typing practice
├── logs            - Application logs (currently not in active use)
├── main.py         - Main entry point for launching the application
├── messages        - Modules for internal widget and event communication
├── playground      - Sandbox for tests, experiments, and prototyping
├── screens         - Application screens / UI pages (e.g., results screen)
├── server.py       - Local server for backend functionality (if used)
├── styles          - All CSS files for UI styling
└── widgets         - GUI widgets and components (e.g., input fields, keypress displays)
```
## Dictionary Formats

The main formats for JSON data used by `TextGenerator` are defined by the schemas in `/core/TextGenerator.py`. For example:

`JSON_CODE_SCHEMA = ['entry_desc', 'entry_text']`
`JSON_CODE_SCHEMA_PREPROCESS = [False, True]`

### Explanation

- `entry_desc`: The first JSON attribute. It is used to display the description of the test on the typing test screen.
- `entry_text`: The second JSON attribute. It contains the actual text or code used in the typing test.

### Important Notes

1. The first and second attributes in any schema must always be present, as TextGenerator relies on them for proper functionality.
2. Additional attributes can be added to the schema, but their usage and handling must be explicitly defined in TextGenerator.
3. The `_PREPROCESS` list corresponds to each attribute in the schema and defines whether preprocessing (like cleaning or formatting) (defined in `_preprocess_code` in `/core/JsonHandler.py`) should be applied to that attribute.


## Notes
- Before usage, make sure to add some sort of dictionary in `/dicts/` and change the config in `main.py` (later will be handled with a dynamic config).
- Oxford 3000 Dictionary is available at `https://github.com/sapbmw/The-Oxford-3000`
