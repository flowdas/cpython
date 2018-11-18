import sqlite3

con = sqlite3.connect(":memory:")
cur = con.cursor()

AUSTRIA = "\xd6sterreich"

# 기본적으로, 행은 유니코드로 반환됩니다
cur.execute("select ?", (AUSTRIA,))
row = cur.fetchone()
assert row[0] == AUSTRIA

# 하지만 우리는 sqlite3가 항상 바이트열을 반환하도록 할 수 있습니다 ...
con.text_factory = bytes
cur.execute("select ?", (AUSTRIA,))
row = cur.fetchone()
assert type(row[0]) is bytes
# 여러분이 데이터베이스에 쓰레기를 저장하지 않는 이상, 바이트열은 UTF-8로 인코딩될 것입니다 ...
assert row[0] == AUSTRIA.encode("utf-8")

# 우리는 또한 사용자 정의 text_factory를 구현할 수 있습니다 ...
# 여기서 모든 문자열에 "foo"를 추가하는 것을 구현합니다
con.text_factory = lambda x: x.decode("utf-8") + "foo"
cur.execute("select ?", ("bar",))
row = cur.fetchone()
assert row[0] == "barfoo"
