from typing import List
import csv
from expertise.ownership import PersonalOwnership


def ownership2csv(ownerships: List[PersonalOwnership], output_path: str):
    if isinstance(ownerships, list):
        # TODO: mind if the name of ownership cannot be encoded by utf-8
        with open(output_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f)
            for ownership in ownerships:
                writer.writerow(ownership.tolist())


def pullrequest2csv(collaboration, path):
    pass
