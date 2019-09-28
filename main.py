import re
from pathlib import Path
from spell import Spell

traditions_folder = Path("traditions")  # TODO: Pass as argument.
traditions_folder_raw = traditions_folder / "raw"
traditions_folder_parsed = traditions_folder / "parsed"
traditions_folder_old = traditions_folder / "old"
traditions_folder_sorted = traditions_folder / "sorted"
SPELL_SEPARATOR = "\n\n"

def list_traditions(traditions_path):
    raw_paths = []
    for f in traditions_path.iterdir():
        if f.is_file() and f.suffix == ".txt":
            raw_paths.append(f)
    return raw_paths


def parse_old_tradition(tradition_path):
    if tradition_path.exists() and tradition_path.is_file():
        return convert_to_spells(tradition_path.read_text(encoding="utf8"))
    return []


def parse_tradition(tradition):
    t = tradition.read_text(encoding="utf8")
    t = remove_junk(t)
    t = "+++ " + t
    t = break_spellname(t)
    t = break_bad_spellname(t)

    spells = convert_to_spells(t, raw=True) + parse_old_tradition(traditions_folder_old / tradition.name)
    spells = sorted(spells, key=lambda spell: spell.rank)

    save_tradition(tradition.name, spells_to_file(spells))


def spells_to_file(spells):
    return SPELL_SEPARATOR.join(map(str, spells))


def convert_to_spells(spell_data, raw=False):
    return [
        Spell(raw=s) if raw else Spell(parsed=s)
        for s in spell_data.split(SPELL_SEPARATOR)
    ]


def remove_junk(raw):
    raw = remove_pages(raw)
    raw = remove_header(raw)
    return remove_doublespaces(raw)


def remove_pages(raw):
    return re.sub("\n[0-9]*", "", raw)


def remove_header(raw):
    return re.sub("Traditions and Spells", "", raw)


def remove_doublespaces(raw):
    return re.sub("  ", " ", raw)


def break_spellname(t):
    t = re.sub("[A-Z] [0-9]* ", replace_with_breaks, t)
    return re.sub("[a-z]\\. *[A-Z]{2}", prefix_line_break, t)


def break_bad_spellname(t):
    return re.sub("(\\. |\\.)[A-Z][A-Z]", bad_breaks, t)


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
    (traditions_folder_parsed / name).write_text(content, encoding="utf8")


def main():
    traditions_to_parse = list_traditions(traditions_folder_raw)
    for tradition in traditions_to_parse:
        parse_tradition(tradition)


if __name__ == '__main__':
    main()
    