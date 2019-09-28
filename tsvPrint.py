import os
def tsvPrint(articleInfo, folder):
    articleName = articleInfo["name"]["fact"][0]
    fileName = os.path.join(folder, articleName + ".tsv")

    with open(fileName, mode="w") as file:
        for relation in articleInfo.keys():
            #ignore name
            if relation != "name":
                # go through list of relations
                i = 0
                for fact in articleInfo[relation]["fact"]:
                    #grab the evidence for the fact
                    evidence = articleInfo[relation]["evidence"][i]

                    # quick dirty change to match format
                    if relation == "is":
                        relation = "type"

                    #only write relations with info in them
                    if len(fact) != 0:
                        statement = articleName + "\t" + relation + "\t" + fact + "\t" + evidence + "\n"
                        file.write(statement)

                    i += 1