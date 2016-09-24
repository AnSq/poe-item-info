# PoE Unique Price Checker

A [Path of Exile](https://www.pathofexile.com/) unique item price checker for Linux.

Pressing ctrl-c in game while hovering over an item will copy the item's stats to the clipboard. The program watches the clipboard for changes. If it sees a unique item in it, it checks its price on [poe.trade](http://poe.trade/). It then displays a notification with the cheapest and most expensive offers available.

TODO: Make the league configurable. Currently it's hard-coded to Essence league.

Dependancies:

* `xsel` external program for checking the clipboard
* `notify-send` external program for displaying prices
* `requests` python module for downloading price information
* `pyquery` python module for parsing price information
