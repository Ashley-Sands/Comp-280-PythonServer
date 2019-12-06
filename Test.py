import unittest
from sql_query import sql_query
from helpers import Helpers as Help

class TestSqlQuery( unittest.TestCase ):

    root_dir = "databases/"

    def test_new_database_is_created(self):

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

        sql = sql_query(db_name)

        # open the connection, creat a table
        sql.connect_db()
        sql.add_table("test", "test_1 INT, test_2 VARCHAR(255), test_3 FLOAT")
        # TODO:... Finish test

        self.assertTrue(False)


if __name__ == "__main__":
    unittest.main()