"""
Created on 15 mars 2016

@author: Gaetan Hadjeres
"""
import os
import sys
import pickle
import numpy as np

from music21 import midi, note, chord, pitch
from music21 import corpus, converter, stream, duration, interval


from DeepBach.data_utils import SLUR_SYMBOL, START_SYMBOL, END_SYMBOL, all_metadatas
from DeepBach.metadata import *



# TODO : Change indexed_chorale_to_score, in order to transform chords names in music21 chord object 
# and add it to the score in order to put it in the exported midi file

def standard_note(note_or_rest_string):
    if note_or_rest_string == 'rest':
        return note.Rest()
    # treat other additional symbols as rests
    if note_or_rest_string == START_SYMBOL or note_or_rest_string == END_SYMBOL:
        return note.Rest()
    if note_or_rest_string == SLUR_SYMBOL:
        print('Warning: SLUR_SYMBOL used in standard_note')
        return note.Rest()
    else:
        return note.Note(note_or_rest_string)


def indexed_chorale_to_score(seq, pickled_dataset):
    """

    :param seq: voice major
    :param pickled_dataset:
    :return:
    """
    _, _, _, index2notes, note2indexes, _ = pickle.load(
        open(pickled_dataset, 'rb'))
    num_pitches = list(map(len, index2notes))
    slur_indexes = list(map(lambda d: d[SLUR_SYMBOL], note2indexes))

    score = stream.Score()
    for voice_index, v in enumerate(seq):
        part = stream.Part(id='part' + str(voice_index))
        dur = 0
        f = note.Rest()
        for k, n in enumerate(v):
            # if it is a played note
            if not n == slur_indexes[voice_index]:
                # add previous note
                if dur > 0:
                    f.duration = duration.Duration(dur / SUBDIVISION)
                    part.append(f)

                dur = 1
                if voice_index == 0:
                    f = standard_note(index2notes[voice_index][n])
                elif voice_index == 1:
                    f = chord.Chord(notesFromChord(index2notes[voice_index][n]))
                else :
                    raise "We can only work with 2 voices"

            else:
                dur += 1
        # add last note
        f.duration = duration.Duration(dur / SUBDIVISION)
        part.append(f)
        score.insert(part)
    return score
    

def getIntervalsFromChordColor(color): 

    if color == "maj" :
        interval =  [4,7]

    elif color == "min" :
        interval =  [3,7]

    elif color == "min#5" :
        interval =  [3,8]

    elif color == "dim" :
        interval =  [3,6]

    elif color == "+" :
        interval =  [4,8]

    elif color == "min7" :
        interval =  [3,7,10]

    elif color == "min(maj7)" :
        interval =  [3,7,11]

    elif color == "7" :
        interval =  [4,7,10]

    elif color == "7sus4" :
        interval =  [5,7,10]

    elif color == "7sus4" :
        interval =  [4,7,17]

    elif color == "7b5" :
        interval =  [4,6,10]

    elif color == "7" :
        interval =  [4,10]

    elif color == "maj7" :
        interval =  [4,7,11]

    elif color == "m7b5" :
        interval =  [3,6,10]

    elif color == "dim7" :
        interval =  [3,6,9]

    elif color == "7+" :
        interval =  [4,8,10]

    elif color == "min6" :
        interval =  [3,7,9]

    elif color == "6" :
        interval =  [4,7,9]

    elif color == "7b9" :
        interval =  [4,7,10,13]

    elif color == "7b5b9" :
        interval =  [4,6,10,13]

    elif color == "9" :
        interval =  [4,7,10,14]

    elif color == "sus49" :
        interval =  [5,7,14]

    elif color == "m9" :
        interval =  [3,7,10,14]

    elif color == "maj9" :
        interval =  [4,7,11,14]

    elif color == "#59" :
        interval =  [4,8,10,14]

    elif color == "7#5b9" :
        interval =  [4,8,10,13]

    elif color == "#5#9" :
        interval =  [4,8,10,15]

    elif color == "#59" :
        interval =  [4,8,14]

    elif color == "#5#9" :
        interval =  [4,8,15]

    elif color == "7#9" :
        interval =  [4,7,10,15]

    elif color == "713" :
        interval =  [4,7,10,21]

    elif color == "7b5#9" :
        interval =  [4,6,10,15]

    elif color == "min11" :
        interval =  [3,7,10,14,17]

    elif color == "7alt" :
        interval =  [3,6,10,13,16,20]

    elif color == "13" :
        interval =  [4,7,10,14,21]

    elif color == "13" :
        interval =  [4,7,10,14,17,21]

    elif color == "69" :
        interval =  [4,7,9,14]

    elif color == "min69" :
        interval =  [3,7,9,14]

    elif color == "11" :
        interval =  [4,7,10,14,17]

    elif color == "9#11" :
        interval =  [4,7,10,14,18]

    elif color == "7#11" :
        interval =  [4,7,10,18]

    elif color == "7sus" :
        interval =  [4,7,10,17]

    elif color == "7sus43" :
        interval =  [4,57,10]

    elif color == "maj7b5":
        interval = [4,7,11,18]

    else :
        raise NameError("Chord Undifined : "+ color)

    return interval


def notesFromChord(chord):

    if chord[1] == "-" or chord[1] == "b" or chord[1] == "#":
        root = chord[0:2]
        color = chord[2:]
    else : 
        root = chord[0:1]
        color = chord[1:]

    root = root.replace("b", "-")

    n = pitch.Pitch(root+'4')
    num = n.midi

    Notes = [num]

    for elem in getIntervalsFromChordColor(color):
        Notes.append(num+int(elem))

    for i in range(len(Notes)):
        # We can use .name in place of .nameWithOctave in order to only have the name of the notes
        Notes[i] = note.Note(Notes[i]).nameWithOctave

    return Notes


#def chordsToVoices(seq):


def seqtoMidi(name):

    pickled_dataset = 'DeepBach/datasets/custom_dataset/' + name + '.pickle'
    seq = pickle.load(open("Results/" + name, 'rb'))

    #seq = chordsToVoices(seq)

    # convert
    score = indexed_chorale_to_score(np.transpose(seq, axes=(1, 0)),
                                     pickled_dataset=pickled_dataset)

    output_file = "Results/" + name + ".mid"
    # save as MIDI file
    mf = midi.translate.music21ObjectToMidiFile(score)
    mf.open(output_file, 'wb')
    mf.write()
    mf.close()
    print("File " + output_file + " written")

if __name__ == "__main__":
    if len(sys.argv) == 2:
        seqtoMidi(sys.argv[1])
    else:
        print("Usage: Python3 PrintResults <file>")

