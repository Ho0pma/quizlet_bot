from database.main import connection


def delete_word_from_main_library(username: str, word: str):
    try:
        with connection.cursor() as cursor:
            query = '''
                 DELETE 
                    FROM main_library
                    WHERE username = %s and word = %s
                    RETURNING *;
            '''
            cursor.execute(query, (username, word))
            connection.commit()
            deleted_rows = cursor.fetchall()
            return deleted_rows[0]
    except Exception as e:
        print(f"An error occurred in def delete_word_from_main_library: {str(e)}")