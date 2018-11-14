import sys
import os
import time
import shutil

#扫描无用资源（代码未使用）

outPath = "/Users/luph/Documents/sizetj/" #输出目录
scanSrcPath = "/Users/luph/Documents/sizetj/entmobile-ios_7.10_composite_feature" #获取资源的源工程
scanSrcExtendPath = "/Users/luph/Documents/luph/svn/tinyvideo-ios_7.10_feature" #扩展扫描目录
outPods = True #是否排除pods目录

#前缀白名单
resPrefixWhiteList = ["yye_online_guardianlevel","yye_level_","treasureFansLevel","teampk_icon_team_","pk_png_team_","expense_lv_medal_","combo_plane_0",
                "combo_lv_medal_","bg_liveroom_confession_animationBoom_",
                "{zk","{zjt","{yjt","{xjt","{sjt","{kel",
                "zhubodengji","yyent_gift_magician_number_","yyent_gift_magician_","yye_liansongtishi_num_","yybear_loading_",
                "yonghudengji_","vulgarAppearAnimate","v_personal_","v_enterprise_","top_player_","tips_user card_labelling",
                "talentLive_time_num_","shenqu_hot_top","shenqu_boardlist_no","run_medal","qinmidudengji","official_liveroom_logobg_",
                "noble_honour_level_","myHeart","module_rank_","module_icon_","mission_quiz_pic_","majia_image_","magicDrag_down_loading_",
                "lottery_rank_","lottery_number_","lottery_compose_","live_thumb_animator_","live_notification","live_animator_image_",
                "knight_lv_num_","icon_wish_time_small_","icon_wish_time_big_","heart","group_image","gift_flash_number_white_",
                "gift_flash_number_","gift_flash_bg_lower_","gift_flash_bg_","gift_flash_","follow_anchor_living","combo_number_",
                "channel_freemode_speakingAnimation","channel_freemode_new_speakingAnimation","ch_animate_F2B_","ch_animate_B2F_",
                "RankRome_","RankNumber_","RankMedal_","TeamPVP_GiftBox_type","TeamPVP_ico_seat_delete_","TeamPVP_ico_seat_add_",
                "op_stock_","op_liveing_music_","正在发言_","环节介绍弹窗0","光","mf_",

                "video_shoot_count-down","topicMusicAlbumCover","title_","tinyVideo_icon_color_","rank_","liveing_music2","MerryBasketball_star_",
                "MerryBasketball_loading_","newBaseTemplate_speakingAnimation","happypk_",
                "3d_touch_video","3d_touch_news","3d_touch_live","3d_touch_accompany","knight_lv_",
                "TeamPVP_bg_seat_add_tips_","TeamPVP_Result_","TeamPVP_Portrait_","ic_livinig_","liveroom_",
                "mvppk_","mutillive_setting_openmic_dis" #RN用的
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


def main():
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
    

if __name__ == "__main__":
    main()