import warnings
import argparse
import FenicsATL as FATL
import pandas as pd

def parse_arguments():
    parser = argparse.ArgumentParser(description='Customize burnsTable and mainDataDir paths.')
    parser.add_argument('--burnsTable', type=str, help='Path to the burns table CSV file.')
    parser.add_argument('--mainDataDir', type=str, help='Path to the main data directory.')

    return parser.parse_args()

if __name__ == '__main__':
    warnings.filterwarnings("ignore")

    args = parse_arguments()

    mainDataDir = args.mainDataDir if args.mainDataDir else "/AtlasDisk/user/FENICS/"
    burnsTable = args.burnsTable if args.burnsTable else '/users/divers/atlas/sisaid/home2/data/burns.csv'

    FENICS = FATL.fen1_data_extractor(mainDataDir, burnsTable)

    FENICS.to_json('/AtlasDisk/home2/sisaid/data/FENICS_data.json')
    print('\n Update: Done')