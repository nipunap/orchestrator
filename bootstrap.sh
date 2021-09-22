#!/bin/bash
. ./configs

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'
BROWN='\033[0;33m'

# verify configurations
verify_configs(){
	if [ ! -z "$SERVER_IPS" ]; then
		echo "Configurations check [ ${GREEN}OK${NC} ]"
	else
		echo "Configurations check [ ${RED}ERROR${NC} ]"
		echo "Verify SERVER_IPS in configs file"
		exit 1
	fi
}

# install webtools such as nginx and php
install_webtools() {
	echo "${BROWN}Installing webtools${NC}"
	for host in $(echo $SERVER_IPS);
	do
		echo "installing webtools in $host"
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'apt-get --assume-yes update'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'apt-get --assume-yes install nginx-light php7.2-fpm'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'apt-get --assume-yes install python3 git'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'systemctl start nginx'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'systemctl enable nginx'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'systemctl start php7.2-fpm.service'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'systemctl enable php7.2-fpm.service'
		ssh -i ~/.ssh/id_slack_rsa -A root@$host 'pip install git'
	done
}

# setup keyless authentication for ssh
setup_keyless_ssh(){
	echo "${BROWN}Setup keyless authentication${NC}"
	echo "n" | ssh-keygen -q -t rsa -N '' -f ~/.ssh/id_slack_rsa >/dev/null 2>&1
	for host in $(echo $SERVER_IPS);
	do
		 ssh-copy-id -i ~/.ssh/id_slack_rsa.pub -o StrictHostKeyChecking=no root@$host
	done
}

# add a cronjob
set_cronjob(){
	echo "${BROWN}Setup cronjob${NC}"
	#bot cron to run every 30mins
	echo "0-59/2 * * * * python3 /root/orchestrator/bot.py" > /tmp/crons_list
	#install new cron file
	crontab /tmp/crons_list
	rm /tmp/crons_list
}

# get git clone
git_clone(){
	cd /root
	git clone https://github.com/nipunap/orchestrator.git
}

#########
verify_configs
setup_keyless_ssh
install_webtools
git_clone
set_cronjob
