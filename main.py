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
        sql = 'SELECT * FROM drivers WHERE driverId = {}'.format(id)

        try:
            self.cursor.execute(sql)
            user = self.cursor.fetchone()

            return user[1],user[2],user[4]
        except Exception as e:
            raise
    
    def year_most_races(self):
        sql = 'SELECT 	count(*) as Cantidad_Carreras, year_race as Año FROM races group by year_race order by Cantidad_Carreras desc LIMIT 1;'
        
        try:
            self.cursor.execute(sql)
            most_races = self.cursor.fetchone()
            return most_races[0], most_races[1]

        except Exception as e:
            raise

    def pilot_most_winner(self):
        sql = 'SELECT 	count(*) as Cantidad_Carreras, r.driverId, d.Name_driver FROM results as r JOIN drivers as d ON (r.driverId = d.driverId) WHERE PositionOrder = 1 GROUP BY driverId ORDER BY Cantidad_Carreras DESC limit 1;	'
        try:
            self.cursor.execute(sql)
            most_winner = self.cursor.fetchone()
            return most_winner[0],most_winner[1],most_winner[2]
        except Exception as e:
            raise

    def most_travelet_circuit(self):
        sql = 'SELECT count(*) as Cantidad_Veces, r.circuitId, c.name, c.location, c.country FROM races as r JOIN circuits as c ON (r.circuitId = c.circuitsId) GROUP BY circuitIdORDER BY Cantidad_Veces DESC LIMIT 1;'
        try:
            self.cursor.execute(sql)
            most_trav_circuit = self.cursor.fetchone()
            return most_trav_circuit[0],most_trav_circuit[1],most_trav_circuit[2],most_trav_circuit[3],most_trav_circuit[4]
        except Exception as e:
            raise

    def pilot_more_points(self):
        american = 'American'
        british = 'British'
        sql = f'SELECT sum(r.points) as Puntos, r.driverId, c.constructorsId, c.nationality, c.name_constructor, d.Name_driver FROM results as r JOIN constructors as c 	ON (r.constructorId = c.constructorsId) JOIN drivers as d 	ON (r.driverId = d.driverId) WHERE c.nationality = "{american}" or c.nationality = "{british}" GROUP BY r.driverId ORDER BY Puntos DESC LIMIT 1;'
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
    Function used as a test for the mysql database, it shows us the data of the driver, 
    specifying the driverId of this

     Specs:

         - Requires parameter 'id'
         - Use a default mysql query in the function, which is:
            <   SELECT * FROM drivers WHERE driverId = {parametro_a_ingresar}    >
    '''
    driverId, code, nationality = database.select_driver(id)
    return {'DriverId':driverId,'Code':code,'Nationality':nationality}

@app.get('/year_most_races')
def most_races():
    '''
    Function used to obtain the year with the highest number of races

    Specs:

        - Does not require parameters
        - Use a default mysql query in the function, which is:
            <   SELECT 	count(*) 	as Cantidad_Carreras,
                        year_race	as Año
                FROM races
                group by year_race
                order by Cantidad_Carreras desc
                LIMIT 1;    >
    '''

    Cantid_Carreras, Año = database.year_most_races()
    return {'Cantidad de Carreras':Cantid_Carreras, 
            'Año':Año}

@app.get('/pilot_most_winner')
def most_winner():
    '''
    Function used to get the name of the driver with the most race wins

    Specs:

        - Does not require parameters
        - Use a default mysql query in the function, which is: 
            <   SELECT 	count(*) as Cantidad_Carreras, 
                        r.driverId,
                        d.Name_driver
                FROM results as r 
                JOIN drivers as d	ON (r.driverId = d.driverId)
                WHERE PositionOrder = 1
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
    Function used to obtain the name of the circuit with the most routes made

    Specs:

        - Does not require parameters
        - Use a default mysql query in the function, which is:
            <   SELECT 	count(*) as Cantidad_Veces,
                        r.circuitId,
                        c.name,
                        c.location,
                        c.country
                FROM races as r
                JOIN circuits as c ON (r.circuitId = c.circuitsId)
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
    Function used to show the pilot with the most points obtained, be it American or British

    Specs:

        - Does not require parameters
        - Use a default mysql query in the function, which is:
            <   SELECT 	sum(r.points) as Puntos,
                        r.driverId,
                        c.constructorsId,
                        c.nationality,
                        c.name_constructor,
                        d.Name_driver
                FROM results as r
                JOIN constructors as c 	ON (r.constructorId = c.constructorsId)
                JOIN drivers as d 	ON (r.driverId = d.driverId)
                WHERE c.nationality = "American" or c.nationality = "British"
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

    
