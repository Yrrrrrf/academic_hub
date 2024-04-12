import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError

from src.main import app

def setup_database(db_url: str, sql_directory: str = './sql'):
    """
    Set up the database by executing SQL scripts in a specified directory in numerical order.
    
    :param db_url: Database connection URL.
    :param sql_directory: Directory containing SQL scripts.
    """
    engine = create_engine(db_url)
    sql_files = sorted(
        [f for f in os.listdir(sql_directory) if f.endswith('.sql')],
        key=lambda x: int(x.split('_')[0])
    )
    

    print(f"Database URL: {db_url}")
    print(f"Found {len(sql_files)} SQL scripts in '{sql_directory}'.")
    
    print("\nExecuting SQL scripts...")


    for filename in sql_files:
        print(f"Executing '{filename}'...")
        filepath = os.path.join(sql_directory, filename)
        with open(filepath, 'r', encoding='utf-8') as file:
            sql_script = file.read()
            try:
                with engine.begin() as connection:
                    connection.execute(sql_script)
                print(f"\033[92mExecuted '{filename}' successfully.\033[0m")
            except SQLAlchemyError as e:
                print(f"\033[91mError executing '{filename}': {e}\033[0m")
                break  # Stop if any SQL fails


@app.on_event("startup")
def startup_event():
    db_url = "postgresql://user:password@localhost/yourdb"
    setup_database(db_url)
    print("Database setup completed.")

# Define your API routes here
