import sqlite3

persons = [
    ("Hugo", "Boss"),
    ("Calvin", "Klein")
    ]

con = sqlite3.connect(":memory:")

# 테이블을 만듭니다
con.execute("create table person(firstname, lastname)")

# 테이블을 채웁니다
con.executemany("insert into person(firstname, lastname) values (?, ?)", persons)

# 테이블의 내용을 인쇄합니다
for row in con.execute("select firstname, lastname from person"):
    print(row)

print("I just deleted", con.execute("delete from person").rowcount, "rows")
