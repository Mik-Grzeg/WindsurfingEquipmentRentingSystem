from PostgreSQLHelper import PostgreSQLHelper
from HelpingClass import HelpingTools


# TODO fix plain text db passwords
# TODO  str representation for desktop app

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
        if type(self) == Equipment:
            raise Exception("<Equipment> must be subclassed.")
        self.model = model_name
        self.cost = cost
        self.available = True
        self.id = PostgreSQLHelper.get_id()

    def insert_to_db(self):
        """
        Method that calls a method from HelpingTools that extract strings with keys and values,
         then it calls method from PostgeSQLHelper that inserts the record to a table.
        """
        HelpingTools.create_query_for_inserting_record(self)

    def update_record(self, key=None, val=None, dict_with_values_to_set=None):
        """
        Method that calls update_table which changes infromations of record in a database,
        depends on arguments it might be single variable or multiple.
        :param key: key word that is the name of a column in database table
        :param val: values that will be set
        :param dict_with_values_to_set: dictionary with column names as keys and values as values to be set.
        """
        if isinstance(dict_with_values_to_set, dict):
            for key in dict_with_values_to_set:
                if isinstance(dict_with_values_to_set[key], str):
                    dict_with_values_to_set[key] = '\'' + dict_with_values_to_set[key] + '\''

                PostgreSQLHelper.update_table(self.id,
                                              key.upper(),
                                              dict_with_values_to_set[key],
                                              self.table_name)
        else:
            if isinstance(val, str):
                val = '\'' + val + '\''
            PostgreSQLHelper.update_table(self.id,
                                          key.upper(),
                                          val,
                                          self.table_name)

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
        if type(self) == Board:
            raise Exception("<Board> must be subclassed.")
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

    def __init__(self, antygrass, nose_protector, purpose, volume, model_name, cost):
        super().__init__(volume=volume, model_name=model_name, cost=cost)
        self.purpose = purpose
        self.nose_protector = nose_protector
        self.antygrass = antygrass

    def __str__(self):
        # TODO representation for desktop app
        return super().__str__() + "\n\tPurpose: {0}\n".format(self.purpose)


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


if __name__ == "__main__":
    not_exit = True

    # y = Sail('Goya Mark', 70, 7.2, 'As new')
    z = AdvancedBoard(False, False, 'Slalom', 95, 'Goya Proton', 90)
    z.insert_to_db()
    # if btn_clicked:
    x = Sail('Goya Mark', 70, 7.4, 'As new')
    x.insert_to_db()
    # HelpingTools.create_tables_for_the_classes()
    # PostgreSQLHelper.bulk_insert(x.table_name, x.sql_columns, )
    # HelpingTools.create_query_for_bulk_inserting_record([x, y])
    # PostgreSQLHelper.update_table(12, 'Sail')
"""
    while not_exit:
        str_input = input("Create an object:")
        list_input = str_input.split(', ')

        if str_input == ':q':
            not_exit = False

"""
