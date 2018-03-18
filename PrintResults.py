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
    X, _, voice_ids, index2notes, note2indexes, _ = pickle.load(open(picklefile, 'rb'))
    for elem in seq:
        Compt = 0

        for i in range(len(elem[0])):
            if Compt == 16:
                Compt = 0
                print()
                for e in range(i-16, i):
                    if e % 4 == 0:
                        print(" ", end="")
                    print(index2notes[1][int(elem[1][e])], end="")
                print()
                print()
            if i % 4 == 0:
                print(" ", end="")
            print(index2notes[0][int(elem[0][i])].replace("-","b"), end="")
            Compt+=1
        print()
        for e in range(len(elem[0])-16, len(elem[0])):
            if e % 4 == 0:
                print(" ", end="")
            print(index2notes[1][int(elem[1][e])], end="")
if __name__ == "__main__":

    if len(sys.argv) == 2:
        main(sys.argv[1])
    else:
        print("Usage: Python3 PrintResults <file>")


