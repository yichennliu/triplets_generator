# Triplets Generation

Extract triplets from domain specific unstructured texts using Stanford OpenIE. Approach used here is based on: [From unstructured text to knowledge graph](https://github.com/varun196/knowledge_graph_from_unstructured_text)
Detailed information in documentation.

![Alt text](/home/yibsimo/PycharmProjects/Rokin_Dev/data/process.png?raw=true)

## Prerequisites

* Python 3.5 or later
* [Stanford CoreNLP](https://stanfordnlp.github.io/CoreNLP/download.html)
* [Gephi](https://gephi.org/users/download/) for visualization
* Dependencies in requirements.txt

```
pip install -r requirements.txt
```

## Steps

1. Extract articles from json file with data_extraction.py

2. Start Stanford CoreNLP server

```
cd stanford-corenlp-full-2015-12-09/
java -mx4g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
```

3. Tag the named entities of the extracted text with stanford_ner.py

4. Extract raw triplets with relation_extractor.py

5. Extract triplets with recognized named entities with create_structured_csv.py

6. Improve triplets with postprocessing.py

7. Run stat_parser.py to avoid triplet duplication

## Visualization with Gephi

Create node and edge files and import them into Gephi

```
python3 gephi_knowledge_graph.py amount_of_triplets node_file.csv edge_file.csv
```
