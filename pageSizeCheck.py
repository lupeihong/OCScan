import os
import enum 

#分析安装包大小

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
appPath = "/Users/xxx/Documents/sizetj/7.9/Mobile.app"
cmpPath = "/Users/xxx/Documents/sizetj/7.8/Mobile.app"

# TagType = Enum('TagType', ('up', 'down', 'add','other'))
class TagType(enum.IntEnum):
    Add = 4
    Up = 3
    Down = 2
    Del = 1
    Other = 0


class FileModel :
    file = ""
    size = 0
    path = ""
    tagType = TagType.Other

def isInWhitelist(path,flist):
    for f in flist:
        if f in path:
            return True
    return False

def getNameFromPath(filePath):
    pathSplit = filePath.split("/")
    name = pathSplit[-1] if len(pathSplit)>0 else "unkown" 
    if len(pathSplit) > 1 and (".bundle" in filePath or ".storyboardc" in filePath):
        name = "({}){}".format(pathSplit[-2],name)
    return name

def paserSizeToStr(size) :
    if  abs(size / 1024.0) > 1024.0:
        return "{:.2f}M".format(size / 1024.0 / 1024.0) 
    else:
        return "{:.2f}K".format(size / 1024.0) 

def getdirsize(dir):  
    size = 0
    for root, dirs, files in os.walk(dir):
        for file in files :
            size += os.path.getsize(os.path.join(root, file)) 
    return size  

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
        

def getModelList(appPath):
    frameworkList = []
    modelList = []
    for root, dirs, files in os.walk(appPath):
        for path in dirs:
            if path.endswith(".framework") or path.endswith(".storyboardc") :
                dirPath = os.path.join(root,path)
                frameworkList.append(dirPath)
                size = getdirsize(dirPath)
                filemodel = FileModel()
                filemodel.file = getNameFromPath(dirPath)
                filemodel.path = dirPath.replace(appPath,"")
                filemodel.size = size
                modelList.append(filemodel)

    for root, dirs, files in os.walk(appPath):
        for file in files:
            filePath = os.path.join(root,file)
            if not isInWhitelist(filePath,frameworkList):
                size = os.path.getsize(filePath)
                filemodel = FileModel()
                filemodel.file = getNameFromPath(filePath)
                filemodel.path = filePath.replace(appPath,"")
                filemodel.size = size
                modelList.append(filemodel)
    return modelList


modelList = getModelList(appPath)
cmpModelList =  getModelList(cmpPath)

modelMap = {}
for model in modelList:
    modelMap[model.path] = model.size

cmpTotal = 0
cmpMap = {}
for model in cmpModelList:
    cmpMap[model.path] = model.size
    cmpTotal += model.size

#增量比较
total = 0
for model in modelList:
    tagType = TagType.Other
    moreThanSize = 0
    if cmpMap.__contains__(model.path):
        cmpSize = cmpMap[model.path]
        moreThanSize = model.size - cmpSize
        tagType = getTag(model.size,cmpSize)
    else:
        moreThanSize = model.size
        tagType = TagType.Add    
    model.moreThanSize = moreThanSize
    model.tagType = tagType;
    total += model.size

#加入被删除的
for model in cmpModelList:
    if not modelMap.__contains__(model.path):
        model.moreThanSize = -model.size
        model.tagType = TagType.Del
        modelList.append(model)


modelList.sort(key = lambda filemodel:(filemodel.tagType,filemodel.moreThanSize),reverse = True)

result = "文件\t大小\t增量K\t标识\t路径\n"
for model in modelList:
    result += "{}\t{}\t{:.2f}\t{}\t{}\n".format(model.file,paserSizeToStr(model.size),model.moreThanSize/1024.0,getTagToStr(model.tagType),model.path)
result += "总计:{}\t增量:{}".format(paserSizeToStr(total),paserSizeToStr(total-cmpTotal))

outputFilePath = os.path.join(outPath,"pageSize.txt") 
output = open(outputFilePath, 'w') 
output.write(result)   
output.close()
print("包大小扫描 结束")

