#!/usr/bin/env python
#coding: utf-8

import subprocess
import time
import json
import requests
import os
from pyquery import PyQuery as pq


settings = {}

max_shown = 5

default_data = {
    "league": "",
    "name": "",
    "online": "x",
    "capquality": "x",
}


def get_clipboard():
    return subprocess.check_output(["xsel", "-b"])


def notify(title, body="", timeout=8000):
    subprocess.call(["notify-send", "-t", str(timeout), title, body])


def get_prices(name):
    league = settings["league"] if "league" in settings else "Standard"
    headers = settings["headers"] if "headers" in settings else {}
    cookies = settings["cookies"] if "cookies" in settings else {}

    data = dict(default_data)
    data["league"] = league
    data["name"] = name

    r = requests.post("http://poe.trade/search", data=data, headers=headers, cookies=cookies)

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


def calc_dps(split):
    p_dmg = None
    e_dmg = None
    c_dmg = None
    p_dps = None
    e_dps = None
    c_dps = None
    dps   = None
    aps   = None
    for line in split:
        if line.startswith("Physical Damage: "):
            p_dmg = line_to_dmg(line)
        elif line.startswith("Elemental Damage: "):
            e_dmg = sum(sum(float(y) for y in x.split()[0].split("-"))/2 for x in line.split(": ")[-1].split(", "))
        elif line.startswith("Chaos Damage: "):
            c_dmg = line_to_dmg(line)
        elif line.startswith("Attacks per Second: "):
            aps = float(line.split(": ")[-1].split()[0])

    if not p_dmg and not e_dmg and not c_dmg:
        return ""

    p_dps = (p_dmg * aps) if p_dmg else 0
    e_dps = (e_dmg * aps) if e_dmg else 0
    c_dps = (c_dmg * aps) if c_dmg else 0

    dps = p_dps + e_dps + c_dps

    result = "DPS: %.2f\n" % dps
    if p_dmg:
        result += "pDPS: %.2f\n" % p_dps
    if e_dmg:
        result += "eDPS: %.2f\n" % e_dps
    if c_dmg:
        result += "cDPS: %.2f\n" % c_dps

    return result


def line_to_dmg(line):
    return sum(float(x) for x in line.split(": ")[-1].split()[0].split("-")) / 2.0


def load_settings():
    fname = "settings.json"
    if os.path.isfile(fname):
        with open(fname) as f:
            return json.load(f)


def main():
    global settings
    settings = load_settings()

    prev_clip = None
    while True:
        clip = get_clipboard()
        if clip != prev_clip:
            if "\n--------\n" in clip and "\nUnidentified" not in clip:
                split = clip.split("\n")
                name = split[1].split(">")[-1]
                base = split[2]

                divcard = False
                if "Rarity: Divination Card\n" in clip:
                    divcard = True
                    base = "- Divination Card"

                fullname = "%s %s" % (name, base)
                print fullname

                dps_fmt = calc_dps(split)

                prices = ""
                if "Rarity: Unique\n" in clip:
                    prices = format_prices(get_prices(fullname))
                elif divcard:
                    prices = format_prices(get_prices(name))

                body = ""
                if dps_fmt and prices:
                    body = "%s%s\n%s" % (dps_fmt, "="*20, prices)
                elif dps_fmt:
                    body = dps_fmt
                elif prices:
                    body = prices

                if body:
                    notify(fullname, body)
            prev_clip = clip
        time.sleep(0.1)


if __name__ == "__main__":
    main()
