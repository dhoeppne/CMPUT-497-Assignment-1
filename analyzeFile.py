import re, nltk
from nltk.stem.regexp import RegexpStemmer
# used to easily handle plurals on my keys
st = RegexpStemmer('s$|ies$')

# regex to extract proper nouns of varying length (ie names of individuals)
nameRe = re.compile(r"(\b[A-Z][\s\w'.]+\b)")
# regex to remove ref tags and comments from the wiki file
removeRe = re.compile(r"(?:\<!).*?(?:>)|(?:\<ref\>).*?(?:\</ref\>)")
# regext to remove the | symbol from certain lines, as it was corrupting my data
pipeRe = re.compile(r"(?:\|[\w]+).*?(?:])")


def analyzeFile(fileName):
    bracketStack = []
    # the list of relations to gather facts for
    # for simplicity's sake, screenplay and writer are each listed
    relationList = [
        "is",
        "name",
        "director",
        "producer",
        "music",
        "starring",
        "writer",
        "country",
        "language",
        "studio",
        "screenplay",
        "editing",
        "distributor"
    ]
    fileObject = compileFileObject(relationList)
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
            if len(fileObject["is"]["fact"]) != 0 and len(bracketStack) == 0:
                break

            # could be start of Infobox. Regardless, we need to add to the bracketstack
            if "{{" in line:
                # use count here because regex can't match brackets well
                numBrackets = line.count("{{")
                for i in range(numBrackets):
                    bracketStack.append("{{")

                # if the infobox is there, grab the fact
                if re.search(r"^{{Infobox", line):
                    typeMatch = re.search(r"\w+\s$", line)
                    fileObject["is"]["fact"].append(typeMatch.group().strip())

            # if we're in this range, that means we are in an infobox
            if len(bracketStack) > 0 and len(bracketStack) <= 2:
                # find the key, which is the relation
                keyMatch = re.findall(r"^\|\s*?(\b\w+\b)", line)
                if keyMatch and st.stem(keyMatch[0]) in keys:
                    key = keyMatch[0]

                if keyMatch and key:
                    # check if on single line
                    if re.search(r"ubl|<br />|unbulleted list", line):
                        # find all names
                        matches = re.findall(nameRe, line)
                        for match in matches:
                            if match not in fileObject[key]["fact"]:
                                fileObject[key]["fact"].append(match)
                        # reset key
                        key = ""
                    # check for basic line match with key
                    elif not len(bracketStack) > 1:
                        match = re.search(nameRe, line)
                        if match:
                            fileObject[key]["fact"].append(match.group())
                        # reset key
                        key = ""

                # handle Plainlist - do not reset key in this instance
                elif len(bracketStack) == 2 and key not in keyMatch:
                    match = re.search(nameRe, line)
                    if match and key in keys:
                        fileObject[key]["fact"].append(match.group())

            # could be end of infobox. regardless, we need to pop the bracketstack
            if "}}" in line:
                numBrackets = line.count("}}")

                for i in range(numBrackets):
                    bracketStack.pop()

                if type(key) != None:
                    key = ""

    return fileObject

# creates an object that is used to store facts and evidence
def compileFileObject(relations):
    fileObject = {}
    for relation in relations:
        fileObject[relation] = {
            "fact": [],
            "evidence": []
        }

    return fileObject
