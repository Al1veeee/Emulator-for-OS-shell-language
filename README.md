# Конфигурационное управление

## **Цель задание:**

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.
Эмулятор должен запускаться из реальной командной строки, а файл с
виртуальной файловой системой не нужно распаковывать у пользователя.
Эмулятор принимает образ виртуальной файловой системы в виде файла формата
tar. Эмулятор должен работать в режиме GUI.
Ключами командной строки задаются:


   - Путь к архиву виртуальной файловой системы.
   - Путь к лог-файлу.
   - Путь к стартовому скрипту.


Лог-файл имеет формат csv и содержит все действия во время последнего
сеанса работы с эмулятором.
Стартовый скрипт служит для начального выполнения заданного списка
команд из файла.
Необходимо поддержать в эмуляторе команды ls, cd и exit, а также
следующие команды:

   - ```date```
   - ```echo```
   - ```cal```


Все функции эмулятора должны быть покрыты тестами, а для каждой из
поддерживаемых команд необходимо написать 2 теста.

Проект поддерживает выполнение команд из текстового файла-скрипта. Каждая строка файла интерпретируется как команда, что упрощает автоматизацию операций.


## **Описание проекта**


Эмулятор предназначен для запуска из командной строки, симулируя работу с виртуальной файловой системой, хранящейся в архиве формата tar. Программа работает в графическом интерфейсе (GUI) и должна максимально имитировать поведение сеанса shell в UNIX-подобных ОС.

Эмулятор поддерживает работу с виртуальной файловой системой, предоставляя пользователю возможность выполнения базовых команд (ls, cd, exit), а также дополнительных команд для вывода информации (date, echo, cal).


## **Ключевые особенности:**

   - **Поддержка командной строки:** Эмулятор принимает несколько параметров при запуске:
     

      - Путь к архиву виртуальной файловой системы (в формате tar).
      - Путь к лог-файлу, куда записываются все действия в формате CSV.
      - Путь к стартовому скрипту, содержащему список команд для начального выполнения.
    
   - **Виртуальная файловая система:** Эмулятор загружает виртуальную файловую систему из tar-архива, не требуя её разархивации на диске.


   - **Команды:** Поддерживаются стандартные команды:

      - ```ls``` — список файлов в текущей директории.
      - ```cd``` — смена текущей директории.
      - ```exit``` — завершение сеанса работы.


   - **Логирование:** Все команды и результаты их выполнения логируются в CSV-файл.

   - **Стартовый скрипт:** При запуске можно указать файл со списком команд, которые должны быть выполнены сразу после запуска эмулятора.

   - **GUI:** Эмулятор работает в графическом интерфейсе, предлагая удобный способ взаимодействия с виртуальной файловой системой и выполнения команд.


# Структура проекта


## Основные компоненты:


1. **Архив виртуальной файловой системы** — tar-файл, представляющий виртуальную файловую систему.


2. Лог-файл — CSV-файл, в который записываются действия пользователя и их результаты.


3. Стартовый скрипт — текстовый файл, содержащий команды, которые выполняются после запуска эмулятора.


4. GUI — графический интерфейс для работы пользователя.


## Команды:


```ls:``` Отображение списка файлов и папок в текущей директории.


```cd:``` Переход в другую директорию.


```exit:``` Завершение сеанса работы с эмулятором.


```date:``` Вывод текущей даты и времени в формате YYYY-MM-DD HH:MM:SS.


```echo [текст]:``` Вывод заданного текста на экран.


```cal:``` Отображение календаря текущего месяца.


## Лог-файл:
Лог-файл создается или обновляется при каждом сеансе работы. Формат CSV содержит следующие поля:


   - Время выполнения команды.
   - Название команды.


Пример лог-файла:
```
Date, Command
2024-10-17 13:33:36, pwd
2024-10-17 13:33:50, cd tests
2024-10-17 13:34:00, ls
```

## Стартовый скрипт:
Стартовый скрипт содержит список команд, которые будут выполнены при запуске программы. Команды указываются в файле построчно.

Пример файла стартового скрипта:

```
pwd
cd tests
cat test1.txt
cat test2.txt
cat test3.txt
ls
date
echo "Hello World"
cal
```


