import yaml
# - - - Get DataBases - Init - - -
with open('rec\\sde\\fsd\\blueprints.yaml', "r") as stream:
    try:
        _BPData = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()
with open('rec\\sde\\fsd\\typeIDs.yaml', "r" , encoding="utf8") as stream:
    try:
        _NameData = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)
        exit()

def main(): 
    # Raven - 688
    # Cormorant - 16239
    #readBlueprint(16239, 1)
    BPID, MANTYPE = getBluePrintID(638)
    readBlueprint(BPID, MANTYPE)
# - - -

def getBluePrintID(ItemID):
    for x in _BPData:
        if "manufacturing" in _BPData[x]["activities"]:
            if "products" in _BPData[x]["activities"]["manufacturing"]:
                if _BPData[x]["activities"]["manufacturing"]["products"][0]["typeID"] == ItemID:
                    #print(str(ItemID) + " is an Manufactured Item and has the BP ID: " + str(x))
                    return x, 1

        if "reaction" in _BPData[x]["activities"]:
            if _BPData[x]["activities"]["reaction"]["products"][0]['typeID'] == ItemID:
                if _BPData[x]["activities"]["reaction"]["products"][0]["typeID"] == ItemID:
                    #print(str(ItemID) + " is an Reaction Item and has the BP ID: " + str(x))
                    return x, 2

    #print("Didnt find BP")
    return 0, 0 # error, didnt find anything!

getBluePrintID(57478)  

def readBlueprint(ID, mantype):  
    print(_NameData[ID]["name"]["en"] + "\n")
    
    if(mantype == 1):
        for x in _BPData[ID]["activities"]["manufacturing"]["materials"]:
            _BPId, _mantype = getBluePrintID(x["typeID"])      
            if(_BPId == 0):
                print(str(_NameData[x["typeID"]]["name"]["en"]) + ": " + str(x["quantity"]) )#+ " -ID davon: " + str(x["typeID"]))
                continue
            print(str(_NameData[x["typeID"]]["name"]["en"]) + ": " + str(x["quantity"]) )
            readBlueprint(_BPId, _mantype)
    if(mantype == 2):
        for x in _BPData[ID]["activities"]["reaction"]["materials"]:
            _BPId, _mantype = getBluePrintID(x["typeID"])        
            if(_BPId == 0):
                print(str(_NameData[x["typeID"]]["name"]["en"]) + ": " + str(x["quantity"]) )#+ " -ID davon: " + str(x["typeID"]))
                #print(getBluePrintID(x))
                continue
            print(str(_NameData[x["typeID"]]["name"]["en"]) + ": " + str(x["quantity"]) )
            readBlueprint(_BPId, _mantype)
    if(mantype == 0): 
        print("Didnt find production type of " + str(ID) + " as the detected prod. type is: " + str(mantype))
    return

if __name__ == "__main__":
    main()

def getBPArr(bluePrintID):
    BPList = []
    if(getBluePrintID(bluePrintID) != (0,0)):
        theBPInstead, mantype = getBluePrintID(bluePrintID)
        BPList.append(theBPInstead)
    else:        
        BPList.append(bluePrintID)
    if(len(BPList)==0):
        return None
#now we have a Blueprint in the array at pos 0 (this is the to be produced bp)
#everything else is a bp that is needed for the componence or the componence of the componence...
    for key, values in _BPData[BPList[0]].items():
        if("activities" == key):    
            if("manufacturing" in values):
                for x in values["manufacturing"]["materials"]:
                    if(getBluePrintID(x["typeID"]) == (0, 0)):
                        continue
                    BPList.append(x["typeID"])
            if("reaction" in values):
                for x in values["reaction"]["materials"]:
                    if(getBluePrintID(x["typeID"]) == (0, 0)):
                        continue
                    BPList.append(x["typeID"])
#now we have the blueprints the item consists of...
    for x in BPList:
        if(x == BPList[0]):
            #print("Found myself!")
            continue
        #print(x)
        arr = getBPArr(x)
        for y in arr:
            if y in BPList:
                continue
            BPList.append(y)
    return BPList

BPID, MANTYPE = getBluePrintID(638) #57478 | 638
getBPArr(BPID)