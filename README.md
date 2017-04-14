# PoE Item Info

A [Path of Exile](https://www.pathofexile.com/) item info script for Linux.

Pressing ctrl-c in game while hovering over an item will copy the item's stats to the clipboard. The program watches the clipboard for changes. If it sees an item, it reports some information about it as a desktop notification. Currently supported modes are:

* Checking the price of Unique items on [poe.trade](http://poe.trade/).
* Checking the price of Divination Cards.
* Calculating the damage per second (DPS) of a weapon. This is reported as total DPS, elemental DPS (eDPS), and chaos DPS (cDPS).
* Seeing what map results from vendoring three of a given map (and what maps vendor into it).

Program settings are loaded from a file called `settings.json`, where you can specify which league to check prices in, and any extra headers or cookies to add to requests. If not specified, the league defaults to Standard. An example settings file is included called `example_settings.json`.

## Dependancies:

* `xsel` external program for checking the clipboard
* `notify-send` external program for displaying prices
* `requests` python module for downloading price information
* `pyquery` python module for parsing price information
