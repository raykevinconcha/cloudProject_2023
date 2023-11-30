import pymysql


class DB:
    def __init__(self, host, username, password, database):
        self.host = host
        self.username = username
        self.password = password
        self.database = database

    # funciones generales

    def get(self, sql: str, whereEquals=None) -> list:
        '''
            inputs
            ---
            sql: query statement (ex: "SELECT * FROM interfaces")
            whereEquals: si se especifica un query con una condicion (ex: "select * from EnlaceBridges where TopologiaBridges_name=%s")
                       en el argumento 'whereEquals' se especifica el valor
            ejemplo de uso
            ---
            obtener_db("select * from EnlaceBridges where TopologiaBridges_name=%s", nombre)
        '''
        # conexion a la base de datos
        connection = pymysql.connect(host=self.host,
                                     user=self.username,
                                     password=self.password,
                                     database=self.database,
                                     cursorclass=pymysql.cursors.DictCursor)
        if (whereEquals):
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql, whereEquals)
                    result = cursor.fetchall()
                    return result
        else:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(sql)
                    result = cursor.fetchall()
                    return result

    def save(self, sql: str, data: tuple) -> None:
        '''
            inputs
            ---
            sql: query statment (ex: "INSERT INTO VM (name, imageName, vncPort) VALUES (%s,%s,%s)")
            data: values in a tuple (ex: (name, image_name, vnc_port))
            ejemplo de uso
            ---
            save_to_db("INSERT INTO VM (name, imageName, vncPort) VALUES (%s,%s,%s)", (vm.name, vm.image_name, vm.vnc_port))
        '''
        # conexion a la base de datos
        connection = pymysql.connect(host=self.host,
                                     user=self.username,
                                     password=self.password,
                                     database=self.database,
                                     cursorclass=pymysql.cursors.DictCursor)
        # ejecucion del sql query
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
                connection.commit()

    # funciones para casos especificos

    def obtener_topologias(self):
        data = self.get('select * from slices')
        # TODO parse data
        print(data)
        return data