# Reddit bot using cvs lookups

## Libraries used
*  praw
*  time
*  re
*  pandas

## Description

A python reddit bot that performs key lookups on csv files.
It replies to users in a table format if the keyword is valid

An example is implemented for a Civilization game.

Given this :

```
{Assyria,civ5}
```

It replies with this 


civ| Assyria
---|---
leader| Ashurbanipal
ability| Treasures of Nineveh:	Treasures of Nineveh:When a city is conquered, gain a free Technology already discovered by its owner. Gaining a city through a trade deal does not count, and it can only happen once per enemy city.
start bias| Avoid Tundra
Unique unit| Siege tower (replaces Catapult)	
unique building|Royal library (replaces Library) 


