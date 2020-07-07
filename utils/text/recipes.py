from utils.files import get_files
from pathlib import Path
from typing import Union

def blizzard(path: Union[str, Path]):
    csv_file = get_files(path, extension='.csv')
    assert len(csv_file) == 1

    text_dict = {}

    with open(filepath, encoding='utf-8') as f  :
        content =  f.readlines()

    for line in content :
        split = line.split('|')
        text_dict[split[0]] = split[-1]

    return text_dict
