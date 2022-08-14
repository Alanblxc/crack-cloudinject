from pyDes import *
import binascii
import os
import sys
from fnmatch import fnmatch
import re
import shutil


Des_IV = "12345678" # 自定IV向量（官网例子就是这么写的）


#解密id算法
def decrypt_str(s):
 k = des(Des_Key, ECB, Des_IV, pad=None, padmode=PAD_PKCS5)
 de = k.decrypt(binascii.a2b_hex(s), padmode=PAD_PKCS5)
 return de

if __name__ == "__main__":
 if len(sys.argv) == 1:
   print("一键破解云注入 by 哔哩哔哩艾伦嗷")
   print("使用方法：python app.py apk名")
 else:
   apk_name = sys.argv[1]
   print("反编译安装包ing...")
   val = os.system('java -jar apktool.jar d ' + apk_name + ' -o out')
   print(val)
   print("反编译完成！")
   print("------------------------------------------------")
   file_name = list()        #新建列表
   for i in os.listdir("out"):        #获取filePath路径下所有文件名
        data_collect = ''.join(i)        #文件名字符串格式
        file_name.append(data_collect)   
   dex_list = list()
   print("寻找云注入文件ing...")
   for file in file_name:
    if fnmatch(file, 'smali*'):
     if os.path.lexists(r'out/'+file+"/com/cloudinject/feature/App.smali"):
        cloudinject_dex=file  #云注入的dex
        app_dex ='out/'+file+"/com/cloudinject/feature/App.smali"
        print (app_dex)
        print("------------------------------------------------")
        with open(app_dex, "r", encoding='UTF-8')as f:
         dex_res = f.read()
         f.close()
        A=re.compile('.field public static A:Ljava/lang/String; = \"(.+)\"') 
        result_applications=A.findall(dex_res)
        print("寻找加密后的application...")
        print (result_applications)
        print("------------------------------------------------")
        print("寻找id ing...")
        appid=re.compile('.field public static APP_ID:Ljava/lang/String; = \"(.+)\"') 
        result_id=appid.findall(dex_res)
        print(result_id)
        print("------------------------------------------------")
        result_id1 =result_id[0]
        print("截取密钥Ing....")
        print(result_id1[0:8])
        print("------------------------------------------------")
        print("解密Application ing...")
        Des_Key = result_id1[0:8]
        application=decrypt_str(result_applications[0])
        print(str(application)[2:-1])
        print("------------------------------------------------")
        print("替换Application ing...")
        with open("out/AndroidManifest.xml", "r", encoding='UTF-8')as xml1:
            xml_res=xml1.read()
            new_xml=xml_res.replace("com.cloudinject.feature.App",str(application)[2:-1])
            xml1.close()
        with open("out/AndroidManifest.xml", "w+", encoding='UTF-8')as xml2:
            xml2.write(new_xml)
            xml2.close()
        print("替换成功！")
        print("------------------------------------------------")
        print("删除云注入文件ing...")
        
        os.remove("out/assets/cloudinject")
        shutil.rmtree("out/"+file)
        print("------------------------------------------------")
        print("打包apk ing...")
        val2 = os.system('java -jar apktool.jar b out -o out.apk')
        shutil.rmtree("out")
