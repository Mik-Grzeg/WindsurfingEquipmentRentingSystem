from PostgreSQLHelper import PostgreSQLHelper
import itertools

#TODO fix plain text db passwords


class Equipment:
    """
    Base class for any kind of equipment
    """
    sql_columns_details = '''ID serial PRIMARY KEY,
                            MODEL TEXT NOT NULL,
                            COST INT NOT NULL,
                            AVAILABLE BOOLEAN NOT NULL'''
    sql_columns = 'MODEL, COST, AVAILABLE'
    table_name = 'equipment'

    def __init__(self, model_name, cost):
        self.model = model_name
        self.cost = cost
        self.available = True

    def __str__(self):
        return "Model: {0}\n\tCost:{1}".format(self.model, self.cost)


class Sail(Equipment):
    """
    Child class of Equipment which stands for sails.
    """
    sql_columns_details = 'SIZE REAL NOT NULL, CONDITION TEXT NOT NULL'
    sql_columns = 'MODEL, COST, SIZE, CONDITION, AVAILABLE'
    table_name = 'sail'

    def __init__(self, model_name, cost, size, condition):
        super(Sail, self).__init__(model_name=model_name, cost=cost)
        self.size = size
        self.condition = condition
        #self.insert_to_db()

    def insert_to_db(self):
        insert_query = ''' INSERT INTO {0} ({1})
                            VALUES(%s,%s,%s,%s,%s)'''.format(Sail.table_name, Sail.sql_columns)
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
    sql_columns_details = 'VOLUME INT NOT NULL'
    sql_columns = 'MODEL, COST, VOLUME, AVAILABLE'
    table_name = 'board'

    def __init__(self, volume, model_name, cost):
        super(Board, self).__init__(model_name=model_name, cost=cost)
        self.volume = volume

    def __str__(self):
        return super(Board, self).__str__() + "\n\tVolume: {0}".format(self.volume)

    def broken_board(self):
        """
        If somebody somehow damage a board, and it needs to be repaired,
        then availability is set to False
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
    sql_columns_details = 'DAGGER BOOLEAN NOT NULL'
    sql_columns = 'MODEL, COST, VOLUME, DAGGER, AVAILABLE'
    table_name = 'dagger_board'

    def __init__(self, volume, model_name, cost):
        super().__init__(volume=volume, model_name=model_name, cost=cost)
        self.dagger = True


class AdvancedBoard(Board):
    """
    Child class of Board, responsible for advanced boards.
    During initialization few attributes are set.
    """
    sql_columns_details = '''PURPOSE TEXT NOT NULL, 
                            NOSE_PROTECTOR BOOLEAN NOT NULL,
                            ANTYGRASS BOOLEAN NOT NULL'''
    sql_columns = 'MODEL, COST, VOLUME, PURPOSE, NOSE_PROTECTOR, ANTYGRASS, AVAILABLE'
    table_name = 'advanced_board'

    def __init__(self, if_antygrass, nose_protector, purpose, volume, model_name, cost):
        super().__init__(volume=volume, model_name=model_name, cost=cost)
        self.purpose = purpose
        self.nose_protector = nose_protector
        self.if_antygrass = if_antygrass

    def __str__(self):
        return super().__str__() + "\n\tPurpose: {0}\n".format(self.purpose)


class HelpingTools:
    @staticmethod
    def name_of_parent_class_for_instance(object):
        parent_class = type(object).__mro__[1].__name__.lower()
        if parent_class != 'object':
            return parent_class
        else:
            return ''

    @staticmethod
    def name_of_parent_class_for_class(object):
        parent_class = object.__mro__[1].__name__.lower()
        if parent_class != 'object':
            return parent_class
        else:
            return ''

    @staticmethod
    def create_tables_for_the_classes():
        PostgreSQLHelper.create_table(Equipment.table_name, Equipment.sql_columns_details,
                                      HelpingTools.name_of_parent_class_for_class(Equipment))
        PostgreSQLHelper.create_table(Board.table_name, Board.sql_columns_details,
                                      HelpingTools.name_of_parent_class_for_class(Board))
        PostgreSQLHelper.create_table(DaggerBoard.table_name, DaggerBoard.sql_columns_details,
                                      HelpingTools.name_of_parent_class_for_class(DaggerBoard))
        PostgreSQLHelper.create_table(AdvancedBoard.table_name, AdvancedBoard.sql_columns_details,
                                      HelpingTools.name_of_parent_class_for_class(AdvancedBoard))
        PostgreSQLHelper.create_table(Sail.table_name, Sail.sql_columns_details,
                                      HelpingTools.name_of_parent_class_for_class(Sail))

    @staticmethod
    def create_query_for_inserting_record(object):
        """
        Method that creates arguments for sql query to insert record into db.
        :param object:
        """
        attrs = vars(object)
        # String with keywords - names of columns
        str_to_join_dict_keys = ", "
        sql_columns = str_to_join_dict_keys.join(list(attrs.keys())).upper()

        # String with '%s' that will be inserted into query
        s_str = '%s,' * len(attrs.values())
        s_str = s_str[:-1]

        # Tuple with values of specific attributes
        values = tuple(attrs.values())

        PostgreSQLHelper.insert_to_table(table=object.table_name, keywords=sql_columns,
                                         percent_s_string=s_str, values=values)


if __name__ == "__main__":
    not_exit = True
    x = Sail('Goya Mark', 70, 7.4, 'As new')
    #HelpingTools.create_tables_for_the_classes()
    #PostgreSQLHelper.bulk_insert(x.table_name, x.sql_columns, )
    HelpingTools.create_query_for_inserting_record(x)
"""
    while not_exit:
        str_input = input("Create an object:")
        list_input = str_input.split(', ')

        if str_input == ':q':
            not_exit = False

"""
