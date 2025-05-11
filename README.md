# Cauldron & Coins

# Table of Contents

- [Installation](#Installation)
- [A list of files and a brief description of classes it contains](#A list of files and a brief description of classes it contains)
  - [Python file](#python-file)
    - [cnc_main.py](#cnc_mainpy)
    - [cnc_config.py](#cnc_configpy)
    - [cnc_draw.py](#cnc_drawpy)
    - [cnc_game.py](#cnc_gamepy)
    - [cnc_herbManager.py](#cnc_herbManagerpy)
    - [cnc_herbs.py](#cnc_herbspy)
    - [cnc_inventory.py](#cnc_inventorypy)
    - [cnc_map.py](#cnc_mappy)
    - [cnc_potion.py](#cnc_potionpy)
    - [dataCollecting.py](#datacollectingpy)
    - [datadisplay.py](#datadisplaypy)
  - [Folders](#folders)
    - [customer folder](#customer-folder)
    - [IngamePic folder](#ingamepic-folder)
    - [Music folder](#music-folder)
  - [Other Files](#other-files)
    - [6710545601 UML class.pdf](#6710545601-uml-classpdf)
    - [DESCRIPTION.md](#descriptionmd)
    - [LICENSE](#license-file)
    - [requirement.txt](#requirementtxt)



# Installation
1. download or clone the project. (cloning using this command)
    ```githubexpressionlanguage
   git clone https://github.com/NattananPimj/Cauldron_n_Coins.git
    ```

2. download all the library and package following in **[requirement.txt]()** 

3. run the **[cnc_main.py](cnc_main.py)**

# A list of files and a brief description of classes it contains

## Python file
### [cnc_main.py](cnc_main.py)
This is the main part of the program, there is no class in here. 
Only the main run and music volume that user can change by their satisfaction

### [cnc_config.py](cnc_config.py)
file containing the game configuration, the stat of the potion and herbs.<br/>
#### Class Config:
containing the game configuration, the stat of the potion and herbs

### [cnc_draw.py](cnc_draw.py)
draw all interface
#### Class Drawer:
draw all the interface and asset, responsible for bedroom, restart popup, and tutorials

### [cnc_game.py](cnc_game.py)
contain and connect all class together
#### Class Game:
combine all the necessary method and call them, with the user event.

### [cnc_herbManager.py](cnc_herbManager.py)
store the interaction between herb and map
#### Class HerbCabinet:
create an object in class Herb and sent to class Map
#### Class HerbManager:
create and storing HerbCabinet for calling

### [cnc_herbs.py](cnc_herb.py)
#### Class Herb:
store the information about herb while create a path for brewing session

### [cnc_inventory.py](cnc_inventory.py)
#### Class ItemSlot:
store one item and display it on UI
#### Class Inventory: (Singleton)
store player data, load, and save player data
#### Class Haggling:
responsible for all haggling gameplay
#### Class Customer:
store request and all customer data
#### Class CustomerManager:
create customer and request, responsible for all shop system

### [cnc_map.py](cnc_map.py)
#### Class Map:
responsible for all brewing system, including create a Potion

### [cnc_potion.py](cnc_potion.py)
#### Class Potion:
store potion information

### [dataCollecting.py](dataCollecting.py)
#### class DataCollector: (Singleton)
storing all the statistic data and save it to csv when the game is save

### [datadisplay.py](datadisplay.py)
#### class DataApp:
display all the data collected

## Folders

### [customer folder](customer)
containing all assets of customer

### [IngamePic folder](IngamePic)
containing all assets in game

### [Music folder](Music)
containing game's background music with its license certificate

## Other files

### [6710545601 UML class.pdf](6710545601%20UML%20class.pdf)
UML class

### [DESCRIPTION.md](DESCRIPTION.md)
the details of the project

### [LICENSE file](LICENSE)
the project License

### [requirement.txt](requirements.txt)