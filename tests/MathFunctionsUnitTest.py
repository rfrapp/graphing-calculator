
import unittest, sys
sys.path.insert(0, '..')
import MathFunctions

class MathFunctionsUnitTest(unittest.TestCase):
    def test_shuntingyard(self):
    	self.assertEqual(MathFunctions.shuntingYard("2 + 2"), "2 2 +")


if __name__ == '__main__':
	unittest.main()
