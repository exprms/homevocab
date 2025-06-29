#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 21 09:13:55 2025

@author: bernd
"""
import hashlib
from pydantic import BaseModel, Field
import os
from dotenv import load_dotenv
import csv
load_dotenv()

class ExportConfig(BaseModel):
    """
    This is the config class for several csv and outpout information:
        column_map: key=csv column name, value=the output markdown colum name
                    columns in this dictionary will be displayed. Add key-value
                    pairs on demand.
        csv_path:   source path of csv
        dest_path:  destination path for the markdown file (e.g. the obsidian vault)
        file_prefix:put this as prefix of the markdown file
        sortby:     data will be sorted A-Z ascending along this column
        tag_prefix: helps to identify tag-columns from the one hot encoded csv
                    e.g.: tag_prefix = "_" --> all column names starting with "_"
                    will be considered as tag column. 
    """
    column_map: dict=Field(
        default={
            "id":"id",
            "right":"neměcký",
            "left":"český",
            "info_left":"info",
            }
        )
    csv_path: str=Field(default=os.getenv('CSV_SOURCE'))
    dest_path: str=Field(default=os.getenv('MD_PATH'))
    file_prefix: str=Field(default='')
    sortby: str=Field(default='left')
    tag_prefix: str=Field(default="")
    
    @property
    def cols(self):
        return list(self.column_map.keys())
    
    @property
    def col_names(self):
        return list(self.column_map.values())
    
class MDTag(BaseModel):
    tags: list[str]
    tag_prefix: str=""
    
    @property
    def sorted(self):
        # remove duplicates
        tmp = list(set([self.tag_prefix + tag for tag in self.tags]))
        return sorted(tmp)
    
    @property
    def displayed(self):
        return [tag.removeprefix(self.tag_prefix) for tag in self.sorted]
    
    @property
    def chksm(self):
        return create_hash_from_tags(self.displayed)
    
    @property
    def yaml_header(self, prefix:str=''):
        yaml_header = f"---\nchksum: {self.chksm}\n"
        if len(self.tags)>0: 
            yaml_header +=  'tags:\n  - ' + '\n  - '.join([f"{prefix}{item}" for item in self.displayed])
        yaml_header += '\n---'
        return yaml_header
    
    @property
    def md_header(self):
        mdh = "## Vocabel \n \nFilter Tags:\n- "
        if len(self.tags)>0: 
            mdh += '\n- '.join(self.displayed) 
        else:
            mdh += '- ALL'
        return mdh
    
    @property
    def tagstring(self):
        return '-'.join(self.displayed)
    
def create_hash_from_tags(tags: list[str]):
    """
    Creates a hash from the given tags to be used as a filename.

    Parameters:
    - tags: list of str, the tags to hash

    Returns:
    - str: a hexadecimal string of the hash
    """
    if tags==[]:
        str2hash = 'no_filter'
    else:
        # Join tags into a single string and encode it
        str2hash = ','.join(sorted(tags))  # Sort to ensure consistent hashing
    
    hash_object = hashlib.md5(str2hash.encode())
    return hash_object.hexdigest()


def get_columns_with_prefix(csv_file:str, prefix:str)->list[str]:
    """
    Open the CSV file and read the first line
    returns all column names wit hgiven prefix
    """
    with open(csv_file, mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=';')
        # Read the first row (header)
        header = next(reader)
        
        # Get columns that start with the specified prefix
        filtered_columns = [column for column in header if column.startswith(prefix)]
        
    return filtered_columns