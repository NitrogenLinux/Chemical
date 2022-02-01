import os, sys

# Check for root
if os.geteuid() != 0:
    exit("You must run chemical as root!")

# Check for internet
if os.system("ping archlinux.org -c 1") != 0:
    exit("You must be connected to the internet to use chemical.")

if os.path.isdir("/sys/firmware/efi/efivars/") == True:
    efi = True;
else:
    efi = False;

if sys.argv[1:]:
    if sys.argv[1] == "atomic":
        atomic = True;
else:
    atomic = False;

def atomic():
    ## TODO: make atomic installer
    print()

def install():
    ## TODO: make regular installer
    print()