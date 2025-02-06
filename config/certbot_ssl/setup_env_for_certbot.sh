#!/bin/bash 

echo 
echo -e "\u001b[33m EDIT \$DOMAIN and \$EMAIL First \u001b[0m"
echo 

exit


# example: your-email@mail.com
EMAIL="email@example.com" 
# example sandbox.example.com 
DOMAIN="www.example.com"
CERT_CONF=${HOME}/certbot/conf
CERT_WWW=${HOME}/certbot/www

echo "CHECKING CERT_EAIML"
if [[ ${CERT_EMAIL:-"unset"} == "unset" ]]; then
    echo "\$CERT_EMAIL not set"
    echo "setting \$CERT_EMAIL=$EMAIL"
    echo "export CERT_EMAIL=${EMAIL}" >> ~/.bashrc

else
    echo "\$CERT_EMAIL=${CERT_EMAIL}"
fi

echo "CHECKING CERT_DOMAIN"
if [[ ${CERT_DOMAIN:-"unset"} == "unset" ]]; then
    echo "\$CERT_DOMAIN not set"
    echo "setting \$CERT_DOMAIN=$DOMAIN"
    echo "export CERT_DOMAIN=$DOMAIN" >> ~/.bashrc
else
    echo "\$CERT_DOMAIN=${CERT_DOMAIN}"
fi

echo "CHECKING CERT_CONF"
if [ ! -d "${CERT_CONF}" ]; then
    echo "${CERT_CONF} not exists" echo "Creating...."
    mkdir -p ${CERT_CONF} \
        && echo "export CERT_CONF=${CERT_CONF}" >> ~/.bashrc \
        && echo `ls ${CERT_CONF}`
else 
    echo "${CERT_CONF} existed"
fi


echo "CHECKING CERT_WWW"
if [ ! -d "${CERT_WWW}" ]; then
    echo "${CERT_WWW} not exists"
    echo "creating ...."
    mkdir -p ${CERT_WWW} \
        && echo "export CERT_WWW=${CERT_WWW}" >> ~/.bashrc \
        && echo `ls ${CERT_WWW}` 
else
    echo "${CERT_WWW} existed"
fi

echo "checking if group docker exists..."
if [ $(getent group docker) ]; then
    echo "group docker exists, check if $USER in the gorup... "
    if [ $(getent group docker | grep `echo $USER`) ]; then
        echo "$USER is in group docker ... "
    else
        echo "adding $USER to the group ... "
        sudo usermod -aG docker $USER
    fi
else
    echo "creating group docker and adding $USER to it..."
    sudo groupadd docker && sudo usermod -aG docker $USER
    echo "Finished adding $USER to group docker "
fi

#
# the source ~/.bashrc won't work if the script is not run in interactive mode
#
# source ~/.bashrc && echo "\$CERT_EMAIL=${CERT_EMAIL}" && echo "\$CERT_DOMAIN=${CERT_DOMAIN}"
#

echo 
echo -e "\u001b[33m run source ~/.bashrc to make \$CERT_EMAIL and \$CERT_DOMAIN available \u001b[0m"
echo 