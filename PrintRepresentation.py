import pickle
import sys
from DeepBach.metadata import *
from DeepBach import *
from metadata import *
from functions import *

def main(pickled_dataset):
	print("You are reading:", pickled_dataset)
	X, X_metadatas, voice_ids, index2notes, note2indexes, metadatas = pickle.load(open(pickled_dataset, 'rb'))
	print("X:", X)
	print("X_metadatas:", X_metadatas)
	print("voice_ids:", voice_ids)
	print("index2notes:", index2notes)
	print("note2indexes", note2indexes)
	print("metadatas:", metadatas)

if __name__ == "__main__":

	if len(sys.argv) == 2:
		main(sys.argv[1])
	else:
		print("Usage: Python3 PrintRepresentation <file.pickle>")


