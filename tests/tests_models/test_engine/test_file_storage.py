import unittest
import json
import os.path
import models
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    def setUp(self):
        self.storage = FileStorage()
        self.storage._FileStorage__objects = {}

    def test_attributes(self):
        self.assertEqual(self.storage._FileStorage__file_path, "file.json")
        self.assertEqual(self.storage._FileStorage__objects, {})

    def test_all(self):
        all_objects = self.storage.all()
        self.assertIsInstance(all_objects, dict)
        self.assertEqual(all_objects, self.storage._FileStorage__objects)

    def test_new(self):
        obj = BaseModel()
        self.storage.new(obj)
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        self.assertIn(obj_key, self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects[obj_key], obj)

    def test_save(self):
        obj = BaseModel()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        self.storage.new(obj)
        self.storage.save()
        with open(self.storage._FileStorage__file_path, 'r') as f:
            data = json.load(f)
        self.assertIn(obj_key, data)
        self.assertEqual(data[obj_key], obj.to_dict())

    def test_reload(self):
        obj = BaseModel()
        obj_key = f"{obj.__class__.__name__}.{obj.id}"
        obj_dict = obj.to_dict()
        with open(self.storage._FileStorage__file_path, 'w') as f:
            json.dump({obj_key: obj_dict}, f)
        self.storage.reload()
        self.assertIn(obj_key, self.storage._FileStorage__objects)
        self.assertEqual(self.storage._FileStorage__objects[obj_key].to_dict(), obj_dict)


if __name__ == '__main__':
    unittest.main()