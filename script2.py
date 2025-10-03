import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
 
# Step 1: CSV file path and chunk size
csv_file = r'C:\Users\C26203E\Documents\fil\dininput.csv'  # Update with your actual path
chunksize = 10000  # Number of rows per chunk
 
# Step 2: MySQL connection details
username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'nasevergreen'
table_name = 'dininputrecords'
 
# Step 3: Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
 
# Step 4: Load CSV into MySQL in chunks
try:
    for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        # Optional: Clean or cast data types here
        # chunk = chunk.astype({'column_name': 'str'})  # Example
 
        chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f'✅ Inserted {len(chunk)} rows into {table_name}')
except SQLAlchemyError as db_err:
    print(f'❌ Database error: {db_err}')
except FileNotFoundError:
    print(f'❌ CSV file not found at: {csv_file}')
except Exception as e:
    print(f'❌ Unexpected error: {e}')
 
# Step 5: Optional row count check
try:
    with engine.connect() as conn:
        result = conn.execute(f"SELECT COUNT(*) FROM {table_name}")
        print(f'📊 Total rows now in {table_name}: {result.scalar()}')
except Exception as e:
    print(f'⚠️ Could not verify row count: {e}')