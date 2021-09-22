import os
import git

def file_permission(file, permission, owner):
    # change file permission
    os.chmod(file, permission)

def file_ownership(file, owner, group):
    #change ownership of the file
    os.chown(file, owner, group)

def restart_service(service):
    # restart service
    os.system("systemctl restart " + service)

def git_pull():
    bot_home = '/root/orchestrator'
    g = git.cmd.Git(bot_home)
    g.checkout('main')
    g.pull()
