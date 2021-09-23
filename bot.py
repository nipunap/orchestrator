#!/usr/bin/env python3
import filecmp
import os
from lib import botlib
from lib import debhandler

def copy_nginx_file():
    # nginx configuration files
    dst_confile='/etc/nginx/sites-available/default'
    src_confile='nginx/default.nginx'
    #compare config files
    check = filecmp.cmp(src_confile, dst_confile)
    #copy files if has a diff
    if (check):
        os.system("mv {} {}".format(src_confile,dst_confile))
        botlib.file_permission(dst_confile, 0o744)
        botlib.file_ownership(dst_confile, 0, 0)
        botlib.restart_service('nginx')

def copy_index_php():
    # nginx configuration files
    dst_confile='/var/www/html/index.php'
    src_confile='nginx/index.php'
    #compare config files
    check = filecmp.cmp(src_confile, dst_confile)
    #copy files if has a diff
    if (check):
        os.system("mv {} {}".format(src_confile,dst_confile))
        botlib.file_permission(dst_confile, 0o744)
        botlib.file_ownership(dst_confile, 0, 0)

def install_deb_packages():
    # get the linux packages list that need to install to the server
    with open('linux/packages_install.txt') as f:
        lines = f.readlines()
    for line in lines:
        debhandler.install_deb(line)

if __name__ == "__main__":
    os.chdir('/root/orchestrator')
    botlib.git_pull()
    install_deb_packages()
    copy_nginx_file()
    copy_index_php()
