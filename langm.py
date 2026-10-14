import json
from ipa import convert
from collections import Counter

noARG = ["save", "exit", "info"]

def load(path="lexicon.json"):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError: # file doesn't exist
        return []
    except PermissionError: # file exists but cannot be opened
        return []
entries = load()
def reset():
    entry["word"] = ""
    entry["ipa"] = ""
    entry["pos"] = ""
    entry["means"] = []
    entry["meta"] = []

def validate(d):
    if not d["word"]: return "Missing Word"
    if not d["ipa"]:  return "Missing IPA"
    if not d["means"]:return "Missing Meaning"
    if not d["meta"]: return "Missing meta"
    if not d["pos"]: return "Missing POS"
    return None
def save(entry, path="lexicon.json"):
    err = validate(entry) 
    if err is not None: 
        print("error: ", err)
        return
    entries.append(entry.copy())
    with open(path, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    print(f"Saved {entry['word']}")
    reset()
# current = None
entry = {
    "word": "",
    "pos": "",
    "ipa": "",
    "means": [],
    "meta": []
}
def info(d):
    amount = 0
    x = 0
    blanks = []
    
    if not d["word"]:
        blanks.append("word")
        amount += 1
    if not d["means"]:
        blanks.append("meaning")
        amount += 1
    if not d["meta"]:
        blanks.append("meta")
        amount += 1
    if not d["pos"]:
        blanks.append("POS")
        amount += 1
    if not d["ipa"]:
        blanks.append("IPA")
        amount += 1
    # try to DRY up this block.
    # I would do it myself but I have no idea what's going on here and don't want to break anything.
    # The goal is to have one `amount += 1`
    
    print(f"Missing fields: {amount} ")
    for missing in blanks:
        print(f"\t{missing} (Reqired)") 

def phoncount(ipa):
    toks = tokenize(ipa)

def poscount(entries):
    c = Counter(e.get("pos") for e in entries)
    for pos, n in c.most_common():
        print(f"{n:>5}  {pos}")

while True:
    x = input("LangM> ").split(" ", 1)
    if len(x) == 1 and x[0] == "exit": 
        break
    elif len(x) == 1 and x[0] not in noARG:
        print("Expected an argument, got none.")
        continue
    cmd = x[0]
    arg = x[1] if len(x) > 1 else ""

    match cmd:
        case "new": 
            reset()
            entry["word"] = arg
        case "pos":
            entry["pos"] = arg
        case "ipa": 
            entry["ipa"] = f"{convert(arg)}"
        case "meaning":
            arg = arg.split(";")
            for m in arg:
                entry["means"].append(m)
        case "meta":  
            arg = arg.split(";")
            if arg == '-' or arg == ['null', 'null']:
                entry["meta"] = [None, None]
            for m in arg:
                entry["meta"].append(m)
            if len(arg) > 2:
                print(f"Error: expected 2 arguments, got {len(arg)}.")
                entry["meta"] = [None, None]
        case "save":
            save(entry)
        case "info":
            info(entry)
        case "saveas":
            save(entry, arg)
        case "count":
            file = None
            try:
                with open(arg) as f:
                    file = json.load(f)
            except FileNotFoundError:
                print(f"Error: Couldn't find file {arg}. Are you sure it exists in this context?")
                continue
            if file is None:
                print("Something went wrong and data couldn't be fetched.")
                continue
            print(len(file))
        case "poscount":
            file = None
            try:
                with open(arg) as f:
                    file = json.load(f)
            except FileNotFoundError:
                print(f"Error: Couldn't find file {arg}")
                continue
            if file is None:
                print("Something went wrong and data couldn't be fetched.")
                continue
            poscount(file)
        case "help":
            # fill this out yourself. I don't know what this program is
            print("Commands: new, pos, ipa, meaning, meta, saves, info, saveas, count, poscount.")
        case _: # unrecognized command
            print(f"{cmd} isn't a recognized command.")
            continue # I don't think this command is necessary but I don't want to fuck around and find out
