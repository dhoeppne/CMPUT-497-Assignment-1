import os
def tsvPrint(articleInfo, folder):
    articleName = articleInfo["name"][0]
    fileName = os.path.join(folder, articleName + ".tsv")

    with open(fileName, mode="w") as file:
        for relation in articleInfo.keys():
            #ignore name
            if relation != "name":
                # go through list of relations
                for info in articleInfo[relation]:
                    #only write relations with info in them
                    if len(info) != 0:
                        statement = articleName + "\t" + relation + "\t" + info + "\n"
                        file.write(statement)