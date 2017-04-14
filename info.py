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

map_string = "Travel to this Map by using it in the Eternal Laboratory or a personal Map Device. Maps can only be used once."

maps = {
    'Abyss Map': 'Maze of the Minotaur Map',
    'Academy Map': 'Spider Lair Map',
    'Acid Lakes Map': 'Mesa Map',
    'Arachnid Nest Map': 'Overgrown Shrine Map',
    'Arachnid Tomb Map': 'Tropical Island Map',
    'Arcade Map': 'Ghetto Map',
    'Arena Map': 'Orchard Map',
    'Arid Lake Map': 'Dungeon Map',
    'Armoury Map': 'Atoll Map',
    'Arsenal Map': 'Chateau Map',
    'Ashen Wood Map': 'Arachnid Nest Map',
    'Atoll Map': 'Temple Map',
    'Barrows Map': 'Promenade Map',
    'Bazaar Map': 'Shipyard Map',
    'Beach Map': 'Vaal Pyramid Map',
    'Beacon Map': 'Volcano Map',
    'Bog Map': 'Crypt Map',
    'Burial Chambers Map': 'Vaal City Map',
    'Canyon Map': 'Catacombs Map',
    'Castle Ruins Map': 'Cemetery Map',
    'Catacombs Map': 'Shore Map',
    'Cavern Map': 'Waste Pool Map',
    'Cells Map': 'Arachnid Nest Map',
    'Cemetery Map': 'Crypt Map',
    'Channel Map': 'Acid Lakes Map',
    'Chateau Map': 'Estuary Map',
    'Colonnade Map': 'Bazaar Map',
    'Colosseum Map': 'Pit of the Chimera Map',
    'Core Map': 'Forge of the Phoenix Map',
    'Courtyard Map': 'Wasteland Map',
    'Coves Map': 'Quay Map',
    'Crematorium Map': 'Sulphur Wastes Map',
    'Crypt Map': 'Arsenal Map',
    'Crystal Ore Map': 'Factory Map',
    'Dark Forest Map': 'Overgrown Ruin Map',
    'Desert Map': 'Oasis Map',
    'Dunes Map': 'Strand Map',
    'Dungeon Map': 'Dunes Map',
    'Estuary Map': 'Beacon Map',
    'Excavation Map': 'Necropolis Map',
    'Factory Map': 'Channel Map',
    'Ghetto Map': 'Sewer Map',
    'Gorge Map': 'Shrine Map',
    'Graveyard Map': 'Tower Map',
    'Grotto Map': 'Villa Map',
    'High Gardens Map': 'Palace Map',
    'Ivory Temple Map': 'Plaza Map',
    'Jungle Valley Map': 'Beach Map',
    'Lair Map': 'Mineral Pools Map',
    'Malformation Map': 'Excavation Map',
    'Marshes Map': 'Vaal Pyramid Map',
    'Maze Map': 'Colosseum Map',
    'Mesa Map': 'Quarry Map',
    'Mineral Pools Map': 'Abyss Map',
    'Mud Geyser Map': 'Pier Map',
    'Museum Map': 'Courtyard Map',
    'Necropolis Map': 'Lair Map',
    'Oasis Map': 'Arid Lake Map',
    'Orchard Map': 'Temple Map',
    'Overgrown Ruin Map': 'Lair of the Hydra Map',
    'Overgrown Shrine Map': 'Terrace Map',
    'Palace Map': 'Dark Forest Map',
    'Peninsula Map': 'Wharf Map',
    'Phantasmagoria Map': 'Burial Chambers Map',
    'Pier Map': 'Atoll Map',
    'Pit Map': 'Racecourse Map',
    'Plateau Map': 'Scriptorium Map',
    'Plaza Map': 'Maze Map',
    'Precinct Map': 'Ivory Temple Map',
    'Primordial Pool Map': 'Canyon Map',
    'Promenade Map': 'Colonnade Map',
    'Quarry Map': 'Ashen Wood Map',
    'Quay Map': 'Precinct Map',
    'Racecourse Map': 'Cells Map',
    'Ramparts Map': 'Mud Geyser Map',
    'Reef Map': 'Underground River Map',
    'Residence Map': 'Plateau Map',
    'Scriptorium Map': 'Maze Map',
    'Sewer Map': 'Graveyard Map',
    'Shipyard Map': 'Waterways Map',
    'Shore Map': 'Coves Map',
    'Shrine Map': 'Abyss Map',
    'Spider Forest Map': 'Armoury Map',
    'Spider Lair Map': 'Spider Forest Map',
    'Springs Map': 'Overgrown Ruin Map',
    'Strand Map': 'Castle Ruins Map',
    'Sulphur Wastes Map': 'Volcano Map',
    'Temple Map': 'Malformation Map',
    'Terrace Map': 'Bazaar Map',
    'Thicket Map': 'Mud Geyser Map',
    'Torture Chamber Map': 'Residence Map',
    'Tower Map': 'Spider Forest Map',
    'Tropical Island Map': 'Reef Map',
    'Underground River Map': 'Underground Sea Map',
    'Underground Sea Map': 'Vault Map',
    'Vaal City Map': 'Catacombs Map',
    'Vaal Pyramid Map': 'Phantasmagoria Map',
    'Vault Map': 'Gorge Map',
    'Villa Map': 'Peninsula Map',
    'Volcano Map': 'Core Map',
    'Waste Pool Map': 'Mesa Map',
    'Wasteland Map': 'Crematorium Map',
    'Waterways Map': 'Springs Map',
    'Wharf Map': 'Castle Ruins Map'
}


