import sqlite3

con = sqlite3.connect(":memory:")

# 확장 로드를 활성화합니다
con.enable_load_extension(True)

# 전체 텍스트 검색 확장을 로드합니다
con.execute("select load_extension('./fts3.so')")

# 대신 API 호출을 사용하여 확장을 로드할 수도 있습니다:
# con.load_extension("./fts3.so")

# 확장 로드를 다시 비활성화합니다
con.enable_load_extension(False)

# SQLite 위키의 예제
con.execute("create virtual table recipe using fts3(name, ingredients)")
con.executescript("""
    insert into recipe (name, ingredients) values ('broccoli stew', 'broccoli peppers cheese tomatoes');
    insert into recipe (name, ingredients) values ('pumpkin stew', 'pumpkin onions garlic celery');
    insert into recipe (name, ingredients) values ('broccoli pie', 'broccoli cheese onions flour');
    insert into recipe (name, ingredients) values ('pumpkin pie', 'pumpkin sugar flour butter');
    """)
for row in con.execute("select rowid, name, ingredients from recipe where name match 'pie'"):
    print(row)
