import pytest
import tarfile
from main import ls, cd, cat, echo, date, cal
import os
import calendar
from datetime import datetime

@pytest.fixture
def all_files():
    tar_file_path = r'C:\Users\User\Desktop\konf\tests.tar'
    with tarfile.open(tar_file_path) as tar:
        return tar.getmembers()

@pytest.fixture
def local_path():
    return ''

def test_ls_root_directory(all_files, local_path):
    items = ls(local_path, all_files)
    assert items == ['tests']

def test_ls_tests_directory(all_files):
    items = ls('tests', all_files)
    assert items == ['test1.txt', 'test2.txt', 'test3.txt']

def test_cd_to_existing_directory(all_files, local_path):
    assert cd(local_path, 'tests', all_files) is True

def test_cd_to_non_existing_directory(all_files, local_path):
    assert cd(local_path, 'non_existing_folder', all_files) is False

def test_cat_existing_file():
    result = cat('', 'tests/test1.txt', r'C:\Users\User\Desktop\konf\tests.tar')
    assert isinstance(result, str)

def test_cat_non_existing_file():
    result = cat('', 'tests/non_existing_file.txt', r'C:\Users\User\Desktop\konf\tests.tar')
    assert result == "Can't open this file"

def test_echo_simple_text():
    result = echo("Hello, World!")
    assert result == "Hello, World!"

def test_echo_empty_text():
    result = echo("")
    assert result == ""

def test_date_format():
    result = date()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    assert result == current_date

def test_cal_output():
    result = cal()
    assert result == calendar.month(datetime.now().year, datetime.now().month)
