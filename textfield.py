def textfield(fileName, fileObject):
    with open(fileName, "r") as file:
        for key in fileObject.keys():
            for line in file:
                pass