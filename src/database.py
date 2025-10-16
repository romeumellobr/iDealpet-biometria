import psycopg2

class DB:
    def __init__(self, config):
        self.conn = psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD
        )

    def execute(self, query, params=None):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()
                else:
                    self.conn.commit()
                    return None
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao executar a consulta: {e}")
            return None

    def close(self):
        if self.conn:
            self.conn.close()

    def fetch_dogs_from_database(self):
        try:
            query = "SELECT * FROM dogs"
            return self.execute(query) or []
        except Exception as e:
            print(f"Erro ao buscar dados dos cães: {e}")
            return []

    def insert_dog(self, dog_name, feature_vector, image_url):
        try:
            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO public.dogs (dog_name, feature_vector, image_path, created_at)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP) RETURNING dog_id;
                """
                cursor.execute(query, (dog_name, feature_vector, image_url))
                dog_id = cursor.fetchone()[0]
                self.conn.commit()
                return dog_id
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir cachorro: {e}")
            return None

    def insert_dog1(self, dog_name, feature_vector, image_url):
        try:
            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO public.dogs (dog_name, feature_vector, image_path, created_at, is_registered)
                VALUES (%s, %s, %s, CURRENT_TIMESTAMP, FALSE) RETURNING dog_id;
                """
                cursor.execute(query, (dog_name, feature_vector, image_url))
                dog_id = cursor.fetchone()[0]
                self.conn.commit()
                return dog_id
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir cachorro: {e}")
            return None

    def get_saved_features(self):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT dog_id, feature_vector FROM public.dogs;")
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar características salvas: {e}")
            return []

    def get_dog_features(self, dog_id):
        try:
            with self.conn.cursor() as cursor:
                cursor.execute("SELECT * FROM dogs WHERE dog_id = %s;", (dog_id,))
                return cursor.fetchall()
        except Exception as e:
            print(f"Erro ao buscar características salvas: {e}")
            return []

    def save_features_to_db(self, dog_id, feature_vector, image_url, mean_color):
        try:
            with self.conn.cursor() as cursor:
                query = """
                INSERT INTO public.features (dog_id, feature_vector, image_url, mean_color, data_criacao)
                VALUES (%s, %s, %s, %s, CURRENT_DATE) RETURNING dog_id;
                """
                cursor.execute(query, (dog_id, str(feature_vector), image_url, str(mean_color)))
                result = cursor.fetchone()[0]
                self.conn.commit()
                return result
        except Exception as e:
            self.conn.rollback()
            print(f"Erro ao inserir features: {e}")
            return None
