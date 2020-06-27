from PostgreSQLHelper import PostgreSQLHelper


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
    def create_query_for_inserting_record(object):
        """
        Method that creates arguments for sql query to insert record into db.
        :param object:
        """
        attrs = vars(object)
        #attrs.pop('id')

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
        #object.set_id(id)

    @staticmethod
    def create_query_for_bulk_inserting_record(objects):
        """
        Method that creates arguments for sql query to insert many records into db.
        :param objects:
        """
        attrs = vars(objects[0])
        attrs.pop('id')
        # String with keywords - names of columns
        str_to_join_dict_keys = ", "
        sql_columns = str_to_join_dict_keys.join(list(attrs.keys())).upper()

        # String with '%s' that will be inserted into query
        s_str = '%s,' * len(attrs.values())
        s_str = s_str[:-1]

        # Tuple with values of specific attributes
        list_of_tuples_of_values = [tuple(vars(object).values()) for object in objects]
        values = tuple(list_of_tuples_of_values)

        PostgreSQLHelper.bulk_insert(table=objects[0].table_name, keywords=sql_columns,
                                     percent_s_string=s_str, values=values)
