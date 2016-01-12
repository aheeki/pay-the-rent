echo "Venmo Username:" && read username
echo "Venmo Password:" && read password

if [ -n "$username" ] && [ -n "$password" ]; then
    echo "export VENMO_USER=$username" >> /root/.bash_profile
    echo "export VENMO_PASS=$password" >> /root/.bash_profile
    source /root/.bash_profile

    apt-get update
    apt-get install -y python-dev
    apt-get install -y python-pip
    pip install requests logging beautifulsoup4 apscheduler

    nohup python pay-the-rent.py &

else
    echo "Set username and password to continue"
fi