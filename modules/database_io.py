import os
import csv

#So users don't have to worry about file paths, we can set up a base directory for our data files. 
#This way, we can easily read from and write to our CSV files without hardcoding the paths every time.
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
data_dir = os.path.join(project_root, 'data')
 
#Maps
#for easy access to the file paths
FILES ={"students": os.path.join(data_dir, 'students.csv'),
        "colleges": os.path.join(data_dir, 'colleges.csv'),
        "programs": os.path.join(data_dir, 'programs.csv')}

#Schema headers for each CSV file, which will be useful when reading and writing data to ensure consistency.
Headers = {"students": ['id', 'firstname', 'lastname', 'program_code', 'year', 'gender'],
           "colleges": ['code', 'name'],
           "programs": ['code', 'name', 'college_code']}


def initialize_storage():
    #if the data directory doesn't exist, create it
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    #for each file in our FILES mapping, check if it exists. If not, create it and write the header row.
    for key, file_path in FILES.items():
        if not os.path.exists(file_path):
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(Headers[key])

#CRUD functions
 
def read_csv(file_key):
    file_path = FILES[file_key]
    data = []
    with open(file_path, 'r', newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append(row)
    return data

def write_csv(file_key, data):
    file_path = FILES[file_key]
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=Headers[file_key])
        writer.writeheader()
        for row in data:
            writer.writerow(row)


def search_csv(file_key, search_query, column=None):
       data = read_csv(file_key)
       search_query = search_query.lower()
       results =[]
       for row in data:
            if column:
                if search_query in str(row[column]).lower():
                 results.append(row)
            else:
                if any(search_query in str(val).lower() for val in row.values()):
                 results.append(row)
                
       return results

def delete_csv(file_key, id_value, id_column='id'): # Default to 'id' for students
    data = read_csv(file_key)
    updated_data = []

    for row in data:
        # If the current row's ID is NOT the one we want to delete, keep it
        if row[id_column] != id_value:
            updated_data.append(row)
            
    # Save the NEW list (the one missing the deleted row)
    write_csv(file_key, updated_data) 
    return updated_data

def update_csv(file_key, id_value,updated_row, id_column='id' ):
    data = read_csv(file_key)
    new_list=[]

    for row in data:
        if row[id_column] == id_value:
            new_list.append(updated_row)
        else:
            new_list.append(row)
    write_csv(file_key, new_list)
    return new_list

def sort(file_key, sort_by_column, reverse=False):
    data=read_csv(file_key)
    return sorted(data, key=lambda x: x[sort_by_column].lower(),reverse=reverse)
    