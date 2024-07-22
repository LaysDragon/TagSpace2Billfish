from dataclasses import dataclass
from typing import List


@dataclass
class Tag:
    title: str
    color: str
    textcolor: str
    type: str


@dataclass
class TagGroup:
    title: str
    children: List[Tag]


@dataclass
class FileTS:
    file: str
    tags:List[str]