import platform
import os

yn = "(y/n)"

def installer():
    # disk
    print("disks:\n")
    os.system("lsblk")
    drive_input = input("enter target drive (e.g. sda): ").strip()
    drive = f"/dev/{drive_input}"
    os.system(f"cfdisk {drive}")
    
    root_input = input("enter root partition (e.g. sda2): ").strip()
    root_part = f"/dev/{root_input}"
    efi_input = input("enter EFI partition (e.g. sda1): ").strip()
    efi_part = f"/dev/{efi_input}"
    
    os.system(f"mkfs.ext4 {root_part}")
    os.system(f"mkfs.fat -F32 {efi_part}")
    os.system(f"mount {root_part} /mnt")
    os.system(f"mount --mkdir {efi_part} /mnt/boot")
    print("disks partitioned, formatted, and mounted successfully!")
    
    # base system
    print("installing base system...")
    os.system("pacstrap /mnt base linux linux-firmware --noconfirm")
    os.system("genfstab -U /mnt >> /mnt/etc/fstab")
    
    # user
    username = input("enter new username: ").strip()
    os.system(f"arch-chroot /mnt useradd -m -G wheel -s /bin/zsh {username}")
    print(f"set password for {username}:")
    os.system(f"arch-chroot /mnt passwd {username}")
    
    # GRUB bootloader
    print("installing GRUB bootloader...")
    os.system("arch-chroot /mnt pacman -S grub efibootmgr --noconfirm")
    os.system("arch-chroot /mnt grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=GRUB --removable")
    os.system("arch-chroot /mnt grub-mkconfig -o /boot/grub/grub.cfg")
    print("GRUB installed successfully!")
    
    # sudo group
    os.system("sed -i 's/^# %wheel ALL=(ALL:ALL) ALL/%wheel ALL=(ALL:ALL) ALL/' /mnt/etc/sudoers")
    
    # os name
    os_release_content = """NAME="Olinux"
ID="olinux"
ID_LIKE="arch"
BUILD_ID="rolling"
ANSI_COLOR="38,2,23,147,209"
HOME_URL="https://github.com/userzzz322/olinux"
DOCUMENTATION_URL="https://wiki.arch-linux.org"
SUPPORT_URL="https://bbs.arch-linux.org"
BUG_REPORT_URL="https://github.com/userzzz322/olinux"
LOGO="linuxfromscratch"
"""
    with open("/mnt/etc/os-release", "w") as f:
        f.write(os_release_content)
    print("OS identity set to Olinux!")
    
    # packages
    print("write what packages you want to install")
    packagesINPUT = input()
    os.system(f"arch-chroot /mnt pacman -Syu {packagesINPUT} --noconfirm")
    
    # desktop
    print("would you like to install XFCE desktop?")
    print(yn)
    desktopINPUT = input()
    if desktopINPUT == "y":
        os.system("arch-chroot /mnt pacman -S xfce4 xfce4-goodies lightdm lightdm-gtk-greeter --noconfirm")
        os.system("arch-chroot /mnt systemctl enable lightdm")
    elif desktopINPUT == "n":
        pass
    
    # xfce/desktop pre-installed
    print("would you like to pre-install some things?")
    print("zsh; xfce4-terminal; dolphin; git; firefox; vim; base-devel; make")
    print(yn)
    select1INPUT = input()
    if select1INPUT == "y":
        os.system("arch-chroot /mnt pacman -S zsh xfce4-terminal dolphin git firefox vim base-devel make --noconfirm")
    elif select1INPUT == "n":
        pass
    
    # end
    print("""                                    ...                                    
                          .......................                          
                     .................................                     
                  ............               ............                  
               .........                           .........               
             ........                                 ........             
           .......                                       .......           
          ......                                           ......          
        ......                                               ......        
       .....                                                   .....       
      .....                                                     .....      
     .....                                                       .....     
    .....                                                         .....    
   .....                                                           .....   
  .....                                                             .....  
  .....                                                             .....  
  ....                                                               ..... 
 .....                                                               ..... 
 ....                                                                 .... 
 ....                                                                 .... 
 ....                                                                 .... 
 ....                                                                 .... 
 ....                                                                 .... 
 .....                                                               ..... 
 .....                                                               ..... 
  .....                                                             .....  
  .....                                                             .....  
   .....                                                           .....   
    .....                                                         .....    
     .....                                                       .....     
      .....                                                     .....      
       .....                                                   .....       
        ......                                               ......        
         .......                                           .......         
           .......                                       .......           
             ........                                  .......             
               .........                           .........               
                  ...........                 ...........                  
                     .................................                     
                         .........................                         
                                  .......                                  """)
    
    print("install ended!")
    print("welcome to matrix!")

print("starting installer")
installer()
