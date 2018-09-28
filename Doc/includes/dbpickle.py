# 지속성 ID를 외부 객체를 참조로 피클 하는데 사용하는 방법을 보여주는 간단한 예제.

import pickle
import sqlite3
from collections import namedtuple

# 우리 데이터베이스의 레코드를 나타내는 간단한 클래스.
MemoRecord = namedtuple("MemoRecord", "key, task")

class DBPickler(pickle.Pickler):

    def persistent_id(self, obj):
        # MemoRecord를 일반 클래스 인스턴스로 피클 하는 대신, 지속성 ID를 출력합니다.
        if isinstance(obj, MemoRecord):
            # 여기서, 우리의 지속성 ID는 태그와 데이터베이스의 특정 레코드를 참조하는 키를 포함하는
            # 단순한 튜플입니다.
            return ("MemoRecord", obj.key)
        else:
            # obj에 지속성 ID가 없으면, None을 반환합니다. 이것은 obj가 평소와 같이 피클 되어야
            # 함을 의미합니다.
            return None


class DBUnpickler(pickle.Unpickler):

    def __init__(self, file, connection):
        super().__init__(file)
        self.connection = connection

    def persistent_load(self, pid):
        # 이 메서드는, 지속성 ID를 만날 때마다 호출됩니다.
        # 여기에서, pid는 DBPickler가 반환한 튜플입니다.
        cursor = self.connection.cursor()
        type_tag, key_id = pid
        if type_tag == "MemoRecord":
            # 데이터베이스에서 참조 된 레코드를 반입하여 리턴하십시오.
            cursor.execute("SELECT * FROM memos WHERE key=?", (str(key_id),))
            key, task = cursor.fetchone()
            return MemoRecord(key, task)
        else:
            # 올바른 객체를 반환할 수 없으면 항상 에러를 일으켜야 합니다. 그렇지 않으면, 언피클러는
            # None이 지속성 ID에 의해 참조되는 객체라고 생각할 것입니다.
            raise pickle.UnpicklingError("unsupported persistent object")


def main():
    import io
    import pprint

    # 데이터베이스를 초기화하고 값을 채웁니다.
    conn = sqlite3.connect(":memory:")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE memos(key INTEGER PRIMARY KEY, task TEXT)")
    tasks = (
        'give food to fish',
        'prepare group meeting',
        'fight with a zebra',
        )
    for task in tasks:
        cursor.execute("INSERT INTO memos VALUES(NULL, ?)", (task,))

    # 피클 할 레코드를 가져옵니다.
    cursor.execute("SELECT * FROM memos")
    memos = [MemoRecord(key, task) for key, task in cursor]
    # 사용자 정의 DBPickler를 사용하여 레코드를 저장합니다.
    file = io.BytesIO()
    DBPickler(file).dump(memos)

    print("Pickled records:")
    pprint.pprint(memos)

    # 확인을 위해 레코드를 갱신합니다.
    cursor.execute("UPDATE memos SET task='learn italian' WHERE key=1")

    # 피클 데이터 스트림에서 레코드를 로드합니다.
    file.seek(0)
    memos = DBUnpickler(file, conn).load()

    print("Unpickled records:")
    pprint.pprint(memos)


if __name__ == '__main__':
    main()
