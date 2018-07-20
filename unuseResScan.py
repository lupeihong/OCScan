import sys
import os
import time
import shutil

#扫描无用资源（代码未使用）

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
scanSrcPath = "/Users/xxx/Documents/xxx/svn/ios_7.8.10_maint" #获取资源的源工程
scanSrcExtendPath = "/Users/xxx/Documents/xxx/svn/7.8.10_maint/Tiny" #扩展扫描目录
outPods = True #是否排除pods目录

#前缀白名单
resPrefixWhiteList = ["treasureFansLevel","teampk_icon_team_","pk_png_team_","expense_lv_medal_","combo_plane_0",
                "{zk","{zjt","{yjt","{xjt","{sjt","{kel"
                ]

tmpDir = time.strftime("TmpPro_%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
scanTargetDir = outPath+tmpDir #创建临时目录（因为后面会删文件）

def isInResWhiteList(name):
    for prefix in resPrefixWhiteList:
        if name.startswith(prefix):
            return True
    return False

class FileModel :
    file = ""
    size = 0
    path = ""

def getdirsize(dir):  
    size = 0
    if os.path.isdir(dir):
        for root, dirs, files in os.walk(dir):
            for file in files :
                size += os.path.getsize(os.path.join(root, file)) 
    else:
        size = os.path.getsize(dir)
    return size  

def getDirOrFileBySuffix(scanImagePath,suffix):
    dirList = []
    for root, dirs, files in os.walk(scanImagePath):
        for dir in dirs:
                if dir.endswith(suffix):
                    imagePathDir = os.path.join(root, dir)
                    dirList.append(imagePathDir)  
    return dirList

def getImagesetNamelist(scanImagePath,suffix):
    imageNamelist = []
    for root, dirs, files in os.walk(scanImagePath):
        for file in dirs:
            if file.endswith(suffix) and not isInResWhiteList(file):
                imagePathDir = os.path.join(root, file)
                imageName = file.replace(suffix,'')
                fileModel = FileModel()
                fileModel.file = imageName
                fileModel.size = getdirsize(imagePathDir)
                fileModel.path = imagePathDir.replace(scanTargetDir,'')
                # imageNamelist.append(imageName)
                imageNamelist.append(fileModel)
    return imageNamelist

def getImageNamelist(scanImagePath,suffix):
    imageNamelist = []
    for root, dirs, files in os.walk(scanImagePath):
        for file in files:
            if file.endswith(suffix) and not isInResWhiteList(file):
                imagePathDir = os.path.join(root, file)
                imageName = file.replace(suffix,'')
                imageName = imageName.replace("@2x",'')
                imageName = imageName.replace("@3x",'')
                
                fileModel = FileModel()
                fileModel.file = imageName
                fileModel.size = getdirsize(imagePathDir)
                fileModel.path = imagePathDir.replace(scanTargetDir,'')

                # imageNamelist.append(imageName)
                imageNamelist.append(fileModel)
    return imageNamelist

def isFindRes(scanContent,resName):
    return scanContent.find(resName,0,len(scanContent))
    
def scanAction(imageNamelist,scanTargetDir):
    scanSuffix_m = ".m"
    scanSuffix_mm = ".mm"
    scanSuffix_xib = ".xib"
    scanSuffix_sb = ".storyboard"
    invalidResList = []
    for nameModel in imageNamelist :
        isExist = False
        for root, dirs, files in os.walk(scanTargetDir):
            for file in files:
                currentFilePath = os.path.join(root,file)
                if (not os.path.isdir(currentFilePath)) and (file.endswith(scanSuffix_m) or file.endswith(scanSuffix_xib) or file.endswith(scanSuffix_sb) or file.endswith(scanSuffix_mm)):
                    try:
                        f = open(currentFilePath, "r")
                        fileContent = f.read()
                        isFind = fileContent.find(nameModel.file,0,len(fileContent))
                        if isFind != -1:
                            isExist = True
                            break
                    except:
                        print ("读取失败%s",currentFilePath)
                    finally:
                        f.close()
            if isExist:
                break

        if not isExist:
            print ("找到无用资源：",nameModel.file)
            invalidResList.append(nameModel)
    return invalidResList

def rmDir(fileOrDir):
    cmd = "rm -rf "+fileOrDir
    os.system(cmd)

def getName(path):
    pathlist = path.split("/")
    timeStamp = int(time.time())
    nameDir = "{}_{}".format(pathlist[-1],timeStamp)
    # nameDir = time.strftime("%Y-%m-%d-%H_%M_%S",pathlist[-1],time.localtime(time.time())) 
    return nameDir


# cmd_cp = "mkdir -p "+scanTargetDir +" | cp -rf "+scanSrcPath+" "+ scanTargetDir
# os.system(cmd_cp)
shutil.copytree(scanSrcPath, scanTargetDir)
shutil.copytree(scanSrcExtendPath,os.path.join(scanTargetDir,scanSrcExtendPath.split("/")[-1]))
if outPods:
    rmDir(scanTargetDir+"/Pods")  


# scanImagePathCfg = [
# (".imageset",
# [scanTargetDir+"/YYMobile/Images.xcassets",
# scanTargetDir+"/YYMobile/YingShou.xcassets",
# scanTargetDir+"/YYMobile/TemplatePlugin/MakeFriends/yytp_makefriend.xcassets",
# scanTargetDir+"/YYMobile/TemplatePlugin/OnePiece/OnePiece.xcassets",
# scanTargetDir+"/YYMobile/TemplatePlugin/VoiceRoom/Images/VoiceRoom.xcassets"]
# ),
# (".png",
# [scanTargetDir])#在无xcassets的情况下使用
# ]

xcassetsPathList = getDirOrFileBySuffix(scanTargetDir,".xcassets")
print("有以下xcassets\n【{0}】".format(xcassetsPathList))
scanImagePathCfg = [
(".imageset",
xcassetsPathList
),
(".png",
[scanTargetDir])#在无xcassets的情况下使用
]

#白名单中的不会检查
# whiteList = ["3rd/SSKeychain/Example/iOS/Images.xcassets",
# "YYMobile/YingShou.xcassets",
# ]
whiteList = []

def isInWhileList(curPath):
    for white in whiteList:
        if white in  curPath:
            return True
    return False


for cfg in scanImagePathCfg:
    suffix = cfg[0]
    for scanImagePath in cfg[1]:
        if isInWhileList(scanImagePath):
            continue
        imageNamelist = []
        print("开始检查【{0}】".format(scanImagePath))
        imageNamelist = []
        if os.path.isdir(scanImagePath) and suffix == ".imageset":
            imageNamelist = getImagesetNamelist(scanImagePath,suffix)
        else:
            imageNamelist = getImageNamelist(scanImagePath,suffix)
        invalidResList = scanAction(imageNamelist,scanTargetDir)
        invalidResList.sort(key = lambda filemodel:(filemodel.file,filemodel.size),reverse = True)
        #输出
        result = "资源名\t大小K\t路径\n"
        for model in invalidResList:
            result += "{}\t{:.2f}\t{}\n".format(model.file,model.size/1024.0,model.path)
        outFileName = getName(scanImagePath)
        outputDir = outPath+"unuseRes"
        os.system("mkdir -p "+outputDir)
        outputFilePath = os.path.join(outputDir,outFileName+"_unuseRes.txt") 
        output = open(outputFilePath, 'w') 
        output.write(result)   
        output.close()
        rmDir(scanImagePath)
