# coding:utf8
import urllib3
import os
import shutil
import time

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)  #禁用requests安全建议警告，不影响结果

current_dir = '/Users/edz/Desktop/zhengmangProject/UpdateGdtCookies/'
# current_dir = '/work/update_gdtcookies/'
ssh_file_path = '/work/update_gdtcookies/gdt_cookie.json'
cookie_file_name = 'gdt_cookie.json'
executable_path='/Users/edz/Desktop/chromedriver'


def send_ssh():
    import paramiko  # 此模块用于连接虚拟机,ansible底层用此模块
    hostname = '47.95.120.23'
    port = 22
    username = 'zmwork'
    password = 'ab&C2S8$14Xr#s0o'
    t = paramiko.Transport((hostname, port))
    t.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(t)
    cookie_file_path = current_dir + cookie_file_name
    sftp.put(cookie_file_path, ssh_file_path)
    sftp.close()
    print('{}成功上传！'.format(cookie_file_name))

    # 判断cookie文件是否存在
    if os.path.exists(cookie_file_name):
        print('file is exit!')
        srcfile = current_dir + cookie_file_name
        dstfile = current_dir + 'cookie_files/' + str(round(time.time()*1000)) + '_gdt_cookie.json'
        fpath, fname = os.path.split(dstfile)  # 分离文件名和路径
        print(fpath)
        print(fname)
        if not os.path.exists(fpath):
            os.makedirs(fpath)
        shutil.move(srcfile,dstfile)
        print('{}移动成功！'.format(cookie_file_name))


if __name__ == '__main__':
    send_ssh()
#getcampaignmultidimensionlist