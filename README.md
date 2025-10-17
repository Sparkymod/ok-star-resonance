<div align="center">
  <h1 align="center">
    <img src="icons/icon.png" width="200"/>
    <br/>
    ok-star-resonance
  </h1> 
<h3><i>Image recognition-based automation for Blue Protocol: Star Resonance, uses Windows API to simulate user clicks, does not read game memory or invasively modify game files/data.</i></h3>
</div>

![Static Badge](https://img.shields.io/badge/platfrom-Windows-blue?color=blue)
[![GitHub release (with filter)](https://img.shields.io/github/v/release/sanheiii/ok-star-resonance)](https://github.com/sanheiii/ok-star-resonance/releases)
[![GitHub all releases](https://img.shields.io/github/downloads/sanheiii/ok-star-resonance/total)](https://github.com/sanheiii/ok-star-resonance/releases)

# Disclaimer
This software is an external tool designed to automate gameplay in Blue Protocol: Star Resonance. It interacts with the game only through the existing user interface and complies with relevant laws and regulations. This software package is designed to simplify user interaction with the game and does not disrupt game balance or provide unfair advantages, nor does it modify any game files or code.

This software is open source and free, intended solely for personal learning and communication purposes, limited to personal game accounts, and must not be used for any commercial or profit-making purposes. The development team holds the final interpretation rights for this project. All issues arising from the use of this software are unrelated to this project and the development team. If you discover merchants using this software for boosting services and charging fees, this is the merchant's personal behavior. This software is not authorized for boosting services, and any resulting issues and consequences are unrelated to this software. This software does not authorize anyone to sell it. Sold versions of the software may contain malicious code, leading to theft of game accounts or computer data, which is unrelated to this software.

### Download
* [GitHub Download](https://github.com/sanheiii/ok-star-resonance/releases)
* [Quark Drive](https://pan.quark.cn/s/53ef87577da9?pwd=nVL9)

### Features
1. Fishing
2. Simple gathering

### Characteristics
1. Works at any 16:9 resolution, supports windowed and fullscreen modes, no screen scaling requirements
2. Cannot run in background
3. AI recognition of fish position for precise casting

### To-Do
1. Retrain the splash recognition model to fix the issue of incorrectly identifying character names and boats as splashes

### Low Priority
1. Don't want to use fixed routes for gathering implementation; automatic recognition and pathfinding are difficult to implement, added a continuous F-key press for now
2. Purchase bait and fishing rods - prioritize bug fixes, users can buy in advance
3. Farm cosmetics in normal extreme spaces - high difficulty, waiting for ideas

### If Issues Occur, Please Check
If you have problems, click here and check each item before asking:
1. **Wrong fish reeling direction:** In the fishing interface, press O to hide other players' and your own character name display, and ensure there are no boats at your fishing spot. These elements may currently be incorrectly identified as splashes
2. **Slow fish pulling, high reeling latency:** Script performance is limited. You can lower the game resolution to improve script refresh rate. If running during daytime, you can disable the auto-click monthly card function
3. **Can/cannot perform focused gathering:** Gathering depends on text recognition. Adjust the camera angle so that quest guidance doesn't overlap with the gathering button and interfere with recognition
4. **Extraction issues:** Extract the archive to a directory containing only English characters.
5. **Antivirus interference:** Add the download and extraction directories to your antivirus software/Windows Defender whitelist.
6. **Display settings:** Ensure the game uses 16:9 resolution, disable graphics card filters and sharpening. Use default game brightness and disable FPS display overlays (like overlays).
7. **Custom key bindings:** If not using default keys, please configure them in the app. Keys not in settings are not supported.
8. **Outdated version:** Ensure you are using the latest version of ok-star-resonance.
9. **Further help:** If the problem persists, please submit a screenshot and script log when the error occurs.

### Running from Python Source
Only supports Python 3.12
```
# CPU version, uses OpenVINO
pip install -r requirements.txt --upgrade # install python dependencies, may need to rerun after code updates
python main.py # run the release version
python main_debug.py # run the debug version
```

### Acknowledgments
* This program is developed based on [ok-script](https://github.com/ok-oldking/ok-script).
