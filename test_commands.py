import unittest
import tarfile
import os
import calendar
from datetime import datetime
from main import ls, cd, cat, echo, date, cal


class TestShellCommands(unittest.TestCase):

    def setUp(self):
        # Задаем путь к архиву
        self.tar_file_path = r'C:\Users\User\Desktop\konf\tests.tar'

        # Открываем tar файл для тестов
        with tarfile.open(self.tar_file_path) as tar:
            self.all_files = tar.getmembers()

        # Устанавливаем начальный local_path
        self.local_path = ''

    # Тесты для команды ls
    def test_ls_root_directory(self):
        items = ls(self.local_path, self.all_files)
        self.assertListEqual(items, ['tests'])

    def test_ls_tests_directory(self):
        items = ls('tests', self.all_files)
        self.assertListEqual(items, ['test1.txt', 'test2.txt', 'test3.txt'])

    # Тесты для команды cd
    def test_cd_to_existing_directory(self):
        success = cd(self.local_path, 'tests', self.all_files)
        self.assertTrue(success)
        self.local_path = 'tests'  # Обновляем local_path

    def test_cd_to_non_existing_directory(self):
        success = cd(self.local_path, 'non_existing_folder', self.all_files)
        self.assertFalse(success)

    # Тест для команды cat
    def test_cat_existing_file(self):
        result = cat('', 'tests/test1.txt', self.tar_file_path)
        self.assertIsInstance(result, str)  # Проверяем, что возвращается строка

    def test_cat_non_existing_file(self):
        result = cat('', 'tests/non_existing_file.txt', self.tar_file_path)
        self.assertEqual(result, "Can't open this file")

    # Тесты для команды echo
    def test_echo_simple_text(self):
        result = echo("Hello, World!")
        self.assertEqual(result, "Hello, World!")

    def test_echo_empty_text(self):
        result = echo("")
        self.assertEqual(result, "")

    # Тест для команды date
    def test_date_format(self):
        result = date()
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.assertEqual(result, current_date)

    # Тест для команды cal
    def test_cal_output(self):
        result = cal()
        self.assertEqual(result, calendar.month(datetime.now().year, datetime.now().month))


if __name__ == '__main__':
    unittest.main()
