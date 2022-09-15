import pymysql
from fastapi import FastAPI

# Creamos la clase para la conexion y consultas con la base de datos 

class DataBase:
    def __init__(self):
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password = '123456',
            db = 'proyecto'
        )
        
        self.cursor = self.connection.cursor()
        print('Conexion establecida')

    def select_driver(self,id):
        sql = 'SELECT * FROM drivers2_db WHERE driverId = {}'.format(id)

        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()

            return user[1],user[2],user[4]
        except Exception as e:
            raise
    
    def year_most_races(self):
        sql = 'SELECT count(*) as Cantidad_Carreras, year as Año FROM races_db group by year order by Cantidad_Carreras desc LIMIT 1;'
        
        try:
            self.cursor.execute(sql)
            most_races = self.cursor.fetchone()
            return most_races[0], most_races[1]

        except Exception as e:
            raise

    def pilot_most_winner(self):
        sql = 'SELECT 	count(*) as Cantidad_Carreras, r.driverId, d.Name_Complete FROM results as r JOIN drivers_db as d	ON (r.driverId = d.driverId) WHERE positionOrder = 1 GROUP BY driverId ORDER BY Cantidad_Carreras DESC limit 1;	'
        try:
            self.cursor.execute(sql)
            most_winner = self.cursor.fetchone()
            return most_winner[0],most_winner[1],most_winner[2]
        except Exception as e:
            raise

    def most_travelet_circuit(self):
        sql = 'SELECT 	count(*) as Cantidad_Veces, r.circuitId, c.name, c.location, c.country FROM races_db as r JOIN circuits as c ON (r.circuitId = c.circuitId) GROUP BY circuitId ORDER BY Cantidad_Veces DESC LIMIT 1;'
        try:
            self.cursor.execute(sql)
            most_trav_circuit = self.cursor.fetchone()
            return most_trav_circuit[0],most_trav_circuit[1],most_trav_circuit[2],most_trav_circuit[3],most_trav_circuit[4]
        except Exception as e:
            raise

    def pilot_more_points(self):
        american = 'American'
        british = 'British'
        sql = f'SELECT 	sum(r.points) as Puntos, r.driverId, c.constructorId, c.nationality, c.name, d.Name_Complete FROM results as r JOIN constructors as c 	ON (r.constructorId = c.constructorId) JOIN drivers_db as d 	ON (r.driverId = d.driverId) WHERE c.nationality = "{american}" or c.nationality = "{british}" GROUP BY r.driverId ORDER BY Puntos DESC LIMIT 1;'
        try:
            self.cursor.execute(sql)
            p_mor_points = self.cursor.fetchone()
            return p_mor_points[0],p_mor_points[1],p_mor_points[2],p_mor_points[3],p_mor_points[4],p_mor_points[5]
        except Exception as e:
            raise

app = FastAPI()         # Instaciamos la clase para generar la API
database = DataBase()   # Intanciamos la clase generada para la base de datos 

@app.get('/driver/{id}')
def Driver_Id(id : int):
    '''
    Funcion usada como testeo para la base de datos mysql, nos muestra los datos 
    del piloto, especificando el driverId de este

    Especificaciones:

        - Requiere parametro 'id'
        - Usa una query mysql predeterminada en la funcion, la cual es:
            <   SELECT * FROM drivers2_db WHERE driverId = {parametro_a_ingresar}    >
    '''
    driverId, code, nationality = database.select_driver(id)
    return {'DriverId':driverId,'Code':code,'Nationality':nationality}

@app.get('/year_most_races')
def most_races():
    '''
    Funcion usada para obtener el año con mayor cantidad de carreras

    Especificaciones:

        - No requiere parametros
        - Usa una query mysql predeterminada en la funcion, la cual es:
            <   SELECT 	count(*) as Cantidad_Carreras,
		            year as Año
                FROM races_db
                group by year
                order by Cantidad_Carreras desc
                LIMIT 1;    >
    '''

    Cantid_Carreras, Año = database.year_most_races()
    return {'Cantidad de Carreras':Cantid_Carreras, 
            'Año':Año}

@app.get('/pilot_most_winner')
def most_winner():
    '''
    Funcion usada para obtener el nombre del piloto con mas carreras ganadas

    Especificaciones:

        - No requiere parametros
        - Usa una query mysql predeterminada en la funcion, la cual es:
            <   SELECT 	count(*) as Cantidad_Carreras, 
                        r.driverId,
                        d.Name_Complete
                FROM results as r 
                JOIN drivers_db as d	ON (r.driverId = d.driverId)
                WHERE positionOrder = 1
                GROUP BY driverId
                ORDER BY Cantidad_Carreras DESC
                limit 1;    >
    '''

    Cantidad_Carreras, driverId, Name_Complete = database.pilot_most_winner()
    return{ 'Cantidad de Carreras':Cantidad_Carreras,
            'driverId': driverId,
            'Nombre Piloto': Name_Complete}

@app.get('/most_traveled_circuit')
def most_circuits():
    '''
    Funcion usada para obtener el nombre del circuito con mas recorridos realizados

    Especificaciones:

        - No requiere parametros
        - Usa una query mysql predeterminada en la funcion, la cual es:
            <   SELECT 	count(*) as Cantidad_Veces,
                        r.circuitId,
                        c.name,
                        c.location,
                        c.country
                FROM races_db as r
                JOIN circuits as c ON (r.circuitId = c.circuitId)
                GROUP BY circuitId
                ORDER BY Cantidad_Veces DESC
                LIMIT 1;    >
    '''

    Cantidad_Carreras, circuitId, name, location, country = database.most_travelet_circuit()
    return{ 'Cantidad de Carreras':Cantidad_Carreras,
            'driverId': circuitId,
            'Nombre de Circuito': name,
            'Localizacion':location,
            'Pais':country}

@app.get('/pilot_more_points')
def pilot_more_points_nationality():
    '''
    Funcion usada para mostrar la piloto con mas puntos obtenidos, sea este Americano o Britanico

    Especificaciones:

        - No requiere parametros
        - Usa una query mysql predeterminada en la funcion, la cual es:
            <   SELECT 	sum(r.points) as Puntos,
                        r.driverId,
                        c.constructorId,
                        c.nationality,
                        c.name,
                        d.Name_Complete
                FROM results as r
                JOIN constructors as c 	ON (r.constructorId = c.constructorId)
                JOIN drivers_db as d 	ON (r.driverId = d.driverId)
                WHERE c.nationality = 'American' or c.nationality = 'British'
                GROUP BY r.driverId
                ORDER BY Puntos DESC
                LIMIT 1;    >
    '''

    puntos, driverId, constructorId, nationality, name, Name_Complete = database.pilot_more_points()
    return {'Puntos totales':puntos,
            'DriverId':driverId,
            'ConstructorID':constructorId,
            'Nacionalidad':nationality,
            'Nombre Constructor':name,
            'Nombre Piloto':Name_Complete}

    
