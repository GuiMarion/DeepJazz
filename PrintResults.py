import pickle
import sys
from DeepBach.metadata import *
from DeepBach import *
from metadata import *
from MusicChordExtraction.functions import *

def main(name):
    print("You are reading:", name)
    seq = pickle.load(open("Results/"+name, 'rb'))
    seq = [np.transpose(seq, axes=(1, 0))]
    picklefile = "DeepBach/datasets/custom_dataset/"+ name + ".pickle"
    X, X_metadatas, voice_ids, index2notes, note2indexes, metadatas = pickle.load(open(picklefile, 'rb'))

    print(seq)

    for elem in seq:
        Compt = 0

        for i in range(len(elem[0])):
            if Compt == 16:
                Compt = 0
                print()
                for e in range(i-16, i):
                    print(index2notes[1][int(elem[1][e])], end="")
                print()
                for e in range(i-16, i):
                    print(index2notes[2][int(elem[2][e])], end="")
                print()
                print()

            print(index2notes[0][int(elem[0][i])].replace("-","b"), end="")
            Compt+=1
        print()
        for e in range(len(elem[0])-16, len(elem[0])):
            print(index2notes[1][int(elem[1][e])], end="")
        print()
        for e in range(len(elem[0])-16, len(elem[0])):
            print(index2notes[2][int(elem[2][e])], end="")
        

        print()
        if (elem is not X[-1]):
            print()
            print("Another One")
        print()

if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: Python3 PrintResults <file>")


