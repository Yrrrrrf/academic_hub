import os
from setuptools import setup, find_packages, Command
from sqlalchemy import create_engine

# todo: test this setup file
# todo: add the sql files to the sql folder

class CreateDatabase(Command):
    """Setuptools Command class to execute SQL scripts for database schema creation."""
    description = "Create the database schema from SQL files."
    user_options = []  # Required by the Command interface

    def initialize_options(self):
        """Set default values for options."""
        pass

    def finalize_options(self):
        """Post-process options."""
        pass

    def run(self):
        """Run command to execute the SQL scripts that setup the database schema."""
        engine = create_engine('postgresql://user:password@localhost/dbname')
        sql_path = 'sql/'  # Directory where SQL files are stored
        for script in os.listdir(sql_path):
            if script.endswith('.sql'):
                with open(os.path.join(sql_path, script), 'r') as file:
                    sql_command = file.read()
                    engine.execute(sql_command)  # Execute SQL script
        print("Database schema created successfully.")

setup(
    name='YourProject',
    version='0.1.0',
    packages=find_packages(),
    cmdclass={
        'create_db': CreateDatabase  # Add custom command to setuptools
    },
)
