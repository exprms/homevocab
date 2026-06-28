import pandas as pd

# Database:
data_base = [
    'data/_sheet_declinations.csv',
    'data/_sheet_sentences.csv',
    'data/_sheet_verbs_past.csv',
    'data/_sheet_verbs_present.csv',
    'data/_sheet_vocab.csv',
]

# Replace 'your_file.csv' with the path to your CSV file
df = pd.read_csv('your_file.csv')

# Display the first few rows
print(df.head())
