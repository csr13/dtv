import os
import unittest
import sys
sys.path.append("..")


from src.config import images_path
from src.loader import Loader


class TestLoaderSetUp(unittest.TestCase):

    def setUp(self):
        self.image_loader = Loader(
            container=os.listdir(images_path),
            description="Pygame Images loader for rects"
        )


    def test_set_container(self):
        self.image_loader.container = [x for x in range(10)]


    def test_get_container(self):
        self.assertEquals(
            self.image_loader.container,
            os.listdir(images_path)
        )


    def test_delete_container(self):
        del self.image_loader.container
        self.assertEquals(self.image_loader.container, None)


    def test_set_description(self):
        self.image_loader.description = "Test Image loader"


    def test_get_description(self):
        self.assertEquals(
            self.image_loader.description,
            "Pygame Images loader for rects"
        )


    def test_delete_description(self):
        del self.image_loader.description
        self.assertEquals(self.image_loader.description, None)

    
    def tearDown(self):
        del self.image_loader


if __name__ == "__main__":
    unittest.main()