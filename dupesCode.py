import os
import time
import shutil

outPath = "/Users/luph/Documents/sizetj/" #输出目录
scanSrcPath = "/Users/luph/Documents/luph/svn/entmobile-ios_7.12_composite_feature" #源工程
toolShellPath = "/Users/luph/Documents/sizetj/tool/pmd-bin-6.4.0/bin/run.sh" #需要pmd工具  https://sourceforge.net/projects/pmd/files/pmd/ 

minDupeLine = 120 #最小重复代码行

def rmDir(fileOrDir):
    cmd = "rm -rf "+fileOrDir
    os.system(cmd)

tmpDir = time.strftime("TmpPro_%Y-%m-%d-%H_%M_%S",time.localtime(time.time())) 
scanTargetDir = outPath+tmpDir #创建临时目录（因为会删文件）

# cmd_cp = "mkdir -p "+scanTargetDir +" | cp -rf "+scanSrcPath+" "+ scanTargetDir
# os.system(cmd_cp)
shutil.copytree(scanSrcPath, scanTargetDir)
rmDir(scanTargetDir+"/Pods")

outFile = outPath + "codeCheck.csv" 
cmd = toolShellPath + " cpd --language ObjectiveC --minimum-tokens "+"{}".format(minDupeLine)+" --format csv_with_linecount_per_file  --files "+scanTargetDir+" > "+outFile
os.system(cmd)

print("重复代码扫描结束")
rmDir(scanTargetDir)