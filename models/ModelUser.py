from .entities.User import User
class ModelUser():
    @classmethod
    def login(self, db, user):
        print("estoy dentro de login archivo ModelUser")
        try:
            print("dentro de try y antes de cursor")
            cursor = db.connection.cursor()
            print("despuesde cursos (se muestran valores de entrada):", db, user)
            sql = """SELECT ID, USUARIO, CLAVE FROM usuario 
                    WHERE USUARIO = '{}'""".format(user.username)
            print("despues de sentencia")
            cursor.execute(sql)
            row=cursor.fetchone()
            print("valores de row:", row)
            if row != None:
                user = User(row[0], row[1], User.check_password(row[2], user.password))
                print("si la respuesta no es None:",user)
                return user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)
    
    @classmethod
    def get_by_id(self, db, id):
        try:
            cursor = db.connection.cursor()
            sql = """SELECT ID, NOMBRE FROM usuario 
                    WHERE ID = '{}'""".format(id)
            cursor.execute(sql)
            row=cursor.fetchone()
            if row != None:
                logged_user = User(row[0], row[1], None)
                return logged_user
            else:
                return None
        except Exception as ex:
            raise Exception(ex)