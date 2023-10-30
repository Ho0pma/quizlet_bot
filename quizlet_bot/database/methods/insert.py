from database.main import connection


def insert_into_main_library(username: str, word: str, definition: str, url: str, shared='No'):
    try:
        with connection.cursor() as cursor:
            query = '''
                INSERT INTO main_library (username, word, definition, url, shared)
                VALUES(%s,%s,%s,%s,%s)
            '''
            cursor.execute(query, (username, word, definition, url, shared))
            connection.commit()
    except Exception as e:
        print(f"An error occurred in def insert_into_main_library: {str(e)}")


def insert_into_swag(username: str, comment: str):
    try:
        with connection.cursor() as cursor:
            query = '''
                INSERT INTO swag (username, comment)
                VALUES(%s,%s)
            '''
            cursor.execute(query, (username, comment))
            connection.commit()
    except Exception as e:
        print(f"An error occurred in def insert_into_main_library: {str(e)}")