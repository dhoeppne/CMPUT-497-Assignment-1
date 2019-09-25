import re

def analyzeFile(fileName):
    bracketStack = []
    fileObject = {
        "articleType": "",
        "name": "",
        "director": [],
        "producer": [],
        "musicComposer": [],
        "starring": [],
        "writer": [],
        "country": "",
        "language": ""
    }
    keys = fileObject.keys()

    with open(fileName, "r") as file:
        for line in file:
            if len(bracketStack) > 0 and len(bracketStack) <= 2:
                matches = re.findall("[\|\S]\S\w+\S", line)
                if len(matches) > 0:
                    if matches[0] in keys:
                        fileObject[matches[0]] = matches[1]

            if "{{" in line and "}}" not in line:
                bracketStack.append("{{")

                if re.search("Infobox", line):
                    fileObject["articleType"] = re.search("\w+$", line).group()
            elif "}}" in line and "{{" not in line:
                bracketStack.pop()

            if fileObject["articleType"] != "" and len(bracketStack) == 0:
                break

        print(fileObject)