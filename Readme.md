# Reddit bot using cvs lookups

## Libraries used
*  praw
*  time
*  re
*  pandas

## Description

A Reddit bot that performs key lookups on csv files.
It replies to users in a table format if the keyword is valid

An example is implemented for the Civilization series.

Given this :

```
{Assyria,civ5}
```

It replies with this:

civ| Assyria
---|---
leader| Ashurbanipal
ability| Treasures of Nineveh:	Treasures of Nineveh:When a city is conquered, gain a free Technology already discovered by its owner. Gaining a city through a trade deal does not count, and it can only happen once per enemy city.
start bias| Avoid Tundra
Unique unit| Siege tower (replaces Catapult)	
unique building|Royal library (replaces Library) 


Given this :

```
{Spearman vs Crossbowman,civ5}
```

It replies with this:

Unit|Spearman|Crossbowman
---|---|---
Production cost|56|120
Combat strength|11|13
Moves|2|2
Range|None|2
Ranged strength|None|18
Technology|Bronze working|Machinery
Upgrades to|Pikeman, Impi|Gatling gun
Notes|50% bonus vs. mounted units|May not melee attack


# Implementing for other games
The bot can be implemented for any other game as long as:
* Data in csv format.
* The file [game_config](game_config.py) must be edited to make it work for other games, documentation are included.

### Keyword  format 

`{Assyria,civ5}`

`civ5` is the name of the folder.

`Assyria` is a a row header in one of the files in `civ5` folder(in this case it is `civs.csv`).
