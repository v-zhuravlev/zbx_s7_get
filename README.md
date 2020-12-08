# zbx_s7_get

Simple Zabbix python3 script, to get values from Siemens S7 PLCs using [snap7 suite](http://snap7.sourceforge.net/) and [python-snap7](https://python-snap7.readthedocs.io/en/latest/).

## Install

Example for Zabbix server/proxy running on Centos 7:

1. Download snap7 from https://sourceforge.net/projects/snap7/files/
2. Install snap7:

```shell
7za x snap7-full-1.4.2.7z
sudo yum groupinstall 'Development Tools'
cd snap7-full-1.4.2/build/unix
make -f x86_64_linux.mk
sudo make -f x86_64_linux.mk install
sudo ldconfig
```

3. Install python-snap7:

`sudo python3 -m pip install python-snap7`

4. Copy s7_get.py to /usr/lib/zabbix/externalscripts/:

```shell
cp s7_get.py /usr/lib/zabbix/externalscripts
chmod +x /usr/lib/zabbix/externalscripts
```

5. Test the script by running it directly from shell:

```shell
$ ./s7_get.py 172.10.1.1 0 0 66 2 int
6
```

## Setup in Zabbix

Create new item:

- **Type**: External check
- **Key**: `s7_get.py[<s7_ip_address>,<s7_rack>,<s7_slot>,<DB>,<offset>,<datatype>]`, where datatype = `int`,`bool` or `float`.

For example:

![image](https://user-images.githubusercontent.com/14870891/71446515-3722d100-2735-11ea-9f73-7ede081be490.png)

