# QA-Overlap

This repository contains code to support the research paper [Question and Answer Test-Train Overlap in Open-Domain Question Answering Datasets](.)

<br>
<p align="center">
  <img src="https://dl.fbaipublicfiles.com/MLQA/logos.png" alt="Facebook AI Research and UCL NLP"  width="60%"/>
  <br>
</p>
<br>

This repository contains both links to download annotations, and an evaluation script to reproduce our evaluation methods.

## Data downloads

Data can be dowloaded by running the `download.py` script,
or to download the annotations manually, you can download the links here: 
* [Natural Questions](https://dl.fbaipublicfiles.com/qaoverlap/data/nq-annotations.jsonl)
* [TriviaQA](https://dl.fbaipublicfiles.com/qaoverlap/data/triviaqa-annotations.jsonl)
* [WebQuestions](https://dl.fbaipublicfiles.com/qaoverlap/data/webquestions-annotations.jsonl)

The annoations are in jsonl format. We recommend using them with our provided evaluation scripts

## Evaluating your model's Test predictions with our splits

To evaluate your model, first download the data using the download script

```
pip install -r requirements
python download.py
```
Then, you can get scores for your models for all QA subsets by running `evaluate.py`

```
$ python evaluate.py -h
usage: evaluate.py [-h] [--predictions PREDICTIONS]
                   [--dataset_name {naturalquestions,triviaqa,webquestions}]

optional arguments:
  -h, --help            show this help message and exit
  --predictions PREDICTIONS
                        path to predictions txt file, one answer per line.
                        Answer order should follow the order in
                        data/{dataset}-test.qa.csv
  --dataset_name {naturalquestions,triviaqa,webquestions}
                        name of datset to evaluate on
```

You will see an output like this:

```
$ python evaluate.py --predictions rag_nq_predictions.txt --dataset_name nq
--------------------------------------------------
Label       : total
N examples  :  3610
Exact Match :  44.48753462603878
--------------------------------------------------
Label       : question_overlap
N examples  :  324
Exact Match :  70.67901234567901
--------------------------------------------------
Label       : no_question_overlap
N examples  :  672
Exact Match :  31.101190476190474
--------------------------------------------------
Label       : answer_overlap
N examples  :  2297
Exact Match :  55.72485851110144
--------------------------------------------------
Label       : no_answer_overlap
N examples  :  1313
Exact Match :  24.828636709824828
--------------------------------------------------
Label       : answer_overlap_only
N examples  :  315
Exact Match :  34.92063492063492
```

## License

The code in this repository is licenced according the LICENSE file.