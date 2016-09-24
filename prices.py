#!/usr/bin/env python
#coding: utf-8

import subprocess
import time
import requests
from pyquery import PyQuery as pq


league = "Essence"

max_shown = 5

default_data = {
    "league": "",
    "name": "",
    "online": "x",
    "capquality": "x",
}


def get_clipboard():
    return subprocess.check_output(["xsel", "-b"])


def notify(title, body="", timeout=5000):
    subprocess.call(["notify-send", "-t", str(timeout), title, body])


def get_prices(name):
    data = dict(default_data)
    data["league"] = league
    data["name"] = name
    r = requests.post("http://poe.trade/search", data=data)

    doc = pq(r.text)
    elements = doc(".item .currency")

    prices = []
    for e in elements:
        currency = e.attrib["class"].split("-")[-1]
        amount = e.text[:-1]
        prices.append((currency, amount))

    return prices


def format_prices(prices):
    result = "%d%s offers\n" % (len(prices), "+" if len(prices)==99 else "")
    result += "-"*20 + "\n"
    for p in prices[:max_shown]:
        result += "%s %s\n" % (p[1], p[0])
    result += u"⋮\n"
    for p in prices[-max_shown:]:
        result += "%s %s\n" % (p[1], p[0])
    return result.strip()


def main():
    prev_clip = None
    while True:
        clip = get_clipboard()
        if clip != prev_clip:
            if "Rarity: Unique\n" in clip and "\n--------\n" in clip and "\nUnidentified" not in clip:
                split = clip.split("\n")
                name = split[1].split(">")[-1]
                base = split[2]

                prices = format_prices(get_prices("%s %s" % (name, base)))

                notify(name, prices)
            prev_clip = clip
        time.sleep(0.1)


if __name__ == "__main__":
    main()