### Пример выполнения команд:

Команда python main.py tests.tar --log log.csv --script script.txt запускает эмулятор, указанный в файле main.py, с следующими параметрами:

   - ```tests.tar``` — путь к файлу архива, представляющему виртуальную файловую систему. Эмулятор загружает этот архив для работы с файловой системой.

   - ```--log log.csv``` — ключ --log указывает путь к лог-файлу, где будут сохраняться все действия, выполняемые во время работы эмулятора. В данном случае все действия будут записываться в файл log.csv.

   - ```--script script.txt``` — ключ --script указывает путь к стартовому скрипту, который содержит список команд для автоматического выполнения при запуске эмулятора. Команды из файла script.txt будут выполнены сразу после загрузки виртуальной файловой системы.


### В файле script.txt находятся команды реализованные в main.py

![image](https://github.com/user-attachments/assets/a75110c5-b21b-4f94-8d18-33a4b8482a93)

### Команда: ```python main.py tests.tar --log log.csv --script script.txt```

![image](https://github.com/user-attachments/assets/b1be8901-056b-4578-aeb7-b6368107e967)

### Команды: ```cd tests``` — переходит в поддиректорию tests и ```ls``` — выводит список файлов и директорий в текущей директории.
![image](https://github.com/user-attachments/assets/04460853-21f0-487e-bb87-f1b2b8a2cefb)


### Команда: ```pwd``` — выводит текущий путь (директорию), в которой вы находитесь.

![image](https://github.com/user-attachments/assets/d265797b-059d-43b2-815c-46cd8df91d2b)

### Команды:
```
cat test1.txt — выводит содержимое файла test1.txt на экран.
cat test2.txt — выводит содержимое файла test2.txt на экран.
cat test3.txt — выводит содержимое файла test3.txt на экран.
```
![image](https://github.com/user-attachments/assets/f6e24443-2055-4d7d-8cc8-431d2d25a6b3)

### Команда: ```date``` — выводит текущую дату и время.
![image](https://github.com/user-attachments/assets/e327eea6-017e-492e-87ef-38652c70c645)

### Команда: ```cal``` — выводит календарь текущего месяца
![image](https://github.com/user-attachments/assets/616085a1-2e65-41f8-9fc3-92120801eb9b)

### Команда: ```echo "Hello World"``` — выводит на экран строку "Hello World".
![image](https://github.com/user-attachments/assets/7c17234d-a28f-4f3b-a77c-4a7cf368e15d)


# Тестирование с помощью unittest:


```unittest``` — это встроенный модуль Python, который позволяет разработчикам создавать и выполнять тесты. Этот фреймворк помогает автоматизировать процесс тестирования, гарантируя, что функции вашего кода работают корректно и без ошибок.


### Тестирование осуществляется в классе TestShellCommands, который наследует от unittest.TestCase. В нем описаны следующие тесты:

1. Тесты для команды ```ls```


   - Проверка содержимого корневого каталога.


   - Проверка содержимого каталога tests.


2. Тесты для команды ```cd```


   - Переход в существующий каталог.


   - Попытка перехода в несуществующий каталог.


3. Тесты для команды ```cat```


   - Чтение содержимого существующего файла.


   - Попытка чтения несуществующего файла.


4. Тесты для команды ```echo```


   - Вывод простого текста.


   - Вывод пустой строки.


5. Тест для команды ```date```


   - Проверка корректного формата текущей даты.


6. Тест для команды ```cal```


   - Проверка вывода текущего месяца.


### Код тестов:
![image](https://github.com/user-attachments/assets/6c71eeb4-ab54-4061-a64f-db981d58dde8)

### Результаты тестирования: 
Ввод: ```python -m unittest -v test_commands.py```

После выполнения тестов, были получены следующие результаты:


Все тесты для команд ls, cat, echo, date и cal прошли успешно.


Тесты для команды cd показали, что:


   - Переход в существующий каталог работает корректно.


   - Попытка перехода в несуществующий каталог также правильно обрабатывается.

![image](https://github.com/user-attachments/assets/d89854cc-1f23-40d5-81f2-62465be19509)
