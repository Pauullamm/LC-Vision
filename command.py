import psycopg2
from config import load_config

def command():
    commands = """
                CREATE TABLE Profiles (
                id SERIAL PRIMARY KEY,
                first_name VARCHAR(255),
                last_name VARCHAR(255),
                email VARCHAR(255),
                gender CHAR(255),
                user_id VARCHAR(255),
                username VARCHAR(255),
                birthdate VARCHAR(255),
                location VARCHAR(255),
                bio TEXT,
                profile_pic VARCHAR(255),
                followers_count INT,
                is_verified BOOL,
                interests TEXT
                );
                """
    try:
        config = load_config()
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                # Split the string into separate SQL commands
                commands = commands.split(";")

                # Execute each command
                for command in commands:
                    if command.strip():  # Skip empty lines
                        cur.execute(command.strip())
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

if __name__ == '__main__':
    command()