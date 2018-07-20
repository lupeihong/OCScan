import os

#扫描重复（内容）资源

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
scanTargetDir = "/Users/xxx/Documents/luph/svn/ios_7.9_composite_feature"

def getDirOrFileBySuffix(scanImagePath,suffix):
    dirList = []
    for root, dirs, files in os.walk(scanImagePath):
        for dir in dirs:
                if dir.endswith(suffix):
                    imagePathDir = os.path.join(root, dir)
                    dirList.append(imagePathDir)  
    return dirList


xcassetsPathList = getDirOrFileBySuffix(scanTargetDir,".xcassets")
print("有以下xcassets\n{0}".format(xcassetsPathList))
cmd = "fdupes -Sr "
for path in xcassetsPathList:
    cmd += " " + path

cmd += " > " + outPath + "dupRes.txt"

#需要安装fdupes https://github.com/adrianlopezroche/fdupes  brew install fdupes
os.system(cmd)
# tmp = os.popen(cmd).readlines()        
print("资源重复扫描结束")