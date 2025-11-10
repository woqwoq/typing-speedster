## Demo
![](https://github.com/woqwoq/typing-speedster/blob/main/demo/Public_Release_Demo_1.gif)

## TODO
### **Fixes** 
- Fix the WPM calculation formula tweakery
- Fix the default difficulty to app's default difficulty
- Fix cursor not displaying on newline char
- Fix keyboard input moving after the first results
- Fix perforamnce issues with `KeypressDisplay`
- Fix accepting a completely unmatching text

### **Best Practices** 
- Move border styling from python to css
- Encapsulate keyboard input from high-level typing-test functionality
- Add dynamic config
- Add scroallable container to attempt entry's tooltip
- Cleanup `ResultsScreen`

### **Features** 
- Replace unmatched char to what it should be
- Add hit-ratio influence for the formulas
- Add different modes x
- Add themes
- Add custom text
- Add stats
- Add json database for attempts/stats

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
## Notes
- Before usage, make sure to add some sort of dictionary in `/dicts/` and change the config in `main.py` (later will be handled with a dynamic config).
- Oxford 3000 Dictionary is available at `https://github.com/sapbmw/The-Oxford-3000`
