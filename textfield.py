import re

removeRe = re.compile(r"(?:\<!).*?(?:>)|(?:\<ref\>).*?(?:\</ref\>)")

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
        for relation in fileObject.keys():
            print("\t\tGathering evidence for facts about the relation " + relation)
            matches = fileObject[relation]["fact"]

            for fact in matches:
                foundEvidence = ""
                file = open(fileName, "r")

                for line in file:
                    # if there relations that have synonyms, check for each of them
                    if relation in synonymsDict.keys():
                        for syn in synonymsDict[relation]:
                            evidenceMatch = evidenceSearch(syn, fact, line)

                            # if one of the synonyms works, see if its shorter than the old one
                            if evidenceMatch:
                                if len(foundEvidence) == 0 or len(foundEvidence) > len(evidenceMatch.group()):
                                    foundEvidence = evidenceMatch.group()
                    else:
                        evidenceMatch = evidenceSearch(relation, fact, line)

                        if evidenceMatch:
                            # if no found evidence or shorter evidence is found, record it
                            if len(foundEvidence) == 0 or len(foundEvidence) > len(evidenceMatch.group()):
                                foundEvidence = evidenceMatch.group()
                file.close()

                # record fact if found, otherwise declare no evidence found
                if len(foundEvidence) > 0:
                    fileObject[relation]["evidence"].append(foundEvidence)
                else:
                    file = open(fileName, "r")
                    # find a mention of the fact in the text
                    basicEvidence = "no evidence found"
                    for line in file:
                        if re.search(r"(\*|\|)[\s\W]*" + fact, line):
                            basicEvidence = re.search(r"(\*|\|)[\s\W]*" + fact, line).group()

                    fileObject[relation]["evidence"].append(basicEvidence)
                    file.close()

def evidenceSearch(relation, fact, line):
    # look for evidence
    factRe = re.compile(r"(.*[\s\W]+\b" + relation + r"\b.*?\b" + fact + r"\b)|(\b" + fact + r"\b.*\b" + relation + r"\b.*$)")
    return re.search(factRe, line)