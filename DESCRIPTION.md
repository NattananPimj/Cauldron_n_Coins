GitHub repo: [https://github.com/NattananPimj/Cauldron_n_Coins](https://github.com/NattananPimj/Cauldron_n_Coins)


Presentation VDO: [https://youtu.be/7NU-JjIIUY4](https://youtu.be/7NU-JjIIUY4)

# Project Overview
Players play as the alchemist who makes the potion and sells it. Explore the world of brewing by moving the bottle around and find the perfect recipe while trying to make money to be the greatest alchemist.

The game will go by days. Each day a certain number of customers will visit your shop. The game is saved and the data is record at the end of the day

# Game Concept

The game is a different kind of open world. Players move around the map by different combinations of lines created by different herbs. Given the creative way to play the game. Also with a selling system for players to find the most satisfied potion for customers.

As the herbs are put into the cauldron, the path shown. To brew a potion the player has to put the path together until reach the specific point that is the certain type of potion. Also, to make the potion more precise, there is the system to drag the position toward original point for precise position

The map can be moved around to see where the path is going. Increase the play area for players to explore.

Since there will not be the herbs garden, the herbs are ready for the player. As the player picks up the herbs, a certain amount of money is deducted.

For selling, as the customer came and gave you their request. There is a haggle option to increase your price and make more profit.

When the player done the day, they can explore the brewing bad or go to bed to save and end the day.

# Object-Oriented Programming Implementation
16 classes [UML.pdf](6710545601%20UML%20class.pdf)
- **Class Config:** containing the game configuration, the stat of the potion and herbs
- **Class Game:** combine all the necessary method and call them, with the user event.
- **Class Drawer:** draw all the interface and asset, responsible for bedroom, restart popup, and tutorials
- **Class Map:** responsible for all brewing system, including create a Potion
- **Class Obstacle:** create the obstacle that will obstruct the brewing gameplay
- **Class HerbCabinet:** create an object in class Herb and sent to class Map
- **Class HerbManager:** create and storing HerbCabinet for calling
- **Class Herb:** store the information about herb while create a path for brewing session
- **Class ItemSlot:** store one item and display it on UI
- **Class Inventory[Singleton]:** store player data, load, and save player data
- **Class Haggling:** responsible for all haggling gameplay
- **Class Customer:** store request and all customer data
- **Class CustomerManager:** create customer and request, responsible for all shop system
- **Class Potion:** store potion information
- **Class DataCollector[Singleton]:** storing all the statistic data and save it to csv when the game is saved
- **Class DataApp:** display all the data collected


# Statistical Data
## Data Recording Method
csv saved in [database](database)
## Data Features
- Table data: Tracking the average profit and cost in each potion
- Graph Data:

| Feature name                                        | Graph objective                                                                                        | Graph type   | X-axis           | Y-axis       |
|-----------------------------------------------------|--------------------------------------------------------------------------------------------------------|--------------|------------------|--------------|
| Herb used                                           | show what herb and which direction that player preferred                                               | Bar chart    | Potion name      | frequency    |
| Distance taken to create a potion                   | show the efficient of path that player create                                                          | Scatter plot | Potion name      | distance     |
| Histograms of offering trials until fail or success | show how many trials would take a player to satisfied the customer or they were rejected/ running away | Histograms   | Number of trials | frequency    |
| Haggle success rate in each speed                   | show the difficulty of each speed of haggle                                                            | Bar chart    | Speed            | Success Rate |

# Goal:
- 50% all brewing section + inventory (By 16 Apr)
- 75% all selling system (By 23 Apr)
- 100% all done including data collection (**Deadline:** 11 May)

# Changed propose feature
- the way to calculate the path: instead of using function, I decided to used parametric equation. Make it more customizable.
 Also,Vertical and Horizontal herb are not needed, so they were removed

# Other sources
- getting music to run (cnc_main.py line 129-132)
    https://www.youtube.com/watch?v=pcdB2s2y4Qc

- music: misty wind -Troubadour- by HarumuchiMusic

    License Certificate: [folk-misty-wind-troubadour-164146-license.txt](Music%2Ffolk-misty-wind-troubadour-164146-license.txt)

    Source: [https://pixabay.com/](https://pixabay.com/)