import csv
import os
from math import ceil
from pathlib import Path


class PhoneBook:
    def __init__(self,
                 path_to_phone_book_data_file: Path,
                 page_size: int = 5):
        """
        Initializes the PhoneBook class.
        Args:
            path_to_phone_book_data_file (Path): Path to the CSV file used
                for storing phone book data.
            page_size (int): Number of records to display per page. Defaults to 5.
        """
        assert isinstance(path_to_phone_book_data_file, Path)
        assert isinstance(page_size, int)
        self._path_to_db_file: Path = path_to_phone_book_data_file
        self._page_size: int = page_size

    def db_file_existence_check(self) -> bool:
        """
        Checks if the phone book data file exists. If not, prompts the user to create it.
        Returns:
            bool: True if the file exists, False otherwise.
        """
        if not self._path_to_db_file.exists():
            print('Phone book data not found!')
            user_input: str = input('\nPress "1" for create new phone book data, '
                                    'or press any other key to exit program: ')
            if user_input == '1':
                self._path_to_db_file.touch(exist_ok=True)
        return self._path_to_db_file.exists()

    def _get_empty_record(self) -> dict[str, str]:
        """
        Provides an empty phone book record structure.
        Returns:
            dict[str, str]: An empty phone book record.
        """
        return {
            'last_name': '',
            'first_name': '',
            'middle_name': '',
            'organization': '',
            'work_phone_number': '',
            'personal_phone_number': '',
        }

    def show_all_records(self) -> None:
        """
        Displays all records from the phone book, paginated by the predefined page size.
        """
        with open(self._path_to_db_file, 'r') as file:
            reader = csv.DictReader(file)
            records_list: list[dict[str, str]] = list(reader)
        pages_count: int = ceil(len(records_list) / self._page_size)
        allowed_pages: list[str] = [str(number + 1) for number in range(pages_count)]
        page: int = 1
        while True:
            start_index: int = (page - 1) * self._page_size
            end_index: int = start_index + self._page_size
            current_page: list = records_list[start_index:end_index]
            if len(current_page) == 0:
                print('\nNo records found.')
                break

            print(f'\n>>>Page {page} of {pages_count}<<<')
            for record in current_page:
                print(record)

            user_input: str = input('\nPress "n" for move to next page,'
                                    '"p" for move to previous page, '
                                    f'\nnumber from 1 to {pages_count} for move to chosen page, '
                                    '\nor any other key to return to main menu: ')
            if user_input == 'n' and str(page + 1) in allowed_pages:
                page += 1
            elif user_input == 'p' and str(page + 1) in allowed_pages:
                page -= 1
            elif user_input in allowed_pages:
                page = int(user_input)
            else:
                break

    def add_new_record(self) -> None:
        """
        Prompts the user to input data for a new record and adds it to the phone book.
        """
        new_record: dict[str, str] = self._get_empty_record()
        for key in new_record:
            new_record[key] = input(f'\nEnter {key}: ')

        with open(self._path_to_db_file, 'a', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=new_record.keys())
            if os.stat(self._path_to_db_file).st_size == 0:
                writer.writeheader()
            writer.writerow(new_record)
        print('Record added successfully!')
        print(new_record)

    def edit_record(self) -> None:
        """
        Allows the user to edit an existing record based on the provided first and last name.
        """
        lastname: str = input('\nEnter the lastname of editable record: ')
        firstname: str = input('Enter the firstname of editable record: ')

        with open(self._path_to_db_file, 'r') as file:
            reader = csv.DictReader(file)
            records_list: list[dict[str, str]] = list(reader)

        matched_records_indexes = []
        editable_record: dict | None = None
        for index, record in enumerate(records_list):
            if (record['last_name'].lower() == lastname.lower() and
                    record['first_name'].lower() == firstname.lower()):
                matched_records_indexes.append(index)

        if len(matched_records_indexes) == 0:
            print('No records found!')
            return

        if len(matched_records_indexes) > 1:
            print(f'Found {len(matched_records_indexes)} records!')
            for index in matched_records_indexes:
                print(f'{index + 1}) {records_list[index]}')

            user_input: str = input('\nEnter number of record you want to edit.')
            try:
                chosen_record_number: int = int(user_input)
            except ValueError:
                print(f'Incorrect value. {user_input} is not a number.')
                return
            if chosen_record_number - 1 in matched_records_indexes:
                editable_record: dict = records_list[chosen_record_number - 1]
        else:
            editable_record_index = matched_records_indexes[0]
            editable_record = records_list[editable_record_index]

        print(f'Editing record: {editable_record}')
        for key, value in editable_record.items():
            new_value = input(f'\nEnter new value for {key} '
                              f'(or press Enter to keep current value): ')
            if new_value:
                editable_record[key] = new_value

        with open(self._path_to_db_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=editable_record.keys())
            writer.writeheader()
            writer.writerows(records_list)
        print('Record updated successfully!')
        print(editable_record)

    def search_record(self) -> None:
        """
        Searches for records based on user input. Displays all matching records.
        """
        search_params: dict[str, str] = self._get_empty_record()
        for key in search_params:
            search_params[key] = input(f'\nEnter {key} (or press Enter to skip): ')

        matches = []
        with open(self._path_to_db_file, 'r') as file:
            reader = csv.DictReader(file)
            records_list: list[dict[str, str]] = list(reader)
            for record in records_list:
                if all(record[key].lower() == value.lower() or
                       not value
                       for key, value in search_params.items()):
                    matches.append(record)

        if matches:
            for match in matches:
                print(match)
        else:
            print('No records found!')
