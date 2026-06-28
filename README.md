## In this repo...

### Vocab Manager:
All data is organized in a libre office file with several sheets. I use `vocab_manager/ods2csv.py` to create those .csv-files you can find in the `data/` directory.

#### csv2md.py
This file is used to generate vocab-table in markdown format to display for example with Obsidian. The required source is `data/_sheet_vocab.csv`. The column headers you find there can be used for the output configuration in `vocab_manager/util/config.py`. Use the attribute `column_map` for organizing the output information.

Columns with a leading `_` in the name are tag-columns. To get all tags present in the file run:
```
vocab_manager/csv2md.py --mode gettags
```

To generate a markdown file with all vocabulary filtered by tags run:
```
vocab_manager/csv2md.py [<tag1>] [<tag2>] [<...>] --mode generate 
```
Provide the tags **without** the leading `_`.

#### Next Steps
There will be introduced a further data model, that genrates more information to each word, e.g. declinations, example sentences etc. work in progress!

### WIP: Generate Vocab HTML Pages with QR Code

Having a json file like given. Running the Pythonfile with either
 
```python
# render all entries in json file
python render_it.py

# render specific word
python render_it.py --word specific_word
```

The html file with translation and example usage will be generated. And a Qr code will also be generated, pointing to the location where the html file lives in your LAN.

Have Fun!
