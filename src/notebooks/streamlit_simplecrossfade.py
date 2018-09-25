from os import listdir
from os.path import isfile, join
import sys
# Change path back to /src to load other modules
sys.path.insert(0, '/home/ubuntu/DeepBass/src')
from ingestion.IO_utils import Load, Save
from model.crossfade_simple import Crossfade_Simple

import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

"""Display what the simple cross fading techniques do to the raw data

User Parameters:
    Ramp (str): Type of ramping function to use
    snippet_time (float) : Amount of time for song overlapping
    AUDIO_DIR (str) : Directory where mp3 are stored.
    output_dir (str) : Directory to save audio with cross fading
Returns:
    Streamlit notebook
"""

st.title('Simple cross fading')

AUDIO_DIR = '/home/ubuntu/DeepBass/data/raw/House_Top20'
filenames = [f for f in listdir(AUDIO_DIR) if isfile(join(AUDIO_DIR, f))]

# Randomly sample two songs from the folder
np.random.seed(442)
selected_files = np.random.choice(filenames,size=2)
print('Files: {}'.format(selected_files))

# Load both songs
sr = 44100
x1, sr1 = Load(AUDIO_DIR, selected_files[0], sr=sr)
time1 = np.arange(0,len(x1),1)/sr1

x2, sr2 = Load(AUDIO_DIR, selected_files[1], sr=sr)
time2 = np.arange(0,len(x2),1)/sr2

# Trim the songs to the beginning and end
if sr1 != sr2:
    raise ValueError('Sampling rates between songs must be identical')

snippet_time = 10 # seconds
snippet_length = snippet_time * sr1 # number of samples

# Cross Fading Choice
Ramp = 'Linear'

mix, x1_trim_faded, x2_trim_faded = Crossfade_Simple(x1, x2, Ramp,
                                                     snippet_time, sr1)

# Plot amplitudes for the beginning and end
x1_trim =x1[-snippet_length:]
t1_trim = time1[-snippet_length:]
x2_trim =x2[0:snippet_length]
t2_trim = time2[0:snippet_length]

fig, ax = plt.subplots(2)
ax[0].plot(t1_trim, x1_trim, 'r-')
ax[1].plot(t2_trim, x2_trim, 'b-')
ax[1].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude')
ax[1].set_ylabel('Amplitude')
st.pyplot()

# Plot cross faded amplitudes over the same time

fig, ax = plt.subplots(2)
ax[0].plot(t1_trim, x1_trim_faded, 'r-')
ax[1].plot(t2_trim, x2_trim_faded, 'b-')
ax[1].set_xlabel('Time (s)')
ax[0].set_ylabel('Amplitude')
ax[1].set_ylabel('Amplitude')
st.pyplot()

# Mixed audio
st.write(Ramp)
fig, ax = plt.subplots()
ax.plot(t1_trim, mix, 'g-')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Amplitude')
st.pyplot()

output_name = Ramp + '_CrossFadedSnippet_' + str(snippet_time) + '.wav'
output_dir = '/home/ubuntu/DeepBass/data/processed/'
Save(output_dir, output_name, mix, sr1)
