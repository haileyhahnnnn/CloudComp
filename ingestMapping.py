import pandas as pd 
import logging 
from google.cloud import bigquery 
from google.cloud import biguery 
from google.cloud.exceptions import GoogleCloudError 

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s') 

def load_CSV(filepath):
  try:
    return pd.read_csv(file_path) 
  except FileNoteFoundError: ""
  except pd.errors.EmptyDataError: 
    logging.error(f"No data found in file: {file_path}")   
    return pd.DataFrame()
  except pd.errors.ParseError: 
    logging.error(f"Error parsing the file: {file_path}")
    return pd.DataFrame()

def parse_corrections): 
  operations.append({
    'field': 'None', 
    'operation': 'None',
    'details' : 'None', 
  }

  operations.append(operation) 
                    
return operations

def save_to_bigquery(df, dataset_id, table_id, project_id):
  try: 
      df.to_gbq(f'{dataset_id}.{table_id}', project_id=project_id, if_exsists='replace')
    logging.info(f"Data successfully loaded to BQ table {dataset_id}.{table_id}")
except GoogleCloudError as e: 
  logging.error(f"Failed to load data into BQ: {e}")
except Exception as e: 
  logging.error(f"Unexpected error: {e}")

def main():
  ingestedForm1_path = '/home/hhahn/igestionFile1Sample.csv'
  ingestedForm2_path = '/home/hhahn/ingestionFile2Sample.csv'

  ingestedForm1 = load_csv(ingestedForm1)
  ingestedForm2 = load_csv(ingestedForm2)

if ingestedform2.empty:
  logging.error("ingestedForm2 DataFrame is empy. Exiting.")
  return

ingestedForm2['changeValue'] = ingestedForm2['changeValue'].astype(str)

changeValue_expanded = pd.json_normalize(parse_changeValue(ingestedForm2['changeValue']))
ingestedValue = pd.concat([ingestedForm2, changeValue_expanded], axis=1)

output_file = "parsed_changedValue_ingestedForm2.csv"
ingestedValue.to_csv(output_file, index=False)
logging.info(f"Parsed correcgtions saved to {output_file}")

project_id = 'hhahn_project'
dataset_id = 'changedValue_mapping_dataset'
table_id = 'changedValue_mapping_table'
save_to_bigwuery(ingestedForm1, dataset_id, table_id, project_id)

if_name_ == "__main__":
  main()

