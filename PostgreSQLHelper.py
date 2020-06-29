import psycopg2
from psswd import PASSWORD


class PostgreSQLHelper:
    """
    Class with only static methods which perform many kind of operations with db.
    """

    @staticmethod
    def get_id():
        try:
            connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                          host="localhost", password=PASSWORD)
            cursor = connection.cursor()

            query = 'SELECT MAX(id) FROM equipment;'
            cursor.execute(query)
            id = cursor.fetchone()[0]

            if id is None:
                id = 0
            else:
                id += 1

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
            id = None
        finally:
            if (connection):
                cursor.close()
                connection.close()
                return id

    @staticmethod
    def get_columns(table_name):
        try:
            connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                          host="localhost", password=PASSWORD)
            cursor = connection.cursor()
            query = '''SELECT column_name FROM INFORMATION_SCHEMA.COLUMNS
                        WHERE table_name = \'{table_name}\';'''.format(table_name=table_name)
            cursor.execute(query)
            columns = [column[0].capitalize() for column in cursor.fetchall()]
            print(columns)
        except(Exception, psycopg2.Error) as error:
            print("Could not get columns ", error)
            columns = None
        finally:
            if connection:
                cursor.close()
                connection.close()
                return columns

    @staticmethod
    def create_table(table, columns, parent_table=''):
        """
        Creating new table
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                          host="localhost", password=PASSWORD)
            cursor = connection.cursor()
            create_table_query = ''' CREATE TABLE IF NOT EXISTS {0}
                                    ({1})'''.format(table, columns)
            if parent_table != '':
                create_table_query += ' INHERITS ({0});'.format(parent_table)
            else:
                create_table_query += ';'
            cursor.execute(create_table_query)
            connection.commit()

            print("Table created successfully in PostreSQL or it already exists.")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")

    @staticmethod
    def insert_to_table(table, keywords, values, percent_s_string):
        """
        Inserting record to table.
        :param table: name of the table to be inserted
        :param keywords: columns names
        :param values: actual data to be inserted
        :param percent_s_string: '%s,' string which is necessary to create sql insert query.
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment", database="windsurfingmanagment",
                                          host="localhost", password=PASSWORD)
            cursor = connection.cursor()

            sql_insert_query = ''' INSERT INTO {0} ({1}) VALUES ({2})'''.format(table, keywords, percent_s_string)
            cursor.execute(sql_insert_query, values)

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
    def bulk_insert(table, keywords, values, percent_s_string):
        """
        Inserting multiple rows to a table
        :param table: name of the table to be inserted
        :param keywords: columns names
        :param values: actual data to be inserted
        :param percent_s_string: '%s,' string which is necessary to create sql insert query.
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD,
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()
            sql_insert_query = ''' INSERT INTO {0} ({1}) VALUES ({2})'''.format(table, keywords, percent_s_string)
            result = cursor.executemany(sql_insert_query, values)
            connection.commit()

            print(cursor.rowcount, "Records inserted successfully into {0} table".format(table))
        except (Exception, psycopg2.Error) as error:
            print('Failed inserting record into ' + table + ' ' + error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')

    @staticmethod
    def update_table(id, key, value, table_name):
        """
        Method that updates records, fe. setting available attribute to the negation.
        :param table_name
        :param value: value that is going to be changed to
        :param key: column name to be changed
        :param id: id of the record
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD,
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()

            # Update single record row
            sql_update_query = ''' UPDATE {table} SET {key} = {value} WHERE id = {id}'''.format(table=table_name,
                                                                                                key=key,
                                                                                                value=value,
                                                                                                id=id)
            cursor.execute(sql_update_query)
            connection.commit()
        except (Exception, psycopg2.Error) as error:
            print('Failed updating record in ' + table_name + ' ' + error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')

    @staticmethod
    def delete_record_from_table(table_name, id):
        """
        Method that removes record from database.
        :param table_name:
        :param id: id of the item
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD,
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()
            delete_query = 'DELETE FROM {table} WHERE id={id}'.format(table=table_name, id=id)
            connection.commit()

            print("Record with ID:{id} has been removed from database.".format(id=id))
        except (Exception, psycopg2.Error) as error:
            print("Failed deleting record from database" + error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')

    @staticmethod
    def get_table(table_name):
        """
        Method that return all record from the given in argument table.
        :param table_name:
        :return: list of records or none if exception is raised.
        """
        record = None
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD,
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()
            query = 'SELECT * FROM {table}'.format(table=table_name)
            cursor.execute(query)
            records = cursor.fetchall()
        except(Exception, psycopg2.Error) as error:
            print("Could not get the table" + error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                return records