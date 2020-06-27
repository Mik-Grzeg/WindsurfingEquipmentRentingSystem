import psycopg2
import itertools
from psswd import PASWORD

class PostgreSQLHelper:
    """
    Class with only static methods which perform many kind of operations with db.
    """
    @staticmethod
    def insert_to_table(insert_query, record_to_insert):
        """
        Inserting record to table.
        :arg insert_query - sql query
        :arg record_to_insert - variables that will be saved
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                          host="localhost", password=PASSWORD)
            cursor = connection.cursor()
            cursor.execute(insert_query, record_to_insert)

            connection.commit()

            print("Record inserted successfully into sail table")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")

    @staticmethod
    def bulk_insert(table, keywords, records):
        """
        Inserting multiple rows to a table
        :param table: name of the table to be inserted
        :param keywords: columns names
        :param records: actual data to be inserted
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD)
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()
            sql_insert_query = ''' INSERT INTO {0} {1} VALUES {2}'''.format(table, keywords, records)
            result = cursor.executemany(sql_insert_query)
            connection.commit()
            print(cursor.rowcount(), "Record inserted successfully into {0} table".format(table))
        except (Exception, psycopg2.Error) as error:
            print('Failed inserting record into ' + table + ' ' + error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')

    @staticmethod
    def update_table(id, model):
        """
        Method that updates records, fe. setting available attribute to the negation.
        :param id: id of the item
        :param model: model of the item (string)
        """
        pass

    @staticmethod
    def delete_data(id, model):
        """
        Method to remove record from db
        :param id: id of the item
        :param model: model of the item (string)
        """
        pass


class Equipment:
    """
    Base class for any kind of equipment
    """
    newid = itertools.count()

    def __init__(self, model_name, cost):
        self.model = model_name
        self.cost = cost
        self.available = True
        #self.id = next(Equipment.newid)

    def __str__(self):
        return "Model: {0}\n\tCost:{1}".format(self.model, self.cost)


class Sail(Equipment):
    """
    Child class of Equipment which stands for sails.
    """

    def __init__(self, model_name, cost, size, condition):
        super(Sail, self).__init__(model_name=model_name, cost=cost)
        self.size = size
        self.condition = condition
        self.insert_to_db()

    def insert_to_db(self):
        insert_query = ''' INSERT INTO sail 
                                (MODEL,
                                COST, SIZE,
                                CONDITION, AVAILABLE)
                                VALUES(%s,%s,%s,%s,%s)'''
        record_to_insert = (self.model, self.cost,
                            self.size, self.condition, self.available)
        PostgreSQLHelper.insert_to_table(insert_query=insert_query, record_to_insert=record_to_insert)

    def rig(self):
        """
        Rigging sail, setting to available.
        :return:
        """
        pass

    def unrig(self):
        """
        Unrigging sail, setting to unavailable.
        #TODO set available atribute to False
        :return:
        """
        pass


class Board(Equipment):
    """
    Child class of equipment, that one is responsible for boards.
    During initialization, volume is being set.
    """

    def __init__(self, volume, model_name, cost):
        super(Board, self).__init__(model_name=model_name, cost=cost)
        self.volume = volume

    def __str__(self):
        return super(Board, self).__str__() + "\n\tVolume: {0}".format(self.volume)

    def broken_board(self):
        """
        If somebody somehow damage a board, and it needs to be repaired,
        then availibility is set to False
        :return:
        """
        self.available = False

    def insert_to_db(self):
        insert_query = ''' INSERT INTO board 
                                (MODEL,
                                COST, VOLUME,
                                AVAILABLE)
                                VALUES(%s,%s,%s,%s,%s)'''
        record_to_insert = (self.model, self.cost,
                            self.size, self.condition, self.available)
        PostgreSQLHelper.insert_to_table(insert_query=insert_query, record_to_insert=record_to_insert)


class DaggerBoard(Board):
    """
    Child class of Board, responsible for daggerboards.
    """

    def __init__(self, volume, model_name, cost):
        super().__init__(volume=volume, model_name=model_name, cost=cost)
        self.dagger = True


class DaggerLessBoard(Board):
    """
    Child class of Board, responsible for daggerless boards.
    During initialization few atributes are set.
    """

    def __init__(self, if_antygrass, nose_protector, purpose, volume, model_name, cost):
        super().__init__(volume=volume, model_name=model_name, cost=cost)
        self.purpose = purpose
        self.nose_protector = nose_protector
        self.if_antygrass = if_antygrass

    def __str__(self):
        return super().__str__() + "\n\tPurpose: {0}\n".format(self.purpose)


#x = DaggerLessBoard(if_antygrass=False, nose_protector=False,
                    #purpose='Slalom', volume=95, model_name='Goya Proton', cost=90)

print("{0}".format('balls'))
#sail = Sail("Goya Mark", 70, 6.2, "As new")
#Sail('Goya Mark', 70, 7.2, "As new")
"""
try:
    connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                  host="localhost", password=PASSWORD)
    cursor = connection.cursor()
    print("Connection established")
        create_table_query = ''' CREATE TABLE SAIL
        (ID INT PRIMARY KEY NOT NULL, 
        MODEL TEXT NOT NULL, 
        COST INT NOT NULL, 
        SIZE REAL NOT NULL,
        CONDITION TEXT,
        AVAILABLE BOOLEAN NOT NULL);'''
    cursor.execute('''INSERT INTO sail 
                        (ID, MODEL,
                        COST, SIZE,
                        CONDITION, AVAILABLE)
                        VALUES(%s,%s,%s,%s,%s,%s)''', (sail.id, sail.model, sail.cost,
                                                       sail.size, sail.condition, sail.available))
    connection.commit()

    print("Record inserted successfully into sail table")
    print("Table created successfully in PostreSQL")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed.")
"""