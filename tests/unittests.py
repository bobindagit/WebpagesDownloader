import unittest
import main


class MainTest(unittest.TestCase):
    def test_get_filename(self):
        answer = '21955c71926e2'
        query = 'https://aviapages.com/docs/21955c71926e2/'
        self.assertEqual(main.get_filename(query), answer)
        
        answer = '21955c71926e2'
        query = 'https://aviapages.com/docs/21955c71926e2'
        self.assertEqual(main.get_filename(query), answer)
        
        answer = '21955c71926e2'
        query = 'https://aviapages.com/docs/21955c71926e2///'
        self.assertEqual(main.get_filename(query), answer)