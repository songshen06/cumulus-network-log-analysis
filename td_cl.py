#!/usr/bin/env python
# coding: utf-8

# In[196]:


import os
import fnmatch 
import re
import sys
try:
    import markup
except:
    print __doc__
    sys.exit( 1 )
from markup import oneliner as e
from collections import defaultdict


# In[197]:


class sw(object):
    def __init__(self,path):
        self.path = path
    def hw(self):
        file_hw_path = self.path + '/proc/cmdline'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            if re.search(r'cl_platform',line):
                #print line.split()[3]
                p = line.split()[3]
                platform = p.split('=')[1]
                #print platform
        return platform
    def soft_version(self):
        file_hw_path = self.path + '/etc/lsb-release'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            if re.search(r'DISTRIB_RELEASE',line):
                print line.split('=')[1]
                platform = line.split('=')[1]
        return platform
    def fw_version(self):
        file_hw_path = self.path + '/proc/mlx_sx/sx_core'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            if re.search(r'fw_ver',line):
                print line
                platform = line
        return platform
    def hostname(self):
        file_hw_path = self.path + '/etc/hostname'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            print line
            platform = line
        return platform
    def uptime(self):
        file_hw_path = self.path + '/Support/uptime'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            if re.search(r'load average',line):
                print line
                platform = line
        return platform
    def sn(self):
        file_hw_path = self.path + '/Support/decode-syseeprom'
        #print file_hw_path
        f = open(file_hw_path)
        lines=f.readlines()
        for line in lines:
            if re.search(r'^Serial',line):
                #print line
                platform = line
            if re.search(r'^Part',line):
                #print line
                pn = line
        return platform,pn


# In[198]:


def get_hardware_platform(path):
    file_hw_path = path + '/proc/cmdline'
    f = open(file_hw_path)
    lines=f.readlines()
    for line in lines:
         if re.search(r'cl_platform',line):
                print line.split()[3]
                hardware_platform = line.split()[3]
    return hardware_platform 


# In[199]:


def get_port_list(path):
    file_hw_path = path + '/Support/ifquery'
    re_swp = re.compile(r'iface swp*')
    port_list = []
    f = open(file_hw_path)
    lines=f.readlines()
    for line in lines:
        if re_swp.match(line):
            swp = line.split()[1]
            port_list.append(swp)
    print port_list
    return port_list


# In[200]:


def get_port_discard(path):
    # return a dict , key is swp, value is 0 or et
    file_hw_path = path + '/Support/port.discards.show'
    re_swp = re.compile(r'Discards *')
    port_dict = {}
    f=open(file_hw_path)
    lines=f.readlines()
    with open(file_hw_path) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_swp.match(line):
                #print line.split()[3]
                #print num
                key = line.split()[3]
                for x in range(1,11):
                    # print lines[num+x]
                    #print x
                    status = lines[num+x]
                    #print status
                    c = status[-2]
                    if c == str(0):
                        value = 0
                    else:
                        value = 'check port.discards.show'
                port_dict[key] = value
    #for port,stat in port_discard_dict.items():
    #    print ('{} {}'.format(port,stat))
    return port_dict     


# In[201]:


def get_port_info(path):
    # create a nested dict, 
    # dict[swp1][speed] 
    # dict[swp1][up_down_mtu]
    file_hw_path = path + '/Support/port.info.show'
    port_dict = defaultdict(dict)
    f = open(file_hw_path)
    lines=f.readlines()
    for line in lines:
        if re.search(r'swp',line):
            swp = line.split()[2]
            up_down_mtu = line.split()[3]
            #print line.split()[4]
            speed = line.split()[4:6]
            port_dict[swp] = {}
            port_dict[swp]['speed'] = speed
            port_dict[swp]['up_down_mtu'] = up_down_mtu
    return port_dict 


# In[238]:


def get_lldp_nei(path):
    file_hw_path = path + '/Support/lldpctl'
    port_dict = defaultdict(dict)
    f = open(file_hw_path)
    lines=f.readlines()
    re_swp = re.compile(r'Interface:*')
    #re_remote = re.compile(r'PortDescr:*')
    with open(file_hw_path) as myfile:
        for num,line in enumerate(myfile, 1):
            if re_swp.match(line):
                #print line
                #print num
                key = line.split()[1]
                #print key
                swp = ''.join(re.split(r'[^A-Za-z0-9]', key)) #remove ,
                #print swp
                sysname_line = lines[num+2]
                #print sysname_line
                sysname = sysname_line.split()[1]
                #print sysname
                remote_iface_line = lines[num+10]
                #print remote_iface_line
                remote_iface = remote_iface_line.split()[1]
                #print remote_iface
                port_dict[swp] = {}
                port_dict[swp]['remote_sys'] = sysname
                port_dict[swp]['remoet_iface'] = remote_iface
    return port_dict 


# In[239]:


def main():
    curent_path = os.getcwd()
 
    switch = sw(curent_path)
    hw = switch.hw()
    soft = switch.soft_version()
    fw = switch.fw_version()
    hostname = switch.hostname()
    uptime = switch.uptime()
    sn =switch.sn()[0]
    pn =switch.sn()[1]
    
    port_list = get_port_list(curent_path)
    port_discard_dict = get_port_discard(curent_path)
    port_info_dict = get_port_info(curent_path)
    get_lldp_nei(curent_path)


# In[240]:


if __name__ == "__main__":
    main()

