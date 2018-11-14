import os
import time
import json
import shutil

outPath = "/Users/luph/Documents/sizetj/" #输出目录
scanTargetDir = "/Users/luph/Documents/luph/svn/tinyvideo-ios_7.12_appThinning_feature"
isBackUpTodo = False

class FileModel :
    file = ""
    size = 0

def getDirOrFileBySuffix(scanImagePath,suffix):
    dirList = []
    for root, dirs, files in os.walk(scanImagePath):
        for dir in dirs:
                if dir.endswith(suffix):
                    imagePathDir = os.path.join(root, dir)
                    dirList.append(imagePathDir)  
    return dirList

def createFileModel(path):
    model = FileModel()
    model.file = path
    model.size = os.path.getsize(path)
    return model

def main():
    scanTmpTargetDir = scanTargetDir
    if isBackUpTodo :
        tmpDir = time.strftime("TmpPro_%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
        scanTmpTargetDir = outPath+tmpDir #创建临时目录（因为后面会删文件）
        shutil.copytree(scanTargetDir, scanTmpTargetDir)

    # scanTmpTargetDir = "/Users/luph/Documents/sizetj/TmpPro_2018-08-28-16_23_54"

    imagesetPathList = getDirOrFileBySuffix(scanTmpTargetDir,".imageset")
    image3xList = []
    for path in imagesetPathList:
        for root, dirs, files in os.walk(path):   
            for file in files:  
                if file == "Contents.json":
                    contentFile = os.path.join(root,file) 
                    print("处理3x资源json",contentFile)
                    imageJsonFile = open(contentFile, 'r',encoding="utf-8") 
                    loadDict = json.load(imageJsonFile)
                    if loadDict.__contains__("images"):
                        imagesList = loadDict["images"]
                        for imageInfo in imagesList:
                            if imageInfo["scale"] == "3x" and imageInfo.__contains__("filename"):
                                imagesList.remove(imageInfo)
                                loadDict["images"] = imagesList
                                imageJsonFileW = open(contentFile, 'w')
                                json.dump(loadDict,imageJsonFileW)
                                imageJsonFileW.close()

                                imageNamePath = os.path.join(root,imageInfo["filename"])
                                if os.path.exists(imageNamePath):
                                    fileModel = createFileModel(imageNamePath)
                                    image3xList.append(fileModel)
                                    os.remove(imageNamePath)
                                    print("删除了3x资源",imageNamePath)
                                
                                break
                    imageJsonFile.close()
    

    output = open(outPath+"del3x.txt", 'w')
    output.write("路径\t大小k\n") 
    for model in image3xList:
        output.write("{}\t{}\n".format(model.file,model.size/1024))
    output.close()

if __name__ == "__main__":
    main()                        