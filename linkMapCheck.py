import os
import enum 

#分析可执行文件增量大小

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
linkmapPath = "/Users/xxx/Documents/sizetj/7.9/LinkMap-normal-arm64.txt"
compareLinkmapPath = "/Users/xxx/Documents/sizetj/7.8/LinkMap.txt"

class TagType(enum.IntEnum):
    Add = 4
    Up = 3
    Down = 2
    Del = 1
    Other = 0
    

class SymbolModel:
    file = ""
    size = 0
    path = ""
    tagType = TagType.Other


def getFileName(path):
    pathSplit = path.split("/")
    name = pathSplit[-1] if len(pathSplit) > 0 else ""
    index = name.find("(",0,len(name))
    if index != -1 :
        name = name[index+1:len(name)-1]
    return name
        

def getLinkmapSymbolsMap(linkpath):
    reachFiles = False
    reachSymbols = False
    reachSections = False
    symbolMap = {}
    linkfile = open(linkpath, 'r',encoding="macroman") 
    for line in linkfile.readlines():
        if line.startswith("#",0,len(line)):
            if "# Object files:" in line:
                reachFiles = True
            elif "# Sections:" in line:
                reachSections = True
            elif "# Symbols:" in line:
                reachSymbols = True
        else:
            if reachFiles == True and reachSections == False and reachSymbols == False :
                line = line.replace("\n","")
                index = line.find("]",0,len(line))
                if index != -1 :
                    ofilePath = line[index+2:]
                    oIndex = line[:index+1]
                    symobl = SymbolModel()
                    symobl.path = ofilePath
                    symobl.file = getFileName(ofilePath)
                    symbolMap[oIndex] = symobl
            elif reachFiles == True and reachSections == True and reachSymbols == True :
                    symbolsArray = line.split("\t")
                    if len(symbolsArray) == 3 :
                        fileKeyAndName = symbolsArray[2]
                        symbolSize = int(symbolsArray[1],16)

                        fileKeyAndName = fileKeyAndName.replace("\n","")
                        index = fileKeyAndName.find("]",0,len(line))
                        if index != -1 :
                            oIndex = fileKeyAndName[:index+1]
                            symobl = symbolMap[oIndex]
                            symobl.size += symbolSize
    linkfile.close()
    return symbolMap


def paserSizeToStr(size) :
    if  abs(size / 1024.0) > 1024.0:
        return "{:.2f}M".format(size / 1024.0 / 1024.0) 
    else:
        return "{:.2f}K".format(size / 1024.0) 


def getTagToStr(type):
    tag = ""
    if type == TagType.Up :
       tag = "↑"
    elif type == TagType.Down :
        tag = "↓"
    elif type == TagType.Add:
        tag = "+"
    elif type == TagType.Del:
        tag = "-"
    return tag

def getTag(size,comSize):
    tag = TagType.Other
    if size > comSize :
        tag = TagType.Up
    elif size < comSize :
        tag = TagType.Down
    return tag

def getSymbolSizeMap(symbols):
    symbolSizeMap = {}
    totalSize = 0
    for symbol in symbols :
        symbolSizeMap[symbol.file] = symbol.size
        totalSize += symbol.size
    return (symbolSizeMap,totalSize)
    


comSymbolMap = getLinkmapSymbolsMap(compareLinkmapPath)
comSymbols = list(comSymbolMap.values())
comSymbolSizeMap,cmpTotalSize = getSymbolSizeMap(comSymbols)

symbolMap = getLinkmapSymbolsMap(linkmapPath)
symbols =  list(symbolMap.values()) 
symbolSizeMap,totalSize = getSymbolSizeMap(symbols)

for symbol in symbols :
    tag = TagType.Other
    thanNum = 0
    name = symbol.file
    if comSymbolSizeMap.__contains__(name):
        comSize = comSymbolSizeMap[name]
        tag = getTag(symbol.size,comSize)
        thanNum = symbol.size - comSize
    else:
        tag = TagType.Add
        thanNum = symbol.size
    symbol.thanNum = thanNum
    symbol.tagType = tag

#加入被删除的
for symbol in comSymbols:
    name = symbol.file
    if not symbolSizeMap.__contains__(name):
        symbol.thanNum = -symbol.size
        symbol.tagType = TagType.Del
        symbols.append(symbol)

symbols.sort(key = lambda symbol: (symbol.tagType,symbol.thanNum),reverse = True)

result = "文件名称\t文件大小\t增量K\t标识\t路径\n"
for symbol in symbols :
    result += "{}\t{}\t{:.2f}\t{}\t{}\n".format(symbol.file,paserSizeToStr(symbol.size),symbol.thanNum/1024.0,getTagToStr(symbol.tagType),symbol.path)
result += "\n总大小:{}\t增量:{}\n".format(paserSizeToStr(totalSize),paserSizeToStr(totalSize-cmpTotalSize))

outputFilePath = os.path.join(outPath,"linkMapSize.txt") 
output = open(outputFilePath, 'w') 
output.write(result)   
output.close()

print("linkmap统计完成")
