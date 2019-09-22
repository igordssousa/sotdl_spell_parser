import re

keywords = ["Target", "Duration", "Area", "Requirement", "Attack Roll 20\\+", "Sacrifice", "Aftereffect", "Triggered"]


class Spell():
    "A Demonlord Spell"

    def __init__(self, raw=None, parsed=None):
        if parsed is not None:
            self.parsed = parsed
            return
        self.raw = raw
        t = break_spelltype(raw)
        t = break_spelldescription(t)
        t = break_keyword(t)
        t = bolden(t)
        t = clear_property_exceptions(t)
        t = missing_seperator(t)
        self.parsed = t

    def __str__(self):
        return self.parsed

    @property
    def name(self):
        return self.parsed.split("\n")[0][4:]

    @property
    def rank(self):
        # print(self.parsed.split("\n"))
        m = re.search("(UTILITY|ATTACK)", self.parsed.split("\n")[1])
        if m is None:
            return 0
        # print(self.parsed.split("\n")[1])
        return int(re.search("[0-9]+", self.parsed.split("\n")[1]).group(), 10)


# Helper functions
def missing_seperator(t):
    return re.sub("[a-z]\n[A-Z]", fmt_horizontal_line, t)


def clear_property_exceptions(t):
    return re.sub("(Area|Target|Duration)\\s*([^\n\r]*)", fmt_clear_exception, t)


def bolden(t):
    for keyword in keywords:
        t = re.sub(f"\n{keyword}", fmt_bold, t)
    return t


def break_spelltype(t):
    return re.sub("[A-Z]* (UTILITY|ATTACK)\\s\\d[0-9]*", fmt_spelltype, t)


def break_spelldescription(t):
    return re.sub("[a-z][A-Z]", fmt_spelldescription, t)


def break_keyword(t):
    for keyword in keywords:
        t = re.sub(f" {keyword}", break_before, t)
    return t


def fmt_spelltype(match):
    match = match.group()
    return "(OP)\n//" + match + "//"


def fmt_spelldescription(match):
    match = match.group()
    return match[:1] + "\n----\n" + match[1:]


def fmt_bold(match):
    match = match.group()
    return match[:1]+"**"+match[1:]+"**"


def fmt_clear_exception(match):
    match = match.group()
    match = re.sub("[a-z] (?!Size)[A-Z][^\"]*", fmt_inception, match)
    return match


def fmt_horizontal_line(match):
    match = match.group()
    return match[:2]+"----\n"+match[2:]


def fmt_inception(match):
    match = match.group()
    return match[:1]+"\n"+match[2:]


def break_before(match):
    match = match.group()
    return "\n" + match[1:]
