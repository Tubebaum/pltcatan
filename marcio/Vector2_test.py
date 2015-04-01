from Vector2 import Vector2
import unittest

class TestVector2(unittest.TestCase):
    def testEqual(self):
        v2 = Vector2(10, 10)
        v1 = Vector2(10, 10)
        self.assertEqual(v1, v2)

    def testMultiply(self):
        v1 = Vector2(10, 10)
        v2 = Vector2(30, 30)
        self.assertEqual(v1 * 3, v2)

    def testMultiplyRight(self):
        v1 = Vector2(10, 10)
        v2 = Vector2(30, 30)
        self.assertEqual(3 * v1, v2)

    def testAdd(self):
        self.assertEqual(Vector2(1, 1) + Vector2(2, 3), Vector2(3, 4))

if __name__ == '__main__':
    unittest.main()
