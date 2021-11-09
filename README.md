Команда Press F, группа Т12О-101М-21: Фадеева Анна, Тищенко Кирилл, Зварич Василина

1. С помощью файла gensql.py генерируем требуемую базу данных, создается файл db.sql с таблицей, состоящей из двух колонок - номера строки и произвольного набора символов (sha256 хеш от строки из этого числа).
2. Далее вводим команду psql -d postgres -U postgres -f db.sql, так мы импортируем сгенерированную БД в Postgres.
3. К БД мы подключаемся локально, устанавливая DB_HOST = 'localhost'. Также для работы с Postrgres нам потребуется установить модуль psycopg2.
4. Запускаем файл main.py. С помощью функции worker() проивзодится работа с потоками - каждый поток подключается к БД и производится запись в файл. Если была произведена запись в буфер, то в конец названия файла добавляется not, если сбрасываем на диск - flush.
Результаты выполнения и примеры файлов доступны по ссылке https://disk.yandex.ru/d/osJs8idvgJ941w
В первом случае (с буфером) результирующее время было ~179,79 секунд, во втором случае (без буфера) ~200,79. Во втором случае время увеличено, так как производится больше операций записи.
