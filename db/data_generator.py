import csv
import random


def generate_test_data(filename: str, records_count: int = 100) -> None:
    """
    Generates test data for phonebook and writes it to a csv file.
    Args:
        filename: (str) name of file with extension (.csv)
        records_count: (int) number of generated records
    """
    lastnames = ['Вася', 'Саня', 'Стас', 'Олег', 'Лёха', 'Ваня', 'Дима', 'Серёга',
                 'Денис', 'Кирилл', 'Слава', 'Витя', 'Вова', 'Боря', 'Андрей']
    firstnames = ['Петров', 'Смирнов', 'Антонов', 'Егоров', 'Иванов', 'Андреев',
                  'Александров', 'Павлов', 'Кузнецов', 'Михайлов', 'Васильев']
    middle_names = ['Александрович', 'Данилович', 'Егорович', 'Ефимович', 'Иванович',
                    'Евгеньевич', 'Анатольевич', 'Викторович', 'Владимирович', 'Витальевич']

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            ['last_name', 'first_name', 'middle_name', 'organization', 'work_phone_number',
             'personal_phone_number'])

        for _ in range(records_count):
            lastname = random.choice(lastnames)
            firstname = random.choice(firstnames)
            middle_name = random.choice(middle_names)
            organization = f'Organization-{random.randint(0, records_count)}'
            work_phone_number = (f'+7-{random.randint(100, 999)}-'
                                 f'{random.randint(100, 999)}-'
                                 f'{random.randint(1000, 9999)}')
            personal_phone_number = (f'+7-{random.randint(100, 999)}-'
                                     f'{random.randint(100, 999)}-'
                                     f'{random.randint(1000, 9999)}')

            writer.writerow([lastname, firstname, middle_name, organization, work_phone_number,
                             personal_phone_number])


if __name__ == '__main__':
    generate_test_data('phone_book_storage.csv')
