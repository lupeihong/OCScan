import os
import re

#扫描未调用select

outPath = "/Users/luph/Documents/sizetj/" #输出目录
mathoFilePaht = "/Users/luph/Documents/sizetj/7.11/Payload/YYMobile.app/YYMobile" #可执行文件
linkmapPath = "/Users/luph/Documents/sizetj/7.11/YYMobile-LinkMap-normal-arm64.txt"

whileList = ["libAFNetworking.a","libMBProgressHUD.a","libBaseApiSDK.a","libCocoaAsyncSocket.a","libFBRetainCycleDetector.a","libFMDB.a",
"libHWFunctional-YY.a","libJSONModel.a","libMJRefresh.a","libOAStackView.a","libOOMDetector.a","libPerfReportSDK.a","libProtobuf.a","libRaptureXML-iOS9.0.a",
"libReactiveObjC.a","libYYAppleIAPSDK.a","libYYKit-YY.a","libYYReactNativeSDK.a","libZipArchive.a","AMapFoundationKit.framework",
"AMapSearchKit.framework","libaudio_static.a","libGPUImage.a","libgslbsdk.a","libHiidoAdTrackingSDK.a","libHiidoSDK.a","libpushsdk.a","libcocos2dxlua.a",
"ShareSDK-YY","libtransvodstatic.a","TXFaceVeirfySDKs","udbauthsdk","y2aplayer","yyabtestsdk","yyantilib","yycertifysdk","yycloudbs2sdk",
"yylivekit","yylivesdk","yyplayersdk","yyvideolib","ZMCreditSDK-YY"]

class SymbolModel:
    symbol = ""
    size = 0
    path = ""

def getLinkmapSymbols(linkpath):
    reachFiles = False
    reachSymbols = False
    reachSections = False
    fileMap = {}
    symoblList = []
    pattern = re.compile(r'[+|-]\[\w+ \w+\]') 
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
                    fileMap[oIndex] = ofilePath
            elif reachFiles == True and reachSections == True and reachSymbols == True :
                    symbolsArray = line.split("\t")
                    if len(symbolsArray) == 3 :
                        fileKeyAndName = symbolsArray[2]
                        symbolSize = int(symbolsArray[1],16)

                        fileKeyAndName = fileKeyAndName.replace("\n","")
                        index = fileKeyAndName.find("]",0,len(line))
                        if index != -1 :
                            oIndex = fileKeyAndName[:index+1]
                            symoblPart = pattern.findall(fileKeyAndName) #获取符号部分
                            if len(symoblPart) > 0:
                                symobl = SymbolModel()
                                symobl.symbol = symoblPart[0]
                                symobl.path = fileMap[oIndex]
                                symobl.size = symbolSize
                                symoblList.append(symobl)
                            
    linkfile.close()
    return symoblList



selrefsFile =  outPath+"/selrefs.txt" #引用sel文件
cmd = "otool -v -s __DATA __objc_selrefs "+ mathoFilePaht +" > "+selrefsFile
os.system(cmd) #逆向selrefs段

# linkmapContent = open(linkmapPath,encoding="utf8", errors='ignore').read()
# pattern = re.compile(r'[+|-]\[\w+ \w+\]') 
# selall = pattern.findall(linkmapContent)
selall = getLinkmapSymbols(linkmapPath)

# outputSelrefs = open(outPath+"outputSelrefs.txt", 'w')
selrefsF = open(selrefsFile,encoding="utf8", errors='ignore')
selrefsList = []
for line in selrefsF.readlines():
    if '__objc_methname' in line:
        line = line.strip("\n");
        lineSplit = line.split(":")
        if  len(lineSplit)  > 0:
            selrefs = ""
            lineSplit.reverse()
            for subStr in lineSplit:
                if len(subStr) > 0:
                    selrefs = subStr
                    break
            if len(selrefs) > 0:
                selrefsList.append(selrefs)
# outputSelrefs.write("{0}".format(selrefsList))
# outputSelrefs.close()
selrefsF.close()   


output = open(outPath+"unUseSel.txt", 'w')
output.write("符号\t大小\t路径\n") 
for sel in selall:
    print("正在扫描【{0}】".format(sel.symbol))
    selMth = sel.symbol
    selMth = selMth.replace("+",'')
    selMth = selMth.replace("-",'')
    selMth = selMth.replace("[",'')
    selMth = selMth.replace("]",'')
    selL = selMth.split(" ")
    selMth = selL[1]
    isUse = False
    for selref in selrefsList:
        if  selref == selMth:
            isUse = True
            break 
    if not isUse:
        print("发现无用方法【{0}】".format(sel.symbol))
        output.write("{}\t{}\t{}\n".format(sel.symbol,sel.size,sel.path))  
     
output.close()
print("扫描结束")
