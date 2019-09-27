import re

reInfo = re.compile(r"\b\w+[\s\w]+\b")
typeRe = re.compile(r"\w+\s$")

def analyzeFile(fileName):
    bracketStack = []
    fileObject = {
        "is": [],
        "name": [],
        "director": [],
        "producer": [],
        "music": [],
        "starring": [],
        "writer": [],
        "country": [],
        "language": [],
        "studio": []
    }
    keys = fileObject.keys()
    key = ""

    with open(fileName, "r") as file:
        for line in file:
            if len(fileObject["is"]) != 0 and len(bracketStack) == 0:
                break

            if "{{" in line:
                # use count here because regex can't match brackets well
                numBrackets = line.count("{{")
                for i in range(numBrackets):
                    bracketStack.append("{{")

                if re.search(r"^{{Infobox", line):
                    typeMatch = re.search(typeRe, line)
                    fileObject["is"].append(typeMatch.group().strip())

            if len(bracketStack) > 0 and len(bracketStack) <= 2:
                matches = re.findall(reInfo, line)

                if matches and len(bracketStack) == 2 and len(key) == 0:
                    key = matches[0]

                if len(matches) > 0:
                    if matches[0] in keys and not len(bracketStack) > 1:
                        fileObject[matches[0]].append(matches[1])
                    elif len(bracketStack) == 2 and key not in matches[0]:
                        match = re.search(reInfo, line)
                        if match and key in keys:
                            fileObject[key].append(match.group())

            if "}}" in line:
                numBrackets = line.count("}}")

                for i in range(numBrackets):
                    bracketStack.pop()

                if len(key) > 1:
                    key = ""

    return fileObject