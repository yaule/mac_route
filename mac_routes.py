#!/usr/bin/env python
#-*-coding:utf-8-*-
import os,sys,urllib,commands
def dowl_file():
  '''
  下载最新的ip列表
  '''
  f_test = os.path.isfile('delegated-apnic-latest')
  if f_test:
    os.remove('delegated-apnic-latest')
  url = 'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
  print 'download delegated-apnic-latest'
  urllib.urlretrieve(url,'delegated-apnic-latest')

def cn_list():
  '''
  根据列表文件生成中国ip列表
  '''
  latest_ip = file('delegated-apnic-latest','rb')
  cn_ip = file('cn_ip','wb')
  print 'Generation CN IP'
  for lines in latest_ip.xreadlines():
    if lines.find('apnic|CN|ipv4') != -1:
      line = lines.split('|')
      if line[1] == 'CN' and line[2] == 'ipv4':
        mask = 32
        while line[4] > 1 :
          line[4] = int(line[4])/2
          mask-=1
        w_data = '%s/%s\n' %(line[3],str(mask))
        cn_ip.write(w_data)

def def_gw():
  '''
  en0 网卡的默认网关
  '''
  def_gw = commands.getoutput("netstat -nr |grep default|grep en0|awk '{print $2}'")
  return def_gw

def route_change(act,gw):
  '''
  修改路由表
  '''
  cn_ip_r = file('cn_ip','rb')
  for line in cn_ip_r.xreadlines():
    ip = line.strip('\n')
    commands.getoutput("sudo route %s %s %s &>/dev/null" %(act,ip,gw))

def main():
  arg = sys.argv
  if len(arg) != 2:
    print 'add change del reset'
    sys.exit()
  args = arg[1]
  if args == 'new':
    dowl_file()
    cn_list()
    route_change('add',def_gw())
  elif args == 'add':
    route_change('add',def_gw())
  elif args == 'change':
    route_change('change',def_gw())
  elif args == 'del':
    route_change('delete',def_gw())
  elif args == 'reset':
    dowl_file()
    route_change('delete',def_gw())
    cn_list()
    route_change('add',def_gw())
  else:
    help_test = '''
    new | add | change | del | reset
    '''
    print help_test
if __name__ == "__main__":
  main()
