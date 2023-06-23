import warnings
import argparse
import FenicsATL as FATL
import pandas as pd
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Customize mainDataDir path.')
    parser.add_argument('--mainDataDir', type=str, help='Path to the main data directory.')

    return parser.parse_args()

if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    args = parse_arguments()

    ans = input('Are you connected to CERN tunnel? Y/N: ')

    if ans.upper() == 'N':
        print('Be sure to be connected to CERN lxtunnel')
    elif ans.upper() == 'Y':
        mainDataDir = args.mainDataDir if args.mainDataDir else "/AtlasDisk/user/tilefen/FENICS2/"
        FENICS2 = FATL.fen2_data_extractor(mainDataDir, os.listdir(mainDataDir))
        FENICS2.to_json('/AtlasDisk/home2/sisaid/data/FENICS2_data.json')
        print('\n Update: Done')
    else:
        print('Be sure to be connected to CERN lxtunnel')