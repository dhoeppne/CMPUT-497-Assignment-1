import os
def tsvPrint(articleInfo, folder):
    articleName = articleInfo["name"]["fact"][0]
    fileName = os.path.join(folder, articleName + ".tsv")

    # create the tsv
    with open(fileName, mode="w") as file:
        for relation in articleInfo.keys():
            #ignore name
            if relation != "name":
                # go through list of relations
                i = 0
                for fact in articleInfo[relation]["fact"]:
                    # grab the evidence for the fact
                    # due to the way the evidence is grabbed and stored in relation to the facts,
                    # I am guaranteed to have the evidence in the same order as the facts
                    # hence, a counter can be used
                    evidence = articleInfo[relation]["evidence"][i]

                    # quick dirty change to match format given in the examples
                    if relation == "is":
                        relation = "type"

                    # only write relations with info in them
                    # this may happen if a relation was not matched in the wiki
                    if len(fact) != 0:
                        statement = articleName + "\t" + relation + "\t" + fact + "\t" + evidence + "\n"
                        file.write(statement)

                    i += 1