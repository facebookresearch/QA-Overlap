# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""Download data for calculating question overlap"""
import wget
import os


DIRNAME = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DIRNAME, 'data')

TEST_SETS_TO_DOWNLOAD = [
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/nq-test.qa.csv','nq-test.qa.csv'),
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/triviaqa-test.qa.csv', 'triviaqa-test.qa.csv'),
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/webquestions-test.qa.csv', 'webquestions-test.qa.csv'),
]
ANNOTATIONS_TO_DOWNLOAD = [
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/nq-annotations.jsonl','nq-annotations.jsonl'),
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/triviaqa-annotations.jsonl', 'triviaqa-annotations.jsonl'),
    ('https://dl.fbaipublicfiles.com/qaoverlap/data/webquestions-annotations.jsonl','webquestions-annotations.jsonl')
]

os.makedirs(DATA_DIR, exist_ok=True)
for link, dest in TEST_SETS_TO_DOWNLOAD:
    wget.download(link, os.path.join(DATA_DIR, dest))

for link, dest in ANNOTATIONS_TO_DOWNLOAD:
    wget.download(link, os.path.join(DATA_DIR, dest))
