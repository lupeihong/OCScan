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


# 查找无用资源实践

### 概述
- 项目经过多个版本迭代，在业务模块删减过程可能会产生一部分无用资源
这种资源，一般我们取项目中的xcassets中的imageset资源名，对工程中.m、xib、storyboard文件进行匹配扫描，若资源名存在于文件中，则可初步说明该资源存在引用.
使用脚本```unuseResScan.py```,设置
```
outPath = "/Users/Documents/sizetj/" #输出目录
scanSrcPath = "/Users/Documents/sizetj/entmobile-ios_7.10_composite_feature" #获取资源的源工程
scanSrcExtendPath = "/Users/Documents/luph/svn/tinyvideo-ios_7.10_feature" #扩展扫描目录
outPods = True #是否排除pods目录
```
执行可在unuseRes目录产出不同xcassets对应的无用资源txt



- 另外，在新增业务功能的时候，某个功能需要用到图片资源，但一般开发可能并不清楚先前工程是否有可用图片，而重复引入了新的资源图片，
最终可能导致同一张图片，在工程不同地方重复添加（资源名不同，内容一样）。
针对这种情况，可借助第三方工具fdupes，此可工具可查找目录下所有相同内容的文件，这里，我们只扫描xcassets目录
使用脚本```dupesRes.py```，配置
```
scanTargetDir = "/Users/Documents/sizetj/entmobile-ios_7.10_composite_feature"
```
执行结果存于dupRes.txt
