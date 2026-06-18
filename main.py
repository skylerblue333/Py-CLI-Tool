import argparse
import sys
import os
import platform

def get_sys_info():
    return {
        "OS": platform.system(),
        "Release": platform.release(),
        "Python": platform.python_version(),
        "CWD": os.getcwd()
    }

def main():
    parser = argparse.ArgumentParser(description="Advanced System Administration CLI")
    parser.add_argument('--info', action='store_true', help='Display system information')
    parser.add_argument('--ping', type=str, help='Mock ping a host')
    
    args = parser.parse_args()
    
    if args.info:
        info = get_sys_info()
        print("--- System Information ---")
        for k, v in info.items():
            print(f"{k}: {v}")
    elif args.ping:
        print(f"Pinging {args.ping}...")
        print(f"Reply from {args.ping}: bytes=32 time=14ms TTL=54")
    else:
        parser.print_help()

if __name__ == "__main__":
    # If run without args, simulate running with --info for demonstration
    if len(sys.argv) == 1:
        sys.argv.append('--info')
    main()