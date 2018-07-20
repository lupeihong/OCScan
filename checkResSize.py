import os
import enum 
#扫描重复（内容）资源

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
scanTargetDir = "/Users/xxx/Documents/luph/svn/ios_7.8.10_maint"
cmpTargetDir = "/Users/xxx/Documents/luph/svn/ios_7.8_maint"


class TagType(enum.IntEnum):
    Add = 4
    Up = 3
    Down = 2
    Del = 1
    Other = 0


class FileModel :
    file = ""
    size = 0
    moreThan = 0
    path = ""
    tagType = TagType.Other

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

def getDirOrFileBySuffix(scanImagePath,suffix):
    dirList = []
    for root, dirs, files in os.walk(scanImagePath):
        for dir in dirs:
                if dir.endswith(suffix):
                    imagePathDir = os.path.join(root, dir)
                    dirList.append(imagePathDir)  
    return dirList

def getPngList(resPath):
    xcassetsPathList = getDirOrFileBySuffix(resPath,".xcassets")

    total = 0
    pngList = []
    pngPahtMap = {}
    for path in xcassetsPathList:
        for root, dirs, files in os.walk(path):   
            for file in files:   
                if file.endswith(".png"):
                    pngPath = os.path.join(root,file)
                    shortPngPath = pngPath.replace(resPath,"")

                    fileModel = FileModel()
                    fileModel.path = shortPngPath
                    fileModel.size = os.path.getsize(pngPath)
                    fileModel.file = file

                    pngList.append(fileModel)
                    pngPahtMap[shortPngPath] = fileModel
                    total += fileModel.size

    return pngList,pngPahtMap,total


pngList,pngMap,pngTotal = getPngList(scanTargetDir)
cmpPngList,cmpPngMap,cmpTotal = getPngList(cmpTargetDir)

for model in pngList:
    if cmpPngMap.__contains__(model.path):
        cmpModel = cmpPngMap[model.path]
        model.tagType = getTag(model.size,cmpModel.size)
        model.moreThan = model.size - cmpModel.size
    else:
        model.tagType = TagType.Add
        model.moreThan = model.size


#拼进已删除的
for model in cmpPngList:
    if not pngMap.__contains__(model.path):
        model.tagType = TagType.Del
        model.moreThan = -model.size
        pngList.append(model)

result = "文件名称\t文件大小\t增量K\t标识\t路径\n"
for model in pngList:
    result += "{}\t{}\t{:.2f}\t{}\t{}\n".format(model.file,paserSizeToStr(model.size),model.moreThan/1024.0,getTagToStr(model.tagType),model.path)
result += "总大小：{}\t增量：{}\n".format(paserSizeToStr(pngTotal),paserSizeToStr(pngTotal-cmpTotal))


outputFilePath = os.path.join(outPath,"imageResSize.txt") 
output = open(outputFilePath, 'w') 
output.write(result)   
output.close()
print("图片资源大小扫描 结束")