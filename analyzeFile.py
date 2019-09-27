import re, nltk
from nltk.stem.regexp import RegexpStemmer
# used to easily handle plurals on my keys
st = RegexpStemmer('s$|ies$')

nameRe = re.compile(r"(\b[A-Z][\s\w'.]+\b)")
removeRe = re.compile(r"(?:\<!).*?(?:>)|(?:\<ref\>).*?(?:\</ref\>)")
pipeRe = re.compile(r"(?:\|[\w]+).*?(?:])")


def analyzeFile(fileName):
    bracketStack = []
    fileObject = {
        "type": [],
        "name": [],
        "director": [],
        "producer": [],
        "music": [],
        "starring": [],
        "writer": [],
        "country": [],
        "language": [],
        "studio": [],
        "screenplay": [],
        "editing": [],
        "distributor": []
    }
    keys = fileObject.keys()
    key = ""

    with open(fileName, "r") as file:
        for line in file:
            # remove problems from line if it exists
            if re.search(removeRe, line):
                line = re.sub(removeRe, "", line)
            # remove weird double piping issue
            if re.search(pipeRe, line) and "<br />" in line:
                line = re.sub(pipeRe, "]", line)
            # check if Infobox has been exited
            if len(fileObject["type"]) != 0 and len(bracketStack) == 0:
                break

            if "{{" in line:
                # use count here because regex can't match brackets well
                numBrackets = line.count("{{")
                for i in range(numBrackets):
                    bracketStack.append("{{")

                if re.search(r"^{{Infobox", line):
                    typeMatch = re.search(r"\w+\s$", line)
                    fileObject["type"].append(typeMatch.group().strip())

            if len(bracketStack) > 0 and len(bracketStack) <= 2:
                keyMatch = re.findall(r"^\|\s*?(\b\w+\b)", line)
                if keyMatch and st.stem(keyMatch[0]) in keys:
                    key = keyMatch[0]

                if keyMatch and key:
                    # check if on single line
                    if re.search(r"ubl|<br />|unbulleted list", line):
                        # find all names
                        matches = re.findall(nameRe, line)
                        for match in matches:
                            if match not in fileObject[key]:
                                fileObject[key].append(match)
                        # reset key
                        key = ""
                    # check for basic line match with key
                    elif not len(bracketStack) > 1:
                        match = re.search(nameRe, line)
                        if match:
                            fileObject[key].append(match.group())
                        # reset key
                        key = ""

                # handle Plainlist - do not reset key in this instance
                elif len(bracketStack) == 2 and key not in keyMatch:
                    match = re.search(nameRe, line)
                    if match and key in keys:
                        fileObject[key].append(match.group())

            if "}}" in line:
                numBrackets = line.count("}}")

                for i in range(numBrackets):
                    bracketStack.pop()

                if type(key) != None:
                    key = ""

    return fileObject

