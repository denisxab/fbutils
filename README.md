# Драйвер для работы с `Firebird`

**Пример использования**

```python
from fbutils.fb_base311 import FB, Fetch

con = FB.connect(
    'localhost:Алиас',
    user='sysdba',
    password='masterkey',
)

fb = FB(
    con
    # Тип получения ответа для одной записи
    , func_fetchOne=Fetch.One.namedtuplefetch
    # Тип получения ответа для нескольких записи
    , func_fetchAll=Fetch.All.dictfetch
)


def create_database():
    print("CREATE DATABASE '/home/denis/fb/test2.fdb';")


def create_table():
    fb.writeOne("""
    create table DIAGLINKS
    (
        DIAGLINKID int,
        DICID int,
        REFID int,
        DGCODE int not null,
        SORTORDER int,
        UID int,
        MODIFYDATE date,
        FILIAL int,
        F25_COLOR int,
        constraint PK_DIAGLINKS primary key (DIAGLINKID)
    );
    """)


def insert_into_from_table():
    fb.writeMany(
        "insert into DIAGLINKS (DIAGLINKID,DICID,REFID,DGCODE) values (?,?,?,?)",
        params=[
            (11, 2, 3, 4),
            (22, 2, 3, 4),
            (33, 2, 3, 4),
            (44, 2, 3, 4),
            (55, 2, 3, 4),
        ]
    )


def read_table_all():
    res = fb.readAll("select * from DIAGLINKS")
    print(res)


def read_table_one():
    for x in fb.readRow("select * from DIAGLINKS"):
        print(x)

if __name__ == '__main__':
    # insert_into_from_table()
    read_table_one()
    read_table_all()

```
