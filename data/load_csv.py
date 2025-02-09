import csv

def load_schema_from_csv(file_path):
    schema = {}
    print(f'load_csv.csv uses {file_path}')
    with open(file_path, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            table_name = row['table_name']
            column_name = row['column_name']
            data_type = row['data_type']
            
            if table_name not in schema:
                schema[table_name] = []
            
            schema[table_name].append({
                'column_name': column_name,
                'data_type': data_type
            })
    return schema