reverse_maps = {}
for m in maps:
    reverse_maps[m] = []
    reverse_maps[maps[m]] = []
for m in maps:
    reverse_maps[maps[m]].append(m)


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


def map_info(split, name, base):
    result = ""

    if base in maps:
        result += "Makes: " + maps[base]
    else:
        result += "Makes: ???"

    result += "\n"

    result += "Made by: "
    if base in reverse_maps:
        mfg = reverse_maps[base]
        if len(mfg) == 0:
            result += "none"
        elif len(mfg) == 1:
            result += mfg[0]
        else:
            result += ", ".join(mfg)
    else:
        result += "???"

    return result


def map_name_base(x):
    options = (
        x,
        " ".join(x.split()[1:]),
        " ".join(x.split()[:-2]),
        " ".join(x.split()[1:-2])
    )

    for m in maps:
        if m in options:
            base = m
            #name = x.replace(m, "*")
            name = base
            return (name, base)
    return (name, "???")


def load_settings():
    fname = "settings.json"
    if os.path.isfile(fname):
        with open(fname) as f:
            return json.load(f)


def unique(clip):
    return "Rarity: Unique\n" in clip

def rare(clip):
    return "Rarity: Rare\n" in clip

def magic(clip):
    return "Rarity: Magic\n" in clip

def normal(clip):
    return "Rarity: Normal\n" in clip

def unidentified(clip):
    return "\nUnidentified" in clip


def main():
    global settings
    settings = load_settings()

    prev_clip = None
    while True:
        clip = get_clipboard()
        if clip != prev_clip:
            if ("\n--------\n" in clip) and (not unidentified(clip) or (map_string in clip)):
                split = clip.split("\n")
                name = split[1].split(">")[-1]
                base = split[2]

                if (not unique(clip) and not rare(clip)) or (rare(clip) and unidentified(clip)):
                    base = name

                divcard = False
                if "Rarity: Divination Card\n" in clip:
                    divcard = True
                    base = "- Divination Card"

                map_item = False
                if map_string in clip:
                    map_item = True
                    base = base.replace("Superior ", "")
                    name = name.replace("Superior ", "")
                    if magic(clip) and not unidentified(clip):
                        name, base = map_name_base(name)

                if name == base:
                    fullname = name
                else:
                    fullname = "%s %s" % (name, base)
                print fullname

                dps_fmt = calc_dps(split)

                prices = ""
                if unique(clip):
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
                elif map_item:
                    body = map_info(split, name, base)

                if body:
                    notify(fullname, body)
            prev_clip = clip
        time.sleep(0.1)


if __name__ == "__main__":
    main()
