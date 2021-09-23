# Orchestrator

Orchestrator is a tool to manage remote linux servers. Management happen via the github.
```
                        ------------
          +---------->  |  Github  |
          |             ------------
  +-------------+           |
  | User laptop |           |      +-----------+
  +-------------+           |----> | Server 1  |
                            |      +-----------+
                            |      +-----------+
                            +----> | Server 2  |
                                   +-----------+          
```
## How to setup ?

Clone this repo to your laptop
```
git clone https://github.com/nipunap/orchestrator.git
```

Next step is, add server IPs to `SERVER_IPS="54.242.46.111 54.87.16.101"` in _configs_ file. Then run _bootstrap.sh_ file
in order to bootstrap the linux packages and github clone. Use following command to bootstrap from your laptop command prompt. It will prompt remote server root password for one time.
```
sh bootstrap.sh
```

## What happen after bootstrap ?

Bootstrap script automatically install required linux packages and git clone the repository to each server node.
Also it is adding a cronjob for _bot.py_ file to execute every 30mins.

Every run of _bot.py_ script will install packages defined in _package_install.txt_ file and also if there is a config file change
automatically copying to `nginx` configuration folder.

## Features

- Change NGINX config file remotely in many server nodes
  Merge a PR to main branch with new changes in _nginx/default.nginx_ file.
- Change the webapp in index.php
  Merge a PR to main branch with new changes in _nginx/index.php_ file.
- Set file permissions
  File permissions can set using following lines. Refer _bot.py_ file for more details.
  ```
  botlib.file_permission(dst_confile, 0o744)
  botlib.file_ownership(dst_confile, 0, 0)
  ```
- Install Debian packages from remotely
  Software packages that required to install to remote servers, need to define in _linux/packages_install.txt_ file.
