import stanza

nlp = stanza.Pipeline(lang='en', processors='tokenize, pos, lemma, ner')
with open("/home/yibsimo/PycharmProjects/Rokin_Dev/quantum_titles") as infile:
    for line in infile:
        doc = nlp(line)
        print(*[f'entity: {ent.text}\ttype: {ent.type}' for sent in doc.sentences for ent in sent.ents], sep='\n')