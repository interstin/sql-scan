sql注入扫描脚本


使用案例
sql.py -u http://192.168.1.1?id=1 -U http://127.0.0.1/ -M post --data "useradmin=*&password=admin"             //*代表注入点

