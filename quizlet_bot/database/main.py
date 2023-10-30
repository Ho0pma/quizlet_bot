import psycopg2

def connect_to_database():
    try:
        with psycopg2.connect(
            database='quizlet_db',
            user='user',
            password='pass',
            host='db',  # имя сервиса в docker-compose
            port='5432'
        ) as connect:
            print("Database opened successfully")
            return connect
    except Exception as e:
        print(f"An error occurred in def connect_to_database: {str(e)}")

connection = connect_to_database()


# КАК СОЗДАТЬ КОНТЕЙНЕР С ПОСТГРЕСОМ И ПОДКЛЮЧИТЬСЯ К НЕМУ
# docker run -e POSTGRES_USER=user -e POSTGRES_PASSWORD=pass --name quizlet_db -v my_volume:/var/lib/postgresql/data -d -p 5432:5432 postgres