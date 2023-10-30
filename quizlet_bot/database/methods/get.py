from database.main import connection


def select_not_shared_from_main_library(username: str):
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT word, definition, url
                    FROM main_library
                    WHERE username = '{}' and shared != 'Yes'
            '''.format(username)
            cursor.execute(query)
            row = cursor.fetchall()
            return row
    except Exception as e:
        print(f"An error occurred in def select_not_shared_from_main_library: {str(e)}")


def select_count_words_by_user_not_shared(username: str):
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT COUNT(username)
                    FROM main_library
                    WHERE username = '{}' and shared = 'No'

            '''.format(username)
            cursor.execute(query)
            row = cursor.fetchall()
            return row[0][0]
    except Exception as e:
        print(f"An error occurred in def select_count_words_by_user_not_shared: {str(e)}")


def select_count_words_by_user_shared(username: str):
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT COUNT(username)
                    FROM main_library
                    WHERE username = '{}' and shared = 'Yes'

            '''.format(username)
            cursor.execute(query)
            row = cursor.fetchall()
            return row[0][0]
    except Exception as e:
        print(f"An error occurred in def select_count_words_by_user_shared: {str(e)}")


def select_shared_from_main_library():
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT word, definition, url
                    FROM main_library
                    WHERE shared = 'Yes'
            '''
            cursor.execute(query)
            row = cursor.fetchall()
            return row
    except Exception as e:
        print(f"An error occurred in def select_shared_from_main_library: {str(e)}")


def select_authors_and_words():
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT username, word
                    FROM main_library
                    WHERE shared = 'Yes'
            '''
            cursor.execute(query)
            row = cursor.fetchall()
            return row
    except Exception as e:
        print(f"An error occurred in def select_authors_and_words: {str(e)}")


# Можно добавить лимит, в будущем, если будет много комментов
def select_from_swag_comments():
    try:
        with connection.cursor() as cursor:
            query = '''
                 SELECT username, comment
                    FROM swag
            '''
            cursor.execute(query)
            row = cursor.fetchall()
            return row
    except Exception as e:
        print(f"An error occurred in def select_authors_and_words: {str(e)}")