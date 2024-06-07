#!/usr/bin/python3
"""
Contains the TestDBStorageDocs and TestDBStorage classes
"""

from datetime import datetime
import inspect
import models
from models.engine import db_storage
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import json
import os
import pep8
import unittest

classes = {
    "Amenity": Amenity,
    "City": City,
    "Place": Place,
    "Review": Review,
    "State": State,
    "User": User,
}


class TestDBStorageDocs(unittest.TestCase):
    """Tests to check the documentation and style of DBStorage class"""
    DBStorage = db_storage.DBStorage

    @classmethod
    def setUpClass(cls):
        """Set up for the doc tests"""
        cls.dbs_f = inspect.getmembers(cls.DBStorage, inspect.isfunction)

    def test_pep8_conformance(self):
        """Test that models/base_model.py conforms to PEP8."""
        files = [
            "models/engine/db_storage.py",
            "tests/test_models/test_engine/test_db_storage.py",
        ]
        err_msg = "Found code style errors (and warnings)."
        for path in files:
            with self.subTest(path=path):
                errors = pep8.Checker(path).check_all()
                self.assertEqual(errors, 0, err_msg)

    def test_db_storage_module_docstring(self):
        """Test for the db_storage.py module docstring"""
        err_msg = "db_storage.py needs a docstring"
        self.assertIsNot(db_storage.__doc__, None, err_msg)
        self.assertTrue(len(db_storage.__doc__) >= 1, err_msg)

    def test_db_storage_class_docstring(self):
        """Test for the DBStorage class docstring"""
        err_msg = "DBStorage class needs a docstring"
        self.assertIsNot(self.DBStorage.__doc__, None, err_msg)
        self.assertTrue(len(self.DBStorage.__doc__) >= 1, err_msg)

    def test_dbs_func_docstrings(self):
        """Test for the presence of docstrings in DBStorage methods"""
        for func in inspect.getmembers(self.DBStorage, inspect.isfunction):
            err_msg = "{:s} method needs a docstring".format(func[0])
            self.assertIsNot(func[1].__doc__, None, err_msg)
            self.assertTrue(len(func[1].__doc__) >= 1, err_msg)


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_all_returns_dict(self):
        """Test that all returns a dictionaty"""
        self.assertIs(type(models.storage.all()), dict)

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_all_no_class(self):
        """Test that all returns all rows when no class is passed"""
        state = State(name="Alabama")
        user = User(email="johndoe@mailer.com", password="j123d")
        state.save()
        user.save()
        self.assertEqual(len(models.storage.all()), 2)

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_new(self):
        """test that new adds an object to the database"""
        state = State(name="Alabama")
        state.save()
        db_state = models.storage.get(State, state.id)
        self.assertIsNotNone(db_state)
        self.assertEqual(state.id, db_state.id)
        self.assertIs(state, db_state)

    @unittest.skipIf(models.storage_t != "db", "not testing db storage")
    def test_save(self):
        """Test that save properly saves objects to file.json"""
