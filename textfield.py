import re

# dictionary of key synonyms
synonymsDict = {
    "director": ["director", "directed"],
    "producer": ["producer", "produced"],
    "music": ["music", "composer", "composed"],
    "starring": ["starring", "starred", "as", "cast"],
    "writer": ["writer", "screenplay", "written"],
    "screenplay": ["writer", "screenplay", "written"],
    "editing": ["editing", "editor", "edited"],
    "distributor": ["distribute", "distributor", "distributed"]
}

def textfield(fileName, fileObject):
        # first for loop to check for each relation
        for relation in fileObject.keys():
            matches = fileObject[relation]["fact"]

            # second for loop to check for each fact in a match
            for fact in matches:
                foundEvidence = ""
                # if the file isn't opened here, each file is not checked properly
                # the next for loop would instead start n lines into the file instead of at the zeroth line
                file = open(fileName, "r")

                # now check each line in the file
                for line in file:
                    # if there relations that have synonyms, check each line for each of them
                    if relation in synonymsDict.keys():
                        for syn in synonymsDict[relation]:
                            evidenceMatch = evidenceSearch(syn, fact, line)

                            # if one of the synonyms works, see if its shorter than the old one
                            if evidenceMatch:
                                if len(foundEvidence) == 0 or len(foundEvidence) > len(evidenceMatch.group()):
                                    foundEvidence = evidenceMatch.group()

                    # otherwise, check normally
                    else:
                        evidenceMatch = evidenceSearch(relation, fact, line)

                        if evidenceMatch:
                            # if no found evidence or shorter evidence is found, record it
                            if len(foundEvidence) == 0 or len(foundEvidence) > len(evidenceMatch.group()):
                                foundEvidence = evidenceMatch.group()
                file.close()

                # record fact if found, otherwise search for a basic one
                # if a basic one cannot be found, then declare no evidence found
                if len(foundEvidence) > 0:
                    fileObject[relation]["evidence"].append(foundEvidence)
                else:
                    file = open(fileName, "r")
                    # find a mention of the fact in the text
                    basicEvidence = "no evidence found"
                    for line in file:
                        # search for a * or | starting in a line, then for the fact
                        if re.search(r"(\*|\|)[\s\W]*" + fact, line):
                            basicEvidence = re.search(r"(\*|\|)[\s\W]*" + fact, line).group()

                    fileObject[relation]["evidence"].append(basicEvidence)
                    file.close()

def evidenceSearch(relation, fact, line):
    # look for evidence
    # this checks for either the format of relation then fact, or the format fact than relation
    # ex for the first is <name> is a <film>
    # ex for the second is <actor> as <role>
    factRe = re.compile(r"(.*[\s\W]+\b" + relation + r"\b.*?\b" + fact + r"\b)|(\b" + fact + r"\b.*\b" + relation + r"\b.*$)")
    return re.search(factRe, line)