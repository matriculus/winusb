#!bin/bash
cd ~/Downloads
sudo apt install wimtools -y
sudo mkdir /media/iso && sudo mount -o loop $1 /media/iso
scp /media/iso/sources/install.wim ~/Downloads
wimlib-imagex split install.wim install.swm 4000
rsync -avr --exclude='sources/install.wim' /media/iso/ $2/
scp install*swm $2/sources/
sudo umount /media/iso
sudo rmdir /media/iso
rm -f install.wim install*.swm
