
import os
import re
from spell import Spell
from operator import attrgetter

traditions_folder_raw = "traditions\\raw"
traditions_folder_parsed = "traditions\\parsed"
traditions_folder_old = "traditions\\old"
traditions_folder_sorted = "traditions\\sorted"

def list_traditions(type):
    raw_tradition_files = []
    # r=root, d=directories, f = files
    for r, _, f in os.walk(type):
        for file in f:
            if '.txt' in file:
                t = (file, os.path.join(r, file))
                raw_tradition_files.append(t)
    
    return raw_tradition_files

def parse_old_tradition(tradition):
    path = f"{traditions_folder_old}\\{tradition}"
    if os.path.exists(path):
        t = open(path, encoding="utf8").read()
        spells = old_to_spells(t)
        return spells
    return []

def parse_tradition(tradition):
    t = open(tradition[1], encoding="utf8").read()
    clean = remove_junk(t)
    clean = "+++ " + clean
    clean = break_spellname(clean)
    # clean = break_bad_spellname(clean)

    if tradition[0] == "metal.txt":
        print(clean)
    

    spells = raw_to_spells(clean)
    old_spells = parse_old_tradition(tradition[0])

    spells = spells + old_spells
    spells = sorted(spells, key=lambda spell: spell.rank)

    save_tradition(tradition[0], spells_to_file(spells))

def spells_to_file(spells):
    txt = ""
    for spell in spells:
        txt = txt + f"{spell}\n\n"
    return txt
    
def old_to_spells(old):
    old_spells = old.split("\n\n")
    spells = []
    for old_spell in old_spells: 
        spells.append(Spell(parsed=old_spell))
    return spells

def raw_to_spells(raw):
    raw_spells = raw.split("\n\n")
    spells = []
    for raw_spell in raw_spells: 
        spells.append(Spell(raw=raw_spell))
    return spells

def remove_junk(raw):
    raw = remove_pages(raw)
    raw = remove_header(raw)
    raw = remove_doublespaces(raw)
    return raw

def remove_pages(raw):
    return re.sub("\n[0-9]*", "", raw)

def remove_header(raw):
    return re.sub("Traditions and Spells", "", raw)

def remove_doublespaces(raw):
    return re.sub("  ", " ", raw)  

def break_spellname(clean):
    clean = re.sub("[A-Z] [0-9]* ", replace_with_breaks, clean) 
    clean = re.sub("[a-z]\\. *[A-Z]{2}", prefix_line_break, clean)
    return clean

def break_bad_spellname(clean):
    clean = re.sub("\\.[A-ZA-Z]", bad_breaks, clean) 
    return clean

def replace_with_breaks(match):
    match = match.group()
    return match + "\n----\n"

def prefix_line_break(match):
    match = match.group()
    match = re.sub(" ", "", match)
    return match[:2]+"\n\n+++ "+match[2:]

def bad_breaks(match):
    match = match.group()
    return match[:1]+"\n\n+++ "+match[1:]

def save_tradition(name, content):
    file = open(f'{traditions_folder_parsed}/{name}', 'w', encoding="utf8")
    file.write(content)
    file.close()

def main():
    traditions_to_parse = list_traditions(traditions_folder_raw)
    for tradition in traditions_to_parse:
        parse_tradition(tradition)

if __name__ == '__main__':
    main()