#!/usr/bin/python3
"""test for file_storage"""
import unittest
import os
import json
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test the FileStorage class"""

    def setUp(self):
        """Set up the tests"""
        self.storage = FileStorage()

    def tearDown(self):
        """Tear down the tests"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

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
        with open("file.json", "r") as f:
            self.assertIn(bm.__class__.__name__ + "." + bm.id,
                          json.load(f))

    def test_reload(self):
        """Test the reload method"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm.__class__.__name__ + "." + bm.id, self.storage.all())

    def test_save_reload(self):
        """Test the save and reload methods"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm.__class__.__name__ + "." + bm.id, self.storage.all())

    def test_all_with_class(self):
        """Test the all method with a class"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm.__class__.__name__ + "." + bm.id,
                      self.storage.all(BaseModel))
        self.assertNotIn(bm.__class__.__name__ + "." + bm.id,
                         self.storage.all(User))

    def test_all_with_class_name(self):
        """Test the all method with a class name"""
        bm = BaseModel()
        self.storage.new(bm)
        self.storage.save()
        self.storage.reload()
        self.assertIn(bm.__class__.__name__ + "." + bm.id,
                      self.storage.all("BaseModel"))
        self.assertNotIn(bm.__class__.__name__ + "." + bm.id,
                         self.storage.all("User"))

    def test_new_with_class(self):
        """Test the new method with a class"""
        bm = BaseModel()
        self.storage.new(bm)
        self.assertIn(bm.__class__.__name__ + "." + bm.id, self.storage.all())
