import sqlite3

con = sqlite3.connect(":memory:")
con.execute("create table person (id integer primary key, firstname varchar unique)")

# 성공적입니다, con.commit()이 자동으로 나중에 호출됩니다
with con:
    con.execute("insert into person(firstname) values (?)", ("Joe",))

# with 블록이 예외로 끝난 후에 con.rollback()이 호출됩니다, 예외는 여전히 발생하고, 잡아야 합니다
try:
    with con:
        con.execute("insert into person(firstname) values (?)", ("Joe",))
except sqlite3.IntegrityError:
    print("couldn't add Joe twice")
