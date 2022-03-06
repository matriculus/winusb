#!bin/bash
echo "Starting..."
echo ""
echo "Installing wintools..."
sudo apt install wimtools -y
echo "wintools installed successfully!"
echo ""
echo "Mounting Windows Media ISO file @ /media/iso..."
sudo mkdir /media/iso && sudo mount -o loop $1 /media/iso
echo "Mounting completed successfully!"
echo ""
echo "Copying main installation file for partitioning..."
scp -v /media/iso/sources/install.wim ~/Downloads
echo "Copying completed successfully!"
echo ""
echo "Splitting the installation for FAT32 partition..."
wimlib-imagex split install.wim install.swm 4000
echo "Splitting completed sccessfully!"
echo ""
echo "Copying the ISO contents to USB"
rsync -avr --exclude='sources/install.wim' /media/iso/ $2
scp -v install*swm $2/sources/
echo "Copying completed successfully!"
echo ""
echo "Cleaning up..."
sudo umount /media/iso
sudo rmdir /media/iso
rm -f install.wim install*.swm
echo "Bootable USB creation successful!"
echo "Enjoy!"
echo "Please give a star to github.com/matriculus/winusb !"
echo "Thank you!"