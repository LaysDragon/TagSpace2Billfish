import sqlite3
from dataclasses import dataclass
from typing import List, Optional
import time


@dataclass(kw_only=True)
class TagV2:
    id: Optional[int] = None
    name: str
    pid: int = 0
    seq: float = 0.900001
    icon: int = 0
    color: int = 0
    born: int = int(time.time())


@dataclass(kw_only=True)
class TagJoinFile:
    id: Optional[int] = None
    fileId: int
    tagId: int
    born: int = int(time.time())


@dataclass(kw_only=True)
class BfFile:
    id: Optional[int] = None
    name: str


class BillFishDB:
    coon: Optional[sqlite3.Connection]
    db_path: str

    def __init__(self, path: str):
        self.db_path = path

    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row

    def add_tag(self, tag: TagV2) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO bf_tag_v2 (name,pid,seq,icon,color,born) VALUES(?, ?, ?, ?, ?, ?)",
            (tag.name, tag.pid, tag.seq, tag.icon, tag.color, tag.born),
        )
        self.conn.commit()
        return cursor.lastrowid

    def find_tag_id(self, name: str) -> None | int:
        cursor = self.conn.cursor()
        row = cursor.execute(
            "SELECT * FROM bf_tag_v2 WHERE name = ?", (name,)
        ).fetchone()
        if row is None:
            return None
        return row["id"]

    def join_file_tag(self, fid: int, tid: int) -> int:
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO bf_tag_join_file (file_id,tag_id,born) VALUES(?, ?, ?)",
            (fid, tid, int(time.time())),
        )
        self.conn.commit()
        return cursor.lastrowid

    def get_all_file(self) -> List[BfFile]:
        cursor = self.conn.cursor()
        rows = cursor.execute("SELECT id, name FROM bf_file").fetchall()
        return [BfFile(id=r["id"], name=r["name"]) for r in rows]
