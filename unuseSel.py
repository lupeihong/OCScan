import os
import re

#扫描未调用select

outPath = "/Users/xxx/Documents/sizetj/" #输出目录
mathoFilePaht = "/Users/xxx/Documents/sizetj/7.9/YYMobile.app/YYMobile" #可执行文件
linkmapPath = "/Users/xxx/Documents/sizetj/7.9/YYMobile-LinkMap-normal-arm64.txt"
selrefsFile =  outPath+"/selrefs.txt" #引用sel文件
cmd = "otool -v -s __DATA __objc_selrefs "+ mathoFilePaht +" > "+selrefsFile
os.system(cmd) #逆向selrefs段

linkmapContent = open(linkmapPath,encoding="utf8", errors='ignore').read()
pattern = re.compile(r'[+|-]\[\w+ \w+\]') 
selall = pattern.findall(linkmapContent)

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
for sel in selall:
    print("正在扫描【{0}】".format(sel))
    selMth = sel.replace("+",'')
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
        print("发现无用方法【{0}】".format(sel))
        output.write("{0}\n".format(sel))  
     
output.close()
print("扫描结束")
