# Конфигурационное управление
----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

Эмулятор для языка оболочки ОС. Работа сделана как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор запускается из реальной командной строки, а файл с
виртуальной файловой системой не распаковывается у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор работает в режиме GUI.

Основное назначение проекта — работа с файлами в формате TAR-архива, что может быть полезно для анализа содержимого архивов без необходимости их предварительной распаковки.

Пример команды для работы с TAR-архивом:

python3 main.py tests.tar --log log.csv --script script.txt

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Данный проект представляет собой эмулятор командной оболочки, написанный на языке Python. Он предназначен для выполнения различных команд, похожих на команды оболочки UNIX, таких как:


ls: вывод списка файлов в директории,

cd: смена директории,

cat: вывод содержимого файлов,

date: вывод текущей даты и времени,

echo: вывод строки,

cal: вывод календаря текущего месяца.

----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Функциональные возможности

Список файлов (ls) Команда выводит содержимое директории. Работает с архивами TAR и может выводить содержимое директории или архива без его распаковки.

Смена директории (cd) Позволяет перемещаться между "директориями" внутри TAR-архива. Поддерживается возврат в родительскую директорию с помощью команды cd .., а также переход в корневую директорию через cd ~.

Вывод содержимого файла (cat) Выводит содержимое файла в TAR-архиве. Если файл не найден, возвращается соответствующее сообщение об ошибке.

Вывод даты и времени (date) Команда выводит текущие дату и время в формате YYYY-MM-DD HH:MM:SS.

Эхо-команда (echo) Выводит переданную строку текста.

Календарь (cal) Выводит календарь для текущего месяца.

Проект поддерживает выполнение команд из текстового файла-скрипта. Каждая строка файла интерпретируется как команда, что упрощает автоматизацию операций.

