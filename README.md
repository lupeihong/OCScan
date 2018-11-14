# OCScan
oc代码质量扫描、包大小分享

# 包体积增量自动化分析

### 概述
该脚本可以统计两个包对比后的增量大小，产出的结果可作为用户进一步分析的基础数据，其中
输出的结果用四种标识进行区分
- ```+``` ：新增文件	
- ```↑```：体积增加	
- ```-``` ：文件已删除	
- ```↓```：体积减少

使用脚本```pageSizeCheck.py```，对两个app文件进行分析 ,设置
```
outPath = "/Users/luph/Documents/sizetj/" #输出目录
appPath = "/Users/luph/Documents/sizetj/7.10/Payload/YYMobile.app"
cmpPath = "/Users/luph/Documents/sizetj/7.9.1/Payload/YYMobile.app" #对比文件
```
执行可在输出目录下产出pageSize.txt结果


对应代码段的分析，可以使用```linkMapCheck.py```，设置
```
outPath = "/Users/luph/Documents/sizetj/" #输出目录
linkmapPath = "/Users/luph/Documents/sizetj/7.10/YYMobile-LinkMap-normal-arm64.txt"
compareLinkmapPath = "/Users/luph/Documents/sizetj/7.9.1/YYMobile-LinkMap-normal-arm64.txt" #对比文件
```
执行可在输出目录下产出linkMapSize.txt结果

可设置
```
isGroud = True #是否分组统计
```
可对使统计粒度扩大到库级别统计，
输出linkMapSizeByGroud.txt
