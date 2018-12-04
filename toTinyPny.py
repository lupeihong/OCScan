import tinify
import os
import enum 

#安装tinify   $ sudo  pip3 install --upgrade tinify
#AppKey 最多500不够继续申请 https://tinypng.com/developers
#AppKey 申请 https://tinypng.com/developers
#https://tinypng.com/dashboard/api
apiKey = ["apiKey1","apiKey2"]

fromFilePath = "/Users/luph/Documents/luph/git/tinyvideo" # 源路径
reportPath = "/Users/luph/Documents/sizetj/tinypng" # 报告路径
# getHasCompressPath = "/Users/luph/Documents/sizetj/tinypng/hasCompressList2018/12/3.txt" #已压缩白名单

keyIndex = 0 #取apikey用的

class FileModel :
    file = ""
    size = 0
    path = ""
    compressSize = 0
    small = 0

class ResultType(enum.IntEnum):
    Error = 1
    Sucess = 0

def createModel (path) :
    model = FileModel()
    model.file = path;
    model.size = os.path.getsize(path)
    return model

def compressImg(path):
    print("压缩 {} 中...".format(path))

    global keyIndex
    key = apiKey[keyIndex]
    print ("{},{}".format(keyIndex,key))
    tinify.key = key
    try:
        source = tinify.from_file(path)
        source.to_file(path)
    except tinify.AccountError as e:
        print("key：{}次数已用完：{}".format(key,e.message))
        keyIndex += 1
        if keyIndex >= len(apiKey):
            print("没有足够的KPIkey可用 index：{}".format(keyIndex))
            return ResultType.Error
        return compressImg(path)
    except Exception as e:
        print("压缩出现错误：{}".format(e))
        return ResultType.Error
    return ResultType.Sucess

    

def saveCompressList(hasCompressList):
    outFileName = "hasCompressList.txt" 
    outputFilePath = os.path.join(reportPath,outFileName) 
    output = open(outputFilePath, 'w') 
    hasCompressShortList = map(lambda x: x.replace(fromFilePath,"") , hasCompressList)
    result = "\n".join(hasCompressShortList)  
    output.write(result)   
    output.close()

def getCompressList():
    inFileName = "hasCompressList.txt" 
    inputFilePath = os.path.join(reportPath,inFileName) 
    # if ( getHasCompressPath != "" ) :
    #     inputFilePath = getHasCompressPath;
    if not os.path.exists(inputFilePath) :
        return []
    rput = open(inputFilePath, 'r') 
    result =  rput.read()
    hasCompressList = result.split('\n')
    rput.close()
    return hasCompressList

def saveReport(imgList):
    result = "文件名称\t文件大小K\t压缩大小K\t减少K\t增幅%\n"
    for model in imgList :
        result += "{}\t{:.2f}\t{:.2f}\t{:.2f}\t{:.2f}\n".format(model.file,model.size/1024,model.compressSize/1024,model.size/1024-model.compressSize/1024,model.small)

    outFileName = "tinypngReport.txt" 
    outputFilePath = os.path.join(reportPath,outFileName) 
    output = open(outputFilePath, 'w') 
    output.write(result)   
    output.close()

def saveJPEGPath(pathlist):
    outFileName = "jpegList.txt" 
    outputFilePath = os.path.join(reportPath,outFileName) 
    output = open(outputFilePath, 'w') 
    hasCompressShortList = map(lambda x: x.replace(fromFilePath,"") , pathlist)
    result = "\n".join(hasCompressShortList)  
    output.write(result)   
    output.close()

def runTinyPNG():
    jpegPath = []
    pathList = []
    imgList = []
    for root, dirs, files in os.walk(fromFilePath):
        for file in files:
            fileName, fileSuffix = os.path.splitext(file)
            if fileSuffix == ".png" or fileSuffix == ".jpg":
                path = os.path.join(root,file)
                pathList.append(path)
            elif fileSuffix == ".jpeg" :
                path = os.path.join(root,file)
                jpegPath.append(path)

    # if len(pathList) > 500*len(apiKey) :
    #     print("太多了，apikey不够用（要继续注释这段）：{}".format(len(pathList)))
    #     return

    if len(jpegPath) > 0 :
        saveJPEGPath(jpegPath)

    hasCompressList = getCompressList()
    count = len(hasCompressList)
    for path in pathList:
        #判断是否以前有压缩过了
        shortPath = path.replace(fromFilePath,"")
        if shortPath in hasCompressList: 
            continue

        fileModel = createModel(path)
        result = compressImg(path)
        if result == ResultType.Error:
            #出错了先保存已压缩进度
            if len(hasCompressList) > count:
                saveCompressList(hasCompressList)
            saveReport(imgList)
            return

        hasCompressList.append(path)
        fileModel.compressSize = os.path.getsize(path)
        fileModel.small = (fileModel.compressSize - fileModel.size ) / fileModel.size * 100
        imgList.append(fileModel)

    if len(hasCompressList) > count:
        saveCompressList(hasCompressList)

    saveReport(imgList)
    print("tinypng压缩完成")

            
if __name__ == "__main__":
    runTinyPNG()   

    
