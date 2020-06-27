import psycopg2
from psswd import PASSWORD


class PostgreSQLHelper:
    """
    Class with only static methods which perform many kind of operations with db.
    """

    @staticmethod
    def create_table(table, columns,  parent_table=''):
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

            sql_get_id_query = 'SELECT MAX(id) FROM {0};'.format(table)
            cursor.execute(sql_get_id_query)

            instance_id = cursor.fetchone()
            print(instance_id[0])
            connection.commit()

            print("Record inserted successfully into sail table")
        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            if (connection):
                cursor.close()
                connection.close()
                print("PostgreSQL connection is closed.")
                return instance_id

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
    def update_table(id, table_name):
        """
        Method that updates records, fe. setting available attribute to the negation.
        :param table_name:
        :param id: id of the item
        :param model: model of the item (string)
        """
        try:
            connection = psycopg2.connect(user="WindsurfingManagment",
                                          password=PASSWORD,
                                          host='localhost',
                                          database='windsurfingmanagment')
            cursor = connection.cursor()
            sql_select_query = ''' SELECT * FROM {0} WHERE id = {1}'''.format(table_name, id)
            cursor.execute(sql_select_query)
            record = cursor.fetchone()

            id = record[0]

            #Update single record row
            #sql_update_query = ''' UPDATE {0} SET available = {1} WHERE id = {2}'''.format(table_name, )
        except (Exception, psycopg2.Error) as error:
            print('Failed updating record in ' + table_name + ' ' + error)
        finally:
            if(connection):
                cursor.close()
                connection.close()
                print('PostgreSQL connection is closed')

    @staticmethod
    def delete_data(id, model):
        """
        Method to remove record from db
        :param id: id of the item
        :param model: model of the item (string)
        """
        pass
