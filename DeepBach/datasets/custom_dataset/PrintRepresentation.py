import os
import pickle

pickled_dataset = "DataWithoutChords.pickle"

X, X_metadatas, voice_ids, index2notes, note2indexes, metadatas = pickle.load(
        open(pickled_dataset, 'rb'))
print(X)
print(X_metadatas)
print(voice_ids)
print(index2notes)
print(note2indexes)
print(metadatas)
