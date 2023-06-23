import warnings
import argparse
import FenicsATL as FATL
import pandas as pd
import os

def parse_arguments():
    parser = argparse.ArgumentParser(description='Customize script options.')
    parser.add_argument('--fenicsVersion', type=int, choices=[1, 2], help='Choose the Fenics version (1 or 2).')
    parser.add_argument('--mainDataDir', type=str, help='Path to the main data directory.')
    parser.add_argument('--burnsTable', type=str, help='Path to the burns table CSV file (only for Fenics version 1).')
    parser.add_argument('--saveLocation', type=str, help='Path to the custom save location.')

    return parser.parse_args()

if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    args = parse_arguments()

    if args.fenicsVersion == 1:
        mainDataDir = args.mainDataDir if args.mainDataDir else "/AtlasDisk/user/FENICS/"
        burnsTable = args.burnsTable if args.burnsTable else '/users/divers/atlas/sisaid/home2/data/burns.csv'

        FENICS = FATL.fen1_data_extractor(mainDataDir, burnsTable)
        saveLocation = args.saveLocation if args.saveLocation else '/AtlasDisk/home2/sisaid/data/FENICS_data.json'
        FENICS.to_json(saveLocation)

    elif args.fenicsVersion == 2:
        ans = input('Are you connected to the CERN tunnel? (Y/N): ')

        if ans.upper() == 'N':
            print('Be sure to be connected to the CERN lxtunnel')
        elif ans.upper() == 'Y':
            mainDataDir = args.mainDataDir if args.mainDataDir else "/AtlasDisk/user/tilefen/FENICS2/"

            FENICS2 = FATL.fen2_data_extractor(mainDataDir)
            saveLocation = args.saveLocation if args.saveLocation else '/AtlasDisk/home2/sisaid/data/FENICS2_data.json'
            FENICS2.to_json(saveLocation)

            print('\nUpdate: Done')
        else:
            print('Be sure to be connected to the CERN lxtunnel')
