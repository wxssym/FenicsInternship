
import argparse

def commands():
    parser = argparse.ArgumentParser(prog='FenicsATL')
    parser.add_argument('--version', action='version', version='FenicsATL 1.0.2')
    # Add more command-line arguments as needed

    args = parser.parse_args()

    # Handle different commands based on the arguments
    if args.version:
        print('FenicsATL version 1.0.2')
    # Add more command handlers based on the arguments

if __name__ == '__main__':
    commands()