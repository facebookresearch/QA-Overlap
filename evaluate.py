# Copyright (c) 2020-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""Evaluation script to get prediction scores for overlapped QA pairs in ODQA datasets"""
from collections import Counter
import string
import re
import json
import os
import argparse


ANNOTATIONS = [
    'total',
    'question_overlap',
    'no_question_overlap',
    'answer_overlap',
    'no_answer_overlap',
    'answer_overlap_only'
]

DIRNAME = os.path.dirname(os.path.abspath(__file__))
REFERENCE_PATHS = {
    'triviaqa': os.path.join(DIRNAME, 'data/triviaqa-test.qa.csv'),
    'naturalquestions': os.path.join(DIRNAME, 'data/nq-test.qa.csv'),
    'webquestions': os.path.join(DIRNAME, 'data/webquestions-test.qa.csv'),
}
ANNOTATION_PATHS = {
    'triviaqa': os.path.join(DIRNAME, 'data/triviaqa-annotations.jsonl'),
    'naturalquestions': os.path.join(DIRNAME, 'data/nq-annotations.jsonl'),
    'webquestions': os.path.join(DIRNAME, 'data/webquestions-annotations.jsonl'),
}


def normalize_answer(s):
    """Lower text and remove punctuation, articles and extra whitespace."""
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def f1_score(prediction, ground_truth):
    prediction_tokens = normalize_answer(prediction).split()
    ground_truth_tokens = normalize_answer(ground_truth).split()
    common = Counter(prediction_tokens) & Counter(ground_truth_tokens)
    num_same = sum(common.values())
    if num_same == 0:
        return 0
    precision = 1.0 * num_same / len(prediction_tokens)
    recall = 1.0 * num_same / len(ground_truth_tokens)
    f1 = (2 * precision * recall) / (precision + recall)
    return f1


def exact_match_score(prediction, ground_truth):
    return (normalize_answer(prediction) == normalize_answer(ground_truth))


def metric_max_over_ground_truths(metric_fn, prediction, ground_truths):
    scores_for_ground_truths = []
    for ground_truth in ground_truths:
        score = metric_fn(prediction, ground_truth)
        scores_for_ground_truths.append(score)
    return max(scores_for_ground_truths)


def read_references(fi, sep='\t'):

    def parse_pandas_answer(a_string):
        # to avoid a pandas dependency, deserialize these manually
        try:
            parsed_answers = eval(a_string) if a_string.startswith('[') else eval(a_string.replace('""', '"')[1:-1])
        except:
            parsed_answers = eval(a_string.replace('""', '"').replace('""', '"').replace('""', '"')[1:-1])
        return parsed_answers

    references = []
    for i, line in enumerate(open(fi)):
        q, answer_str = line.strip('\n').split(sep)
        refs = parse_pandas_answer(answer_str)
        references.append({'references': refs, 'id':i})
    return references


def read_jsonl(path):
    with open(path) as f:
        return [json.loads(l) for l in f]


def read_lines(path):
    with open(path) as f:
        return [l.strip() for l in f]


def read_annotations(annotations_data_path):
    return read_jsonl(annotations_data_path)


def read_predictions(path):
    if path.endswith('json') or path.endswith('.jsonl'):
        return read_jsonl(path)
    else:
        return [{'id': i, 'prediction': pred} for i,pred in enumerate(read_lines(path))]


def _get_scores(answers, refs, fn):
    return [metric_max_over_ground_truths(fn, pred, rs) for pred, rs in zip(answers, refs)]


def get_scores(predictions, references, annotations, annotation_labels=None):
    predictions_map = {p['id']:p for p in predictions}
    references_map = {r['id']: r for r in references}
    annotations_map = {a['id']: a for a in annotations}
    assert predictions_map.keys() == references_map.keys(), 'predictions file doesnt match the gold references file '
    assert predictions_map.keys() == annotations_map.keys(), 'prediction file doesnt match the annotation file '
    assert annotations_map.keys() == references_map.keys(), 'annotations file doesnt match the gold references file '

    annotation_labels = ANNOTATIONS if annotation_labels is None else annotation_labels

    results = {}
    for annotation_label in annotation_labels:
        annotation_ids = [annotation['id'] for annotation in annotations if annotation_label in annotation['labels']]
        preds = [predictions_map[idd]['prediction'] for idd in annotation_ids]
        refs = [references_map[idd]['references'] for idd in annotation_ids]
        em = _get_scores(preds, refs, exact_match_score)
        f = _get_scores(preds, refs, f1_score)
        results[annotation_label] = {
            'exact_match': 100 * sum(em) / len(em),
            'f1_score': 100 * sum(f) / len(f),
            'n_examples': len(annotation_ids),
        }
    return results


def _print_score(label, results_dict):
    print('-'*50)
    print('Label       :' , label)
    print('N examples  : ', results_dict['n_examples'])
    print('Exact Match : ', results_dict['exact_match'])
    # print('F1 score    : ', results_dict['f1_score'])


def _main(predictions_path, references_path, annoations_path):
    predictions = read_predictions(predictions_path)
    references = read_references(references_path)
    annotations = read_annotations(annoations_path)
    scores = get_scores(predictions, references, annotations)
    for label in ANNOTATIONS:
        _print_score(label, scores[label])


def main(predictions_path, dataset_name):
    references_path = REFERENCE_PATHS[dataset_name]
    annotations_path = ANNOTATION_PATHS[dataset_name]
    if not os.path.exists(references_path):
        raise Exception(' References expected at ' + references_path
                        + ' not found, please download them using the download script (see readme)')
    if not os.path.exists(annotations_path):
        raise Exception(' Annotations expected at ' + annotations_path
                        + ' not found, please download them usiing the download script (see readme)')
    _main(predictions_path, references_path, annotations_path)


if  __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--predictions",
                        help="path to predictions txt file, one answer per line. "
                             "Answer order should follow the order in data/{dataset}-test.qa.csv", type=str)
    parser.add_argument('--dataset_name', choices=['naturalquestions', 'triviaqa', 'webquestions'], type=str,
                        help='name of datset to evaluate on')
    args = parser.parse_args()
    main(args.predictions, args.dataset_name)