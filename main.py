
import os
import re

traditions_folder_raw = "raw_traditions"
traditions_folder_parsed = "parsed_traditions"
keywords = ["Target", "Duration", "Area", "Requirement", "Attack Roll 20\\+", "Sacrifice", "Aftereffect"]

def list_traditions():
    raw_tradition_files = []
    # r=root, d=directories, f = files
    for r, _, f in os.walk(traditions_folder_raw):
        for file in f:
            if '.txt' in file:
                t = (file, os.path.join(r, file))
                raw_tradition_files.append(t)
    
    return raw_tradition_files

def parse_tradition(tradition):
    t = open(tradition[1]).read()
    clean = remove_junk(t)
    clean = "+++ " + clean
    clean = break_spellname(clean)
    clean = break_spelltype(clean)
    clean = break_spelldescription(clean)
    clean = break_keyword(clean)
    clean = bolden(clean)
    clean = clear_property_exceptions(clean)

    save_tradition(tradition[0], clean)

def clear_property_exceptions(clean):
    return re.sub("(Area|Target|Duration)\\s*([^\n\r]*)", format_clear_exception, clean) 

def bolden(clean):
    for keyword in keywords:
        clean = re.sub(f"\n{keyword}", format_bold, clean)
    return clean

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

def break_spelltype(clean):
    return re.sub("[A-Z]* (UTILITY|ATTACK) [0-9]*", format_spelltype, clean)

def break_spelldescription(clean):
    return re.sub("[a-z][A-Z]", format_spelldescription, clean)

def break_keyword(clean):
    for keyword in keywords:
        clean = re.sub(f" {keyword}", break_before, clean)
    return clean

def replace_with_breaks(match):
    match = match.group()
    return match + "\n----\n"

def prefix_line_break(match):
    match = match.group()
    match = re.sub(" ", "", match)
    return match[:2]+"\n\n+++ "+match[2:]

def format_spelltype(match):
    match = match.group()
    return "\n//" + match + "//"

def format_spelldescription(match):
    match = match.group()
    return match[:1] + "\n----\n" + match[1:]

def format_bold(match):
    match = match.group()
    return match[:1]+"**"+match[1:]+"**"

def format_clear_exception(match):
    match = match.group()
    match = re.sub("[a-z] (?!Size)[A-Z][^\"]*", format_inception, match)
    return match

def format_inception(match):
    match = match.group()
    return match[:1]+"\n"+match[2:]

def break_before(match):
    match = match.group()
    return "\n" + match[1:]

def save_tradition(name, content):
    file = open(f'{traditions_folder_parsed}/{name}', 'w')
    file.write(content)
    file.close()

def main():
    traditions = list_traditions()
    for tradition in traditions:
        parse_tradition(tradition)

if __name__ == '__main__':
    main()