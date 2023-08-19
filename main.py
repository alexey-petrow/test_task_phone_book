from pathlib import Path
from typing import Callable, Optional

from phone_book import PhoneBook

DB_DIR_PATH: str = 'db'
FILENAME: str = 'phone_book_storage.csv'
FILEPATH: Path = Path(DB_DIR_PATH) / Path(FILENAME)
PAGE_SIZE: int = 5


def get_function_to_call(user_input: str, phone_book_instance: PhoneBook) -> Optional[Callable]:
    """
    Retrieves the corresponding PhoneBook method based on the user's input.
    Args:
        user_input (str): The user's choice represented as a string (e.g., '1', '2', etc.).
        phone_book_instance (PhoneBook): An instance of the PhoneBook class.
    Returns:
        Optional[Callable]: The method from the PhoneBook instance that corresponds
            to the user's input, or None if the input doesn't match any available method.
    """
    allowed_functions: dict = {
        '1': phone_book_instance.show_all_records,
        '2': phone_book_instance.add_new_record,
        '3': phone_book_instance.edit_record,
        '4': phone_book_instance.search_record,
    }
    function_to_call = allowed_functions.get(user_input)
    return function_to_call


def main():
    phone_book = PhoneBook(
        path_to_phone_book_data_file=FILEPATH,
        page_size=2,
    )
    while True:
        if phone_book.db_file_existence_check() is False:
            break
        print('Hello! Welcome to phonebook.')
        print('\nMenu:')
        print('1. Show all records')
        print('2. Add new record')
        print('3. Edit record')
        print('4. Search record')
        print('5. Exit program')

        user_choice = input('Choose option (1-5): ')

        function_to_call = get_function_to_call(
            user_input=user_choice,
            phone_book_instance=phone_book,
        )
        if function_to_call is not None:
            function_to_call()
        elif user_choice == '5':
            print('Bye, bye!')
            break
        else:
            print('Unknown command!')


if __name__ == '__main__':
    main()
