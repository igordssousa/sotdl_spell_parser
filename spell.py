import re

keywords = ["Target", "Duration", "Area", "Requirement", "Attack Roll 20\\+", "Sacrifice", "Aftereffect"]

class Spell():
    "A Demonlord Spell"
    def __init__(self, raw):
        self.raw = raw
        clean = break_spelltype(raw)
        clean = break_spelldescription(clean)
        clean = break_keyword(clean)
        clean = bolden(clean)
        clean = clear_property_exceptions(clean)
        clean = missing_seperator(clean)
        self.parsed = clean
    def __lt__(self, other):
        pass #order using self.name and self.rank
    def __str__(self):
        return self.parsed
    @property    
    def  name(self):
        return self.parsed.split("\n")[0][4:]
    @property
    def rank(self):
        m = re.search("(UTILITY|ATTACK)", self.parsed.split("\n")[1]) 
        if m is None:
            return ""
        return re.search("[0-9]+", self.parsed.split("\n")[1]).group()

# Helper functions
def missing_seperator(clean):
    return re.sub("[a-z]\n[A-Z]", format_horizontal_line, clean)

def clear_property_exceptions(clean):
    return re.sub("(Area|Target|Duration)\\s*([^\n\r]*)", format_clear_exception, clean) 

def bolden(clean):
    for keyword in keywords:
        clean = re.sub(f"\n{keyword}", format_bold, clean)
    return clean

def break_spelltype(clean):
    return re.sub("[A-Z]* (UTILITY|ATTACK) [0-9]*", format_spelltype, clean)

def break_spelldescription(clean):
    return re.sub("[a-z][A-Z]", format_spelldescription, clean)

def break_keyword(clean):
    for keyword in keywords:
        clean = re.sub(f" {keyword}", break_before, clean)
    return clean

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

def format_horizontal_line(match):
    match = match.group()
    return match[:2]+"----\n"+match[2:]

def format_inception(match):
    match = match.group()
    return match[:1]+"\n"+match[2:]

def break_before(match):
    match = match.group()
    return "\n" + match[1:]