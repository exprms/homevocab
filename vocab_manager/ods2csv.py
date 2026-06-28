#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Mar 23 07:12:53 2025

@author: bernd
"""

import os
import pandas as pd
from dotenv import load_dotenv
import argparse
import util.custom_logger as cl

def convert_ods_to_csv(
        input_file: str, 
        output_file: str, 
        check_col: str = "", 
        sheet_name: str = ""
        ):

    # Read the .ods file
    if sheet_name == "":
        df = pd.read_excel(input_file, engine='odf')
        cl.logger.info("load first sheet")
    else:
        df = pd.read_excel(input_file, engine='odf', sheet_name=sheet_name)
        cl.logger.info(f"load sheet: '{sheet_name}'")

    if check_col != "":
        cl.logger.info(f"check for duplicates in column {check_col}")
        duplicates = df[df.duplicated([check_col], keep=False)].sort_values(by=check_col, ascending=True)

        if not duplicates.empty:
            cl.logger.warning("Found duplicates: -----------------------------------")
            print(duplicates[['id', check_col]])
            cl.logger.warning("-----------------------------------------------------")
        else:
            cl.logger.info("No duplicates found")

    # Write the DataFrame to a .csv file
    df.to_csv(output_file, index=False, sep=';')

    cl.logger.info(f"Created csv file: '{output_file}'")

if __name__ == "__main__":

    # get env variables
    load_dotenv()
    
    # Create the parameter parser
    parser = argparse.ArgumentParser()

    # Add arguments
    #required
    parser.add_argument("sheetname", help="name of ods sheet to parse")

    # optional
    parser.add_argument("--chk", type=str, help="which column to check for duplicates", default="")

    args = parser.parse_args()
    
    # Example usage
    input_file = os.getenv('ODS_SOURCE')
    output_file = 'data/_sheet_' + args.sheetname + '.csv'
    check_col = args.chk
    
    convert_ods_to_csv(
        input_file=input_file, 
        output_file=output_file, 
        check_col=check_col,
        sheet_name=args.sheetname
        )