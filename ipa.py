
MAP = {
    "S": "ʃ",
    "T": "θ",
    "R": "ɾ",
    "q": "ʁ",
    "D": "ð",
    "'": "ˈ",
    ":": "ː",
    "B": "β"
}

PASS = set("abcdefgiklmnopqrstuvw.")


def get(file):
    data = None
    try: 
        with open(file) as f:
            data = f.readlines()
    except FileNotFoundError:
        print(f"Error: File {file} could not be found in this context.")
        return
    except PermissionError:
        print("Error: Something unexpected happened and we couldn't retrieve the data from your file...")
        return
    i = 0
    result = {}
    for line in data:
        i += 1
        line = line.strip()
        stuff = line.split(" ", 1)
        if len(stuff) != 2:
            print(f"Error: Expected 2 arguments on line {i}, got {len(stuff)}")
        char = stuff[0]
        map  = stuff[1]
        if char not in result:
            result[char] = map
    return result


def convert(s):
    out = []
    for ch in s:
        if ch in MAP:
            out.append(MAP[ch])
        elif ch in PASS:
            out.append(ch)
        else:
            print(f"Unrecognized character {ch!r}")
            out.append(ch)
    return "".join(out)


def tokenize(ipa, skips="ˈ.ˌ"):
    inventory = ['a', "aː", "e","eː", "i", "iː","o","oː", "u","uː","b", "d", "f", "ɡ", "j", "k", "l", "m", "n", "p", "r", "ʁ", "s", "t", "θ", 'tʃ', 'v','w', 'x']
    # Longest-match-first so tʃ beats t, aː beats a.
    tokens = []
    i = 0
    while i < len(ipa):
        if ipa[i] in skips:
            i += 1
            continue
        for ph in inventory:          # inventory sorted by len desc
            if ipa.startswith(ph, i):
                tokens.append(ph)
                i += len(ph)
                break
        else:
            tokens.append(ipa[i])     # unknown symbol, keep it visible
            i += 1
    return tokens

