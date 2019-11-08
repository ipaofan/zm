# encoding:utf-8
import paramiko
import os

def remote_scp():
    HOST_IP = '47.95.120.23'
    REMOTE_PATH = '/work/update_gdtcookies/'
    REMOTE_FILENAME = 'info.json'
    LOCAL_PATH = './'
    USERNAME = 'zmwork'
    PASSWORD = 'ab&C2S8$14Xr#s0o'
    if not os.path.isdir(LOCAL_PATH):
        os.makedirs(LOCAL_PATH)
    if not os.path.isfile(LOCAL_PATH + '/' + REMOTE_FILENAME):
        fp = open(LOCAL_PATH + '/' + REMOTE_FILENAME, 'w')
        fp.close()
    t = paramiko.Transport((HOST_IP, 22))
    t.connect(username=USERNAME, password=PASSWORD)  # 登录远程服务器
    sftp = paramiko.SFTPClient.from_transport(t)  # sftp传输协议
    src = REMOTE_PATH + '/' + REMOTE_FILENAME
    des = LOCAL_PATH + '/' + REMOTE_FILENAME
    sftp.get(src, des)
    t.close()

if __name__ == '__main__':
    remote_scp()
