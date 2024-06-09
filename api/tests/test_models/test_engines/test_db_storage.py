#!/usr/bin/python3
"""test for db_storage"""
import unittest
import os
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.engine.db_storage import DBStorage


class TestDBStorage(unittest.TestCase):
    """Test the DBStorage class"""

    def setUp(self):
        """Set up the tests"""
        self.storage = DBStorage()

    def tearDown(self):
        """Tear down the tests"""
        self.storage._DBStorage__session.close()
        self.storage._DBStorage__session.remove()

    def test_all(self):
        """Test the all method"""
        self.assertIsInstance(self.storage.all(), dict)

    def test_new(self):
        """Test the new method"""
        bm = BaseModel()
        self.storage.new(bm)
        key = bm.__class__.__name__ + "." + bm.id
        self.assertIn(key, self.storage.all())

    def test_save(self):
        """Test the save method"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertIn(bm, self.storage.all().values())

    def test_reload(self):
        """Test the reload method"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm, self.storage.all().values())

    def test_save_reload(self):
        """Test the save and reload methods"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm, self.storage.all().values())

    def test_count(self):
        """Test the count method"""
        count = self.storage.count()
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertEqual(count + 1, self.storage.count())

    def test_get(self):
        """Test the get method"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertEqual(bm, self.storage.get(BaseModel, bm.id))

    def test_count_cls(self):
        """Test the count_cls method"""
        count = self.storage.count()
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.assertEqual(count + 1, self.storage.count(BaseModel))

    def test_close(self):
        """Test the close method"""
        self.storage.close()
        self.assertIsNone(self.storage._DBStorage__session)
