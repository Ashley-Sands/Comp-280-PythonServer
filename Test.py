import unittest
from sql_query import sql_query
from helpers import Helpers as Help
import os

class TestSqlQuery( unittest.TestCase ):

    root_dir = "test/test_databases/"

    def test_new_database_is_created_and_destroyed(self):

        db_name = self.root_dir + "test_creatAndDestroy_db"

        sql = sql_query(db_name)
        # open and close the database
        sql.connect_db()
        sql.close_db()

        # does it exist?
        self.assertTrue( Help.file_exist(db_name) )

        # destroy db
        sql.destroy_database()

        # has it been destroyed?
        self.assertFalse( Help.file_exist(db_name) )

    def test_row_is_added_and_removed(self):

        db_name = self.root_dir + "test_row_added_db"

        sql = sql_query(db_name)

        # open the connection, creat a table and insert a row :D
        sql.connect_db()
        sql.add_table("test", "test_1 INT, test_2 VARCHAR(255), test_3 FLOAT")
        sql.insert_row("test", ["test_1", "test_2", "test_3"], ["10", "helloo World", "11.11"])

        # get the row from the DB and test the tree value exist
        data = sql.select_from_table("test", ["*"], ["test_1"], ["10"])
        data = list(data[0])

        self.assertTrue( 10 in data and "helloo World" in data and 11.11 in data)

        # destroy the db, not needed any more :)
        sql.destroy_database()


    def test_table_is_created_and_dropped(self):
        db_name = self.root_dir + "test_table_added_dropped"
        table_name = "test_table"

        sql = sql_query(db_name)

        # open the connection, to the database
        sql.connect_db()

        # check the table we are going to create does not already exist
        tables = sql.get_all_tables()

        self.assertFalse( table_name in tables )

        # add table and check it does exist
        sql.add_table(table_name, "test_1 INT, test_2 VARCHAR(255), test_3 FLOAT")
        tables = sql.get_all_tables()

        self.assertTrue( table_name in tables )

        # drop the table and check it no longer exist
        sql.drop_table(table_name)
        tables = sql.get_all_tables()

        self.assertFalse( table_name in tables )

        # finally clear up the test and remove database
        sql.destroy_database()

    def test_select_from_table_selects_correct_item(self):

        db_name = self.root_dir + "test_select_from_table"
        table_name = "test_table"
        sql = sql_query(db_name)

        # create the test database and populate with items
        sql.connect_db()
        sql.add_table(table_name, "test_1 INT, test_2 VARCHAR(255), test_3 FLOAT")

        sql.insert_row(table_name, ["test_1", "test_2", "test_3"], ["0", "helloo World", "0.1"])
        sql.insert_row(table_name, ["test_1", "test_2", "test_3"], ["2", "helloo World", "0.2"])
        sql.insert_row(table_name, ["test_1", "test_2", "test_3"], ["1", "helloo World", "0.3"])
        sql.insert_row(table_name, ["test_1", "test_2", "test_3"], ["4", "goodbye World", "0.4"])

        # select a single item from the table
        # SELECT * FROM test_table WHERE test_1 == 2
        selected_items = sql.select_from_table(table_name, ["*"], ["test_1"], ["2"])

        print(selected_items[0])
        # check there is only one result
        self.assertEqual(len(selected_items), 1)
        # and the data matches the inputted data
        self.assertEqual(selected_items[0], (2, "helloo World", 0.2))

        # select multiple items from the table
        # SELECT * FROM test_table WHERE test_2 == "helloo World"
        selected_items = sql.select_from_table(table_name, ["*"], ["test_2"], ["helloo World"])

        # check there we have 3 results
        self.assertEqual(len(selected_items), 3)
        # and the data matches the inputted data
        self.assertEqual(selected_items[0], (0, "helloo World", 0.1))
        self.assertEqual(selected_items[1], (2, "helloo World", 0.2))
        self.assertEqual(selected_items[2], (1, "helloo World", 0.3))

        sql.destroy_database()

    def test_item_is_updated_correctly(self):

        db_name = self.root_dir + "test_update_table_item"
        table_name = "test_update"
        sql = sql_query(db_name)

        # create database and populate
        sql.connect_db()
        sql.add_table(table_name, "test_1 INT, test_2 VARCHAR(255), test_3 FLOAT")
        sql.insert_row(table_name, ["test_1", "test_2", "test_3"], ["0", "helloo World", "0.1"])

        # update the inserted row
        sql.update_row( table_name, ["test_2"], ["goodbye world"], ["test_1"], ["0"])

        # check that values t1 and t3 match the inserted but t2 does not match (but matching the updated value)
        updated_row = sql.select_from_table(table_name, ["*"])[0]
        print(updated_row)
        # inserted
        self.assertEqual(updated_row[0], 0)
        self.assertEqual(updated_row[2], 0.1)
        # updated
        self.assertEqual(updated_row[1], "goodbye world")

        sql.destroy_database()


if __name__ == "__main__":

    # search for a path that does not exist
    # to insure we don't delete any stuff that is needed
    # and it also insures that we are creating new databases ect...
    i = 1
    base_root = TestSqlQuery.root_dir[:-1]

    while os.path.exists( TestSqlQuery.root_dir ) and len(os.listdir( TestSqlQuery.root_dir ) ) > 0:
        TestSqlQuery.root_dir = base_root + "_"+str(i)+"/"
        i += 1

    # create the test folder
    os.makedirs( TestSqlQuery.root_dir, exist_ok=True )

    # run test
    unittest.main()
