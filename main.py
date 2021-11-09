import sys
import time

import psycopg2
import threading

DB = 'postgres'
USER = 'postgres'
PASS = '123'
IP = 'localhost'

counter = 1
mutex = threading.Lock()
flush = False
thread_count = 10


def get_next():
    global counter
    # в этот блок может войти только один поток одновременно
    with mutex:
        last = counter
        counter += 1
    return last


def worker(thread_id, filename):
    # открываем соединение на каждый воркер
    conn = psycopg2.connect(dbname=DB, user=USER, password=PASS, host=IP)
    cur = conn.cursor()

    # открываем файл
    f = open(filename, 'w')

    while True:
        # берем 1 запись с id, который получили из get_next()
        # БД сделана так, что id идут с 1 по порядку до миллиона
        pos = get_next()
        cur.execute("SELECT id, data FROM test WHERE id={} LIMIT 1".format(pos))
        # получаем первую запись. у нас она и так вернется одна
        data = cur.fetchone()
        # в тот момент, когда записей больше нет, прекращаем
        if data is None:
            break
        # пишем в файлик thread_id и то, что прилетело с базы
        f.write("{}| {} {}\n".format(thread_id, data[0], data[1]))
        # сбрасываем на диск если установлен флаг
        if flush:
            f.flush()
    # закрываем соединение и файлы
    conn.close()
    f.close()


if __name__ == '__main__':
    # выполняется слева направо, если первое условие true то дальше не проверяется
    if len(sys.argv) == 2 and sys.argv[1] == 'flush':
        flush = True
    thread_list = []
    for a in range(thread_count):
        thread_list.append(threading.Thread(target=worker, args=(a, "dump{}_{}".format(
            a, "flush" if flush else "not"
        ))))

    begin_time = time.time()
    # запускаем потоки
    for a in thread_list:
        a.start()
    # дожидаемся завершения
    for a in thread_list:
        a.join()

    print("Execution time takes", time.time() - begin_time, "seconds")
