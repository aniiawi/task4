import hashlib

if __name__ == '__main__':
    t = open('db.sql', 'w')
    t.write('''
DROP TABLE IF EXISTS test;
CREATE TABLE test(
        id INT,
        data varchar(64)
);
CREATE INDEX ON test(id);
INSERT INTO test VALUES
''')
    a = 1
    while True:
        t.write("({}, '{}')".format(a, hashlib.sha256(str(a).encode('utf-8')).hexdigest()))
        if a == 1000001:
            t.write(";")
            break
        else:
            t.write(",\n")
        a += 1

