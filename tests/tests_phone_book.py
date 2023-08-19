import unittest
from phone_book import PhoneBook
from unittest.mock import patch
from pathlib import Path
import csv
import tempfile


class TestPhoneBook(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=True)
        self.phone_book = PhoneBook(path_to_phone_book_data_file=Path(self.temp_file.name),
                                    page_size=2)

    def tearDown(self):
        self.temp_file.close()

    def test_db_file_existence_check_no_file(self):
        self.tearDown()
        with patch('builtins.input', return_value='q'):
            self.assertFalse(self.phone_book.db_file_existence_check())

    def test_db_file_existence_check_file_exists(self):
        self.setUp()
        self.assertTrue(self.phone_book.db_file_existence_check())

    def test_get_empty_record(self):
        expected = {
            'last_name': '',
            'first_name': '',
            'middle_name': '',
            'organization': '',
            'work_phone_number': '',
            'personal_phone_number': '',
        }
        self.assertEqual(self.phone_book._get_empty_record(), expected)

    def test_add_new_record(self):
        user_inputs = ['Андреев', 'Иван', 'Николаевич', 'Company', '123-456', '789-012']
        with patch('builtins.input', side_effect=user_inputs):
            self.phone_book.add_new_record()

        with open(self.temp_file.name, 'r') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['last_name'], 'Андреев')
        self.assertEqual(records[0]['first_name'], 'Иван')
        self.assertEqual(records[0]['middle_name'], 'Николаевич')
        self.assertEqual(records[0]['organization'], 'Company')
        self.assertEqual(records[0]['work_phone_number'], '123-456')
        self.assertEqual(records[0]['personal_phone_number'], '789-012')

    def test_edit_record(self):
        initial_data = [
            {
                'last_name': 'Андреев',
                'first_name': 'Иван',
                'middle_name': 'Николаевич',
                'organization': 'Company',
                'work_phone_number': '123-456',
                'personal_phone_number': '789-012'
            }
        ]
        with open(self.temp_file.name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=initial_data[0].keys())
            writer.writeheader()
            writer.writerows(initial_data)

        user_inputs = ['Андреев', 'Иван',
                       '', 'Ваня', '', 'Company2', '123-123', '789-789']
        with patch('builtins.input', side_effect=user_inputs):
            self.phone_book.edit_record()

        with open(self.temp_file.name, 'r') as file:
            reader = csv.DictReader(file)
            records = list(reader)

        self.assertEqual(len(records), 1)
        self.assertEqual(records[0]['last_name'], 'Андреев')
        self.assertEqual(records[0]['first_name'], 'Ваня')
        self.assertEqual(records[0]['middle_name'], 'Николаевич')
        self.assertEqual(records[0]['organization'], 'Company2')
        self.assertEqual(records[0]['work_phone_number'], '123-123')
        self.assertEqual(records[0]['personal_phone_number'], '789-789')

    def test_search_record(self):
        initial_data = [
            {
                'last_name': 'Андреев',
                'first_name': 'Иван',
                'middle_name': 'Николаевич',
                'organization': 'Company',
                'work_phone_number': '123-456',
                'personal_phone_number': '789-012'
            },
            {
                'last_name': 'Андреев',
                'first_name': 'Олег',
                'middle_name': 'Николаевич',
                'organization': 'Company',
                'work_phone_number': '123-456',
                'personal_phone_number': '789-012'
            }
        ]
        with open(self.temp_file.name, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=initial_data[0].keys())
            writer.writeheader()
            writer.writerows(initial_data)

        user_inputs = ['Андреев', 'Олег', '', '', '', '']
        with patch('builtins.input', side_effect=user_inputs):
            with patch('builtins.print') as mock_print:
                self.phone_book.search_record()

        mock_print.assert_called_with(initial_data[1])


if __name__ == "__main__":
    unittest.main()
