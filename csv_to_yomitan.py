from collections.abc import Iterator, Mapping
import csv
import json
import sys
from typing import Final, TypeAlias, TypedDict, cast


class Row(TypedDict):
    headword: str
    pos: str
    cefr: str
    core_inventory1: str
    core_inventory2: str
    threshold: str


class Value(TypedDict):
    value: int
    displayValue: str


FreqRecord: TypeAlias = tuple[str, str, Value]


GRADES: Final[Mapping[str, int]] = {
    "A1": 1,
    "A2": 2,
    "B1": 3,
    "B2": 4,
    "C1": 5,
    "C2": 6,
}


def read(reader: Iterator[Row]) -> Iterator[FreqRecord]:
    for row in reader:
        cefr = row["cefr"]
        yield row["headword"], "freq", Value(value=GRADES[cefr], displayValue=cefr)


def main() -> int:
    word_list = cast(
        Iterator[Row],
        csv.DictReader(
            sys.stdin,
            fieldnames=tuple(Row.__annotations__.keys()),
            delimiter=";",
            lineterminator="\n",
        ),
    )
    res = 0

    try:
        _ = next(word_list)
    except StopIteration:
        print("Error: CSV has no header", file=sys.stderr)
        return 1

    print("[", end="")
    for i, record in enumerate(read(word_list)):
        if i > 0:
            print(",", end="")
        try:
            print(flush=True)
            json.dump(record, sys.stdout)
        except BrokenPipeError:
            return 1
        except Exception as e:
            print("Error:", e, file=sys.stderr)
            res = 1
            break
    print("]", flush=True)

    return res


if __name__ == "__main__":
    sys.exit(main())
