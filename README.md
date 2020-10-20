sudo apt install samba samba-common git vim tmux python3-pip net-tools -y
mkdir -p ~/workspace/github
mkdir -p ~/workspace/share
sudo chmod -R 777 ~/workspace/
sudo smbpasswd -a test
scp test@192.168.2.3:/etc/samba/smb.conf /tmp/
sudo cp /tmp/smb.conf /etc/samba/smb.conf

ssh-keygen -t rsa -C
git config --global user.name
git config --global user.email

