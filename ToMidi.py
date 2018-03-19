"""
Created on 15 mars 2016

@author: Gaetan Hadjeres
"""
import os
import pickle

from music21 import midi

from Deepbach.data_utils import generator_from_raw_dataset, BACH_DATASET, \
    all_features, \
    indexed_chorale_to_score, START_SYMBOL, END_SYMBOL, all_metadatas, \
    standard_note, SOP, BASS, PACKAGE_DIR
from .metadata import *


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
                f = standard_note(index2notes[voice_index][n])
            else:
                dur += 1
        # add last note
        f.duration = duration.Duration(dur / SUBDIVISION)
        part.append(f)
        score.insert(part)
    return score


def chordsToVoices(seq):



def seqtoMidi(name):

    pickled_dataset = 'DeepBahc/datasets/custom_dataset' + name + '.pickle'
    pickle.load(open("Results" + name, 'rb'))

    seq = chordsToVoices(seq)
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

    # display in editor
    #score.show()

    pickle.dump(seq, open("Results"+ pickled_dataset[pickled_dataset.rfind("/"):pickled_dataset.rfind(".")], 'wb'), pickle.HIGHEST_PROTOCOL)
    
