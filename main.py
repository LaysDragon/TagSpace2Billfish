import glob
import json
from pathlib import Path
from typing import Dict, List
import TagSpace
import BillfishDB

TARGETFOLDER_PATH = "./"
DATABASE_PATH = "./billfish.db"
TAG_FILE_PATH = "./tag-library.json"


tags_collection: List[TagSpace.TagGroup] = []
file_tags: Dict[str, TagSpace.FileTS] = {}

print(f"loading TagSpace tag collection from {TAG_FILE_PATH}...")
with open(TAG_FILE_PATH, encoding="utf-8") as f:
    data = json.load(f)

    tags_collection = [
        TagSpace.TagGroup(
            title=g["title"],
            children=[
                TagSpace.Tag(
                    color=t["color"],
                    textcolor=t["textcolor"],
                    title=t["title"],
                    type=t["type"],
                )
                for t in g["children"]
            ],
        )
        for g in data["tagGroups"]
    ]


print(f"loading TagSpace TS data from {TARGETFOLDER_PATH}...")
for file in glob.glob(TARGETFOLDER_PATH + "/**/.ts/*.json"):
    with open(file, encoding="utf-8-sig") as f:
        name = Path(file).stem
        data = json.load(f)
        if name in file_tags:
            raise "重複檔名"
        file_tags[name] = TagSpace.FileTS(
            file=name, tags=[t["title"] for t in data["tags"]]
        )

db = BillfishDB.BillFishDB(DATABASE_PATH)
db.connect()

print(f"writing tags into database {DATABASE_PATH}...")
for tagGroup in tags_collection:
    gid = db.add_tag(BillfishDB.TagV2(name=tagGroup.title))
    for tag in tagGroup.children:
        db.add_tag(BillfishDB.TagV2(name=tag.title, pid=gid))


print(f"writing file tag into database {DATABASE_PATH}...")
for file in db.get_all_file():
    if file.name not in file_tags:
        continue
    tags = file_tags[file.name]
    print(f"writing {file.name} -> {','.join(tags.tags)}")
    for tag in tags.tags:
        tid = db.find_tag_id(tag)
        db.join_file_tag(file.id, tid)
