import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
 
# Step 1: CSV file path and chunk size
csv_file = r'C:\Users\C26707E\Downloads\audit-4L.csv'
chunksize = 10000  # Number of rows per chunk
 
# Step 2: MySQL connection details
username = 'root'
password = 'root'
host = 'localhost'
port = '3306'
database = 'nasevergreeningstatsdb'
table_name = 'auditinputfiles'
 
# Step 3: Create SQLAlchemy engine
engine = create_engine(f'mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database}')
 
# Step 4: Load CSV into MySQL in chunks
try:
    for chunk in pd.read_csv(csv_file, chunksize=chunksize):
        # ✅ Clean column names
        chunk.columns = chunk.columns.str.strip()
 
        # ✅ Clean specific fields to avoid truncation errors
        if 'SrcSubjIdNb' in chunk.columns:
            chunk['SrcSubjIdNb'] = chunk['SrcSubjIdNb'].astype(str).str.strip().str[:10]
           
       
        if 'DinFoundFlag' in chunk.columns:
            chunk['DinFoundFlag'] = chunk['DinFoundFlag'].astype(str).str.strip().str[:1]
           
        if 'ProcessStg' in chunk.columns:
            chunk['ProcessStg'] = chunk['ProcessStg'].astype(str).str.strip().str[:1]

        if 'SequenceNb' in chunk.columns:
            chunk['SequenceNb'] = chunk['SequenceNb'].fillna(0)
 
        if 'AinFromNas' in chunk.columns:
            chunk['AinFromNas'] = pd.to_numeric(chunk['AinFromNas'], errors='coerce').fillna(0)
 
        if 'AinChangeFlag' in chunk.columns:
            chunk['AinChangeFlag'] = chunk['AinChangeFlag'].astype(str).str.strip().str[:1]
 
        if 'ErrorCode' in chunk.columns:
            chunk['ErrorCode'] = chunk['ErrorCode'].astype(str).str.strip().str[:50]

 
        if 'FieldIndicator' in chunk.columns:
            chunk['FieldIndicator'] = chunk['FieldIndicator'].astype(str).str.strip().str[:1]
 
        if 'DinCount' in chunk.columns:
            chunk['DinCount'] = pd.to_numeric(chunk['DinCount'], errors='coerce').fillna(0)
 
        if 'DataProvider' in chunk.columns:
            chunk['DataProvider'] = pd.to_numeric(chunk['DataProvider'], errors='coerce').fillna(0)
 
        if 'PinCount' in chunk.columns:
            chunk['PinCount'] = pd.to_numeric(chunk['PinCount'], errors='coerce').fillna(0)
 
        if 'NonStdLinCount' in chunk.columns:
            chunk['NonStdLinCount'] = pd.to_numeric(chunk['NonStdLinCount'], errors='coerce').fillna(0)
 
        if 'DataProvider' in chunk.columns:
            chunk['DataProvider'] = pd.to_numeric(chunk['DataProvider'].astype(str).str.strip(), errors='coerce').fillna(0).astype(int)
 
        if 'QtyFromNas' in chunk.columns:
            chunk['QtyFromNas'] = chunk['QtyFromNas'].astype(str).str.strip().str[:1]
 
        if 'ErrorCode' in chunk.columns:
            chunk['ErrorCode'] = chunk['ErrorCode'].astype(str).str.strip().str[:10]  # Adjust 10 to match your MySQL column size
 
 
        # ✅ Insert into MySQL
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
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        print(f'📊 Total rows now in {table_name}: {result.scalar()}')
except Exception as e:
    print(f'⚠️ Could not verify row count: {e}')