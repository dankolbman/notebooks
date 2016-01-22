import os
import numpy as np
import mido

class MidiSong:
  ''' A full song with various features, notes, and piano roll '''

  def __init__(self, filename, r=(40, 109), dt=0.1):
    ''' Initializes a song by reading in the midi file and
    creating a pianoroll from it
    
    filename: filename
    r: pitch range
    dt: time resolution
    '''
    midi = mido.MidiFile(filename)
    self.notes = []
    time = 0.0
    on_notes = {}
    for msg in midi:
      # time in ticks
      time += msg.time
      if not isinstance(msg, mido.MetaMessage):
        if msg.type == 'note_on':
          on_notes[msg.note] = time
        elif (msg.type == 'note_off'
          and msg.note in on_notes
          and on_notes[msg.note] > 0.0):
          self.notes.append([msg.note, on_notes[msg.note], time])
          on_notes[msg.note] = -1.0
    # Create the pianoroll
    dur = np.array(self.notes).max(axis=0)[2] / dt
    self.piano_roll = np.zeros( (int(np.ceil(dur)), r[1]-r[0]) )
    # Resolves each note into a key and time slice in the pianoroll
    for n in self.notes:
       self.piano_roll[int(np.ceil(n[1]/dt)):
                       int(np.ceil(n[2]/dt)), int(n[0]-r[0])] = 1.0

  def __repr__(self):
    return '< MidiSong {} Notes >'.format(len(self.notes))

