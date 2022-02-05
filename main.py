import os
import sys
from subprocess import Popen

# Check for root
if os.geteuid() != 0:
    exit("You must run chemical as root!")

# Check for internet
if os.system("ping archlinux.org -c 1") != 0:
    exit("You must be connected to the internet to use chemical.")

if os.path.isdir("/sys/firmware/efi/efivars/") is True:
    efi = True
else:
    efi = False

if sys.argv[1:]:
    if sys.argv[1] == "atomic":
        atomic = True
else:
    atomic = False


def atomic():
    # TODO: make atomic installer
    print()


def install():
    # TODO: make regular installer

    os.system("clear")
    print("Welcome to Nitrogen Installer!")
    print()
    print("Partition Disks")
    print("Which disk would you like to use?")
    os.system("lsblk -d")
    disk = input("/dev/")
    os.system("cfdisk /dev/" + disk)

    def im_sure_the_partitions_are_right():
        os.system("lsblk /dev/" + disk)
        print("Are you sure the partitions are correctly created?")
        sure = input("Y/n ")
        if sure in ["y", "Y", "yes", "yeah"]:
            pass
        elif sure in ["n", "N", "no", "nope"]:
            im_sure_the_partitions_are_right()
        else:
            print(sure + ": Command not understood")
            im_sure_the_partitions_are_right()
    im_sure_the_partitions_are_right()

    print("Formatting partitions")
    print("Select root partition")
    root = input("/dev/" + disk)
    print("Select swap(empty for none)")
    swap = input("/dev/" + disk)

    if efi is True:
        print("Select EFI Partition")
        efi_part = input("/dev/" + disk)

    print("Are you sure you want to continue? Continuing will remove every file 
            from the selected partitions.")
    removal_prompt = input("Y/n ")

    if removal_prompt == "n":
        sys.exit(1)
    else:
        pass

    os.system("mkfs.btrfs -f /dev/" + disk + root)

    if len(swap) != 0:
        os.system("mkswap /dev/" + disk + swap)

    if efi is True:
        os.system("mkfs.vfat -F32 /dev/" + disk + efi_part)

    print("Mounting file systems")
    os.system("mount /dev/" + disk + root + " /mnt")
    os.system("swapon -a")
    if efi is True: 
        os.system("mkdir /mnt/boot")
        os.system("mount /dev/" + disk + efi_part + " /mnt/boot")

    print("Installing Nitrogen Base")
    os.system("pacstrap /mnt base linux-lts linux-firmware base-devel sof-firmware python")
    os.system("genfstab -U /mnt >> /mnt/etc/fstab")
    print("Configuring Nitrogen")
    print("Select Region")
    os.system("ls /mnt/usr/share/zoneinfo/")
    region = input("Region: ")
    print("Select City")
    os.system("ls /mnt/usr/share/zoneinfo/" + region)
    city = input("City: ")
    os.system("ln -s /mnt/usr/share/zoneinfo/" + region + "/" + city)
    os.system("echo LANG=en_US.UTF-8 >> /mnt/etc/locale.conf")    
    os.system("echo 'en_US.UTF-8 UTF-8' >> /mnt/etc/locale.gen")
    os.system("arch-chroot /mnt/ locale-gen")
    os.system("arch-chroot /mnt/ hwclock --systohc")

    print("Select hostname(empty for default)")
    hostname = input("Hostname: ")
    if len(hostname) == 0:
        os.system("echo nitrogen > /mnt/etc/hostname")

    print("Password for root")
    def set_root_password():
        root_passwd = input("password: ")
        confirm_root_passwd = input("again: ")
        if root_passwd == confirm_root_passwd:
            root_passwd_change = Popen(['arch-chroot', '/mnt/' ,'/usr/bin/passwd', 'root', '--stdin'])
            root_passwd_chang.communicate(root_passwd)

        else:
            print("Passwords do not match!")
            set_root_password()

    print("Creating a user")
    username = input("New user's name: ")
    os.system("arch-chroot /mnt/ useradd -m -G wheel " + username)
    def set_user_passwd():
        user_password = input("New user's password: ")
        confirm_user_passwd = input("again: ")
        if user_password == confirm_user_passwd:
            user_change_password = Popen(['arch-chroot', '/mnt/', '/usr/bin/passwd', username, '--stdin'])
            user_change_password.communicate(user_password)
        else:
            print("Passwords do not match!")
            set_user_passwd()
    os.system("pacstrap /mnt grub")
    print("Installing Boot Loader")
    if efi is True:
        # TODO: add efi grub installer
        os.system("arch-chroot /mnt/ grub-install --target=x86_64-efi --efi-directory=/boot --bootloader-id=Nitrogen")
    else:
        os.system("arch-chroot /mnt/ grub-install --target=i386-pc /dev/" + disk)
    os.system("arch-chroot /mnt/ grub-mkconfig -o /boot/grub/grub.cfg")
    


# Run Chemical with either atomic installer or normal installer.
if atomic is True:
    atomic()
else:
    install()
