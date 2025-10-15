#!/usr/bin/env python3
"""
ISO to USB Bootable Drive Creator for macOS
Creates bootable USB drives from ISO files on macOS
"""

import subprocess
import sys
import os
import time
import argparse

def run_command(command, capture_output=True, check=True):
    """Execute shell command and return output"""
    try:
        if capture_output:
            result = subprocess.run(command, shell=True, capture_output=True, text=True, check=check)
            return result.stdout.strip()
        else:
            subprocess.run(command, shell=True, check=check)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        if e.stderr:
            print(f"Error details: {e.stderr}")
        return None

def list_usb_drives():
    """List available USB drives"""
    print("\n📱 Scanning for USB drives...")
    
    # Get disk list
    output = run_command("diskutil list external physical")
    
    if not output:
        print("No external drives found.")
        return None
    
    print("\nAvailable USB drives:")
    print(output)
    
    # Parse disk identifiers
    drives = []
    lines = output.split('\n')
    for line in lines:
        if '/dev/disk' in line and 'external' in line:
            parts = line.split()
            for part in parts:
                if '/dev/disk' in part:
                    drives.append(part)
    
    return drives

def get_drive_info(disk):
    """Get detailed information about a drive"""
    output = run_command(f"diskutil info {disk}")
    if output:
        info = {}
        for line in output.split('\n'):
            if 'Device / Media Name:' in line:
                info['name'] = line.split(':')[1].strip()
            elif 'Disk Size:' in line:
                info['size'] = line.split(':')[1].strip()
        return info
    return None

def unmount_disk(disk):
    """Unmount a disk"""
    print(f"\n🔧 Unmounting {disk}...")
    return run_command(f"diskutil unmountDisk {disk}")

def convert_iso_to_dmg(iso_path):
    """Convert ISO to DMG format for macOS"""
    dmg_path = iso_path.rsplit('.', 1)[0] + '.dmg'
    
    if os.path.exists(dmg_path):
        print(f"DMG already exists at {dmg_path}")
        return dmg_path
    
    print(f"\n🔄 Converting ISO to DMG format...")
    print(f"Source: {iso_path}")
    print(f"Target: {dmg_path}")
    
    cmd = f"hdiutil convert -format UDRW -o '{dmg_path}' '{iso_path}'"
    result = run_command(cmd, capture_output=False)
    
    # macOS might add .dmg extension
    if os.path.exists(dmg_path + '.dmg'):
        os.rename(dmg_path + '.dmg', dmg_path)
    
    if os.path.exists(dmg_path):
        print(f"✅ Conversion complete: {dmg_path}")
        return dmg_path
    else:
        print("❌ Conversion failed")
        return None

def write_to_usb(source_path, target_disk):
    """Write ISO/DMG to USB using dd"""
    print(f"\n📝 Writing to USB drive {target_disk}")
    print("⚠️  This will erase all data on the USB drive!")
    
    # Unmount the disk first
    unmount_disk(target_disk)
    
    # Convert disk identifier to raw disk for faster writing
    raw_disk = target_disk.replace('/dev/disk', '/dev/rdisk')
    
    print(f"\n🚀 Writing image to {raw_disk}...")
    print("This may take several minutes. Please be patient...")
    
    # Use dd to write the image
    cmd = f"sudo dd if='{source_path}' of={raw_disk} bs=1m status=progress"
    
    print(f"Running: {cmd}")
    print("\nYou'll need to enter your admin password:")
    
    try:
        subprocess.run(cmd, shell=True, check=True)
        print("\n✅ Successfully written to USB!")
        
        # Eject the disk
        print("\n🔄 Ejecting disk...")
        run_command(f"diskutil eject {target_disk}", check=False)
        print("✅ USB drive is ready! You can safely remove it.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to write to USB: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Create bootable USB drives from ISO files on macOS',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s /path/to/ubuntu.iso
  %(prog)s -d /dev/disk2 /path/to/windows.iso
  %(prog)s --list  # List available USB drives
        """
    )
    
    parser.add_argument('iso_path', nargs='?', help='Path to ISO file')
    parser.add_argument('-d', '--disk', help='Target disk (e.g., /dev/disk2)')
    parser.add_argument('-l', '--list', action='store_true', help='List available USB drives')
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation prompts')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("🔥 ISO to USB Bootable Drive Creator for macOS")
    print("=" * 60)
    
    # List drives mode
    if args.list:
        list_usb_drives()
        return
    
    # Check if ISO path provided
    if not args.iso_path:
        parser.print_help()
        print("\n❌ Error: Please provide an ISO file path")
        sys.exit(1)
    
    # Verify ISO exists
    if not os.path.exists(args.iso_path):
        print(f"❌ Error: ISO file not found: {args.iso_path}")
        sys.exit(1)
    
    iso_path = os.path.abspath(args.iso_path)
    print(f"\n📀 ISO file: {iso_path}")
    print(f"📊 Size: {os.path.getsize(iso_path) / (1024**3):.2f} GB")
    
    # Get target disk
    if args.disk:
        target_disk = args.disk
    else:
        drives = list_usb_drives()
        if not drives:
            print("\n❌ No USB drives found. Please insert a USB drive and try again.")
            sys.exit(1)
        
        print("\n🎯 Select target USB drive:")
        for i, drive in enumerate(drives, 1):
            info = get_drive_info(drive)
            if info:
                print(f"  {i}. {drive} - {info.get('name', 'Unknown')} ({info.get('size', 'Unknown')})")
            else:
                print(f"  {i}. {drive}")
        
        while True:
            try:
                choice = input("\nEnter number (or 'q' to quit): ").strip()
                if choice.lower() == 'q':
                    print("Cancelled.")
                    sys.exit(0)
                
                idx = int(choice) - 1
                if 0 <= idx < len(drives):
                    target_disk = drives[idx]
                    break
                else:
                    print("Invalid selection. Please try again.")
            except ValueError:
                print("Invalid input. Please enter a number.")
    
    # Show selected drive info
    print(f"\n🎯 Target drive: {target_disk}")
    info = get_drive_info(target_disk)
    if info:
        print(f"   Name: {info.get('name', 'Unknown')}")
        print(f"   Size: {info.get('size', 'Unknown')}")
    
    # Confirmation
    if not args.yes:
        print("\n⚠️  WARNING: This will ERASE ALL DATA on the USB drive!")
        confirm = input("Are you sure you want to continue? (yes/no): ").strip().lower()
        if confirm != 'yes':
            print("Cancelled.")
            sys.exit(0)
    
    # Check if conversion needed
    source_path = iso_path
    if iso_path.lower().endswith('.iso'):
        print("\n🔍 Detected ISO file. Converting to DMG format for macOS...")
        dmg_path = convert_iso_to_dmg(iso_path)
        if dmg_path:
            source_path = dmg_path
        else:
            print("❌ Failed to convert ISO to DMG")
            sys.exit(1)
    
    # Write to USB
    success = write_to_usb(source_path, target_disk)
    
    if success:
        print("\n🎉 Success! Your bootable USB drive is ready!")
        print("📌 You can now use it to boot your computer.")
        print("📌 Remember to change your boot order in BIOS/UEFI if needed.")
    else:
        print("\n❌ Failed to create bootable USB drive.")
        sys.exit(1)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)