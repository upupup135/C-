import requests
import exrex
from IPy import IP
from scapy.all import *
from scapy.layers.l2 import Ether, ARP
from scapy.sendrecv import srp


#arp去判断是否主机存活
#构造arp包
arp_req = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst="172.16.116.0/24")
#发送arp请求
arp_resp = srp(arp_req, timeout=2, verbose=0)[0]
#遍历ARP响应
dicts = {}  #给一个空字典
for arp in arp_resp:
    mac = arp[1].hwsrc
    ip = arp[1].psrc
    #print(mac, ip)
    # 字典赋值
    dicts[ip] = mac
print(dicts)
#再去进行端口测试
#发请求80 443
#遍历字典
#写一个列表，把ip存在列表里面
ip_list = []
for ip, mac in dicts.items():
#在Python中，dicts.items() 是字典对象的一个方法，它返回一个可迭代的对象，其中包含了字典的所有键值对。 dicts字典里面的所有键值对。
#ip为键，mac为值  键值对
#打印发送出来的ip
    print(f"正在请求{ip}的80端口")
#构造请求
    try:
        res = requests.get("http://"+ip, timeout=2, verify=True)
        if res.status_code == 200:
            print(ip, "开放了80端口")
            ip_list.append({"ip":ip, "port":80})  #{"ip":ip, "port":80}为一个字典，ip_list为列表，列表里面存放着字典。ip对应的端口
    except:
        pass

#写个方法,把它保存在文件里面
def save_txt(ip_list, filename="dict.txt"):
    with open(filename, "a") as f:             #a表示追加的形式
        for i in ip_list:                      #表示一行一行写入，{i}\n表示写入一个字典就换行
            f.write(f"{i}\n")


save_txt(ip_list)

