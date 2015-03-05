from Vector2 import Vector2
import unittest

class TestVector2(unittest.TestCase):

    def test_eq(self):
        v2 = Vector2(10,10)
        v1 = Vector2(10,10)
        self.assertEqual(v1, v2)

    def test_mult(self):
        v1 = Vector2(10,10)
        v2 = Vector2(30,30)
        self.assertEqual(v1*3, v2)

    def test_multr(self):
        v1 = Vector2(10,10)
        v2 = Vector2(30,30)
        self.assertEqual(3*v1, v2)

    def test_add(self):
        self.assertEqual(Vector2(1, 1)+Vector2(2, 3), Vector2(3, 4))

if __name__ == '__main__':
    unittest.main()