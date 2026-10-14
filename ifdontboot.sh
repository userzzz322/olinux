mount /dev/sda2 /mnt
mount /dev/sda1 /mnt/boot
arch-chroot /mnt
grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --removable
grub-mkconfig -o /boot/grub/grub.cfg
exit
reboot