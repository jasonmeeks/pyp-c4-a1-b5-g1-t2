import os
import sys
from collections import OrderedDict
from datetime import date


databases = {}

class Database(object):
    def __init__(self):
        self.tables = {}
    
    
    def create_table(self, name, columns):
        # Takes column title info, checks for ID, puts ID in first location,
        # and then creates a table object based on that information
        processed_columns = OrderedDict()
        if isinstance(columns, dict):
            if "id" in columns.keys():
                processed_columns["id"] = columns["id"]
                for item in columns:
                    if item != "id":
                        processed_columns[item] = columns[item]
            else:
                raise ValueError
        else:
            print "No columns entered"
        self.tables[name] = Table(processed_columns)


    def __getattr__(self, name):
        return self.tables[name]


class Table(object):
    def __init__(self, columns):
        self.columns = columns
        self.rows = {}
    
    
    def insert(self, *args):
        # Checks row data type and length and then creates row inside table
        count = 0
        if len(self.columns) == len(args):
            for column in self.columns:
                    if not isinstance(args[count], self.columns[column]):
                        raise ValueError
                    count += 1
            else:
                count = 0
                self.rows[args[0]] = OrderedDict()
                for title in self.columns:
                    self.rows[args[0]][title] = args[count]
                    count += 1
        else:
            raise IndexError
    
    
    def query(self, **kwargs):
        # Searches for query in database rows and prints matching rows
        matches = 0
        result = ""
        for key, value in kwargs.iteritems():
            print "Searching for %s = %s..." % (key, value)
        if key in self.columns:
            for row in self.rows:
                if str(value) in str(self.rows[row][key]):
                    matches += 1
                    for item in self.rows[row]:
                        result += str(item) + ": " + str(self.rows[row][item]) + "   "
                    result += "\n"
                    # print self.rows[row]
        else:
            raise ValueError
        if matches == 1:
            print str(matches) + " match found..."
        else:
            print str(matches) + " matches found..."
        print result
        

    def index(self):
        pass


def create_database(name):
    # Creates new database based on name given
    # Later this will create a file to write to and store database into
    databases[name] = Database()


def use(name):
    # Returns database from given name if database exists
    if name in databases:
        return databases[name]
    else:
        raise ValueError
