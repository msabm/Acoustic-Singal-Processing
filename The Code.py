# Import necessary libraries
import sounddevice as sd  # Library for audio recording and playback
import matplotlib.pyplot as plt  # Library for data visualization
import numpy as np  # Library for numerical operations
import librosa.display  # Library for audio and music analysis
from scipy.signal import butter, filtfilt  # Functions for signal filtering
from scipy import ndimage  # Functions for n-dimensional image processing
import pandas as pd  # Library for data manipulation and analysis

# Function to compute the constellation map based on given parameters
def compute_constellation_map(Y, dist_freq, dist_time, thresh):
    # Apply maximum filter to identify local maximums
    result = ndimage.maximum_filter(Y, size=[2 * dist_freq + 1, 2 * dist_time + 1], mode='constant')
    # Create a map of points that satisfy certain conditions
    Cmap = np.logical_and(Y == result, result > thresh)
    return Cmap

# Sampling frequency and duration for audio recording
fs = 44000  # Sampling frequency (samples per second)
duration = 14  # Duration of audio recording in seconds
result_list = []
threshold_freq = 250  # Minimum frequency for considering a point as a "1"

# Record audio using sounddevice
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1)  # Record audio for the given duration
print('recording...')
sd.wait()  # Wait for the recording to finish

audio_data = np.squeeze(myrecording)  # Extract audio data from the recorded array

# Define filter parameters for audio signal
lowcut = 4800
highcut = 7200
order = 4

nyquist_freq = 0.5 * fs
low = lowcut / nyquist_freq
high = highcut / nyquist_freq
b, a = butter(order, [low, high], btype='band')  # Design a bandpass filter
filtered_audio = filtfilt(b, a, audio_data)  # Apply the filter to the audio data
time = np.arange(0, len(filtered_audio)) / fs  # Create a time array for the filtered audio

# Calculate spectrogram of filtered audio
spectrogram = librosa.amplitude_to_db(np.abs(librosa.stft(filtered_audio)), ref=np.max)  # Compute the spectrogram
frequencies = librosa.fft_frequencies(sr=fs, n_fft=spectrogram.shape[0])  # Compute frequency bins

Y = np.abs(librosa.stft(filtered_audio))  # Compute the short-time Fourier transform of the filtered audio

# Parameters for constellation map computation
dist_freq = 7  # Distance in frequency bins for finding local maximums
dist_time = 7  # Distance in time bins for finding local maximums
thresh = 2  # Threshold for determining valid local maximums

# Compute the constellation map
Cmap = compute_constellation_map(Y, dist_freq=dist_freq, dist_time=dist_time, thresh=thresh)

# Apply thresholding to the spectrogram and constellation map
mask = np.abs(spectrogram) < np.max(spectrogram) * thresh  # Create a mask based on the threshold
Cmap[mask] = False  # Set values outside the mask to False

# Visualize spectrogram and constellation map
plt.figure(figsize=(14, 7))
plt.subplot(2, 1, 1)
librosa.display.specshow(librosa.amplitude_to_db(Y, ref=np.max), sr=fs, x_axis='time', y_axis='linear', cmap='magma')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Spectrogram')
plt.ylim([lowcut, highcut])

plt.subplot(2, 1, 2)
librosa.display.specshow(Cmap, sr=fs, x_axis='time', y_axis='linear', cmap='magma')
plt.xlabel('Time (s)')
plt.ylabel('Frequency (Hz)')
plt.title('Constellation Map')
plt.ylim([lowcut, highcut])

plt.tight_layout()

# Extract points from the constellation map and sort them
points = np.transpose(np.nonzero(Cmap))
sorted_points = points[np.lexsort((points[:, 0], points[:, 1]))]

# Create a list to store results for each row
rows_list = []
current_row = {}

# Process the points and create rows
for i, point in enumerate(sorted_points):
    if i % 8 == 0 and i > 0:
        # Calculate and append the parity bit to the current row
        parity_bit = sum(current_row.values()) % 2
        current_row['Parity'] = parity_bit

        # Append the current row to the list and reset the current row
        rows_list.append(current_row)
        current_row = {}

    if point[0] > threshold_freq:
        current_row[f'Bit{i % 8}'] = 1
    else:
        current_row[f'Bit{i % 8}'] = 0

# Calculate and append the parity bit to the last row (if any)
if current_row:
    parity_bit = sum(current_row.values()) % 2
    current_row['Parity'] = parity_bit
    rows_list.append(current_row)

# Convert the list of rows to a DataFrame
result_df = pd.DataFrame(rows_list)

# Add additional columns to the DataFrame
result_df['Sent Parity'] = [1, 0, 1, 0, 0, 0, 0, 1]
result_df['Match'] = ['=IF($I2=$J2, "Yes", "No")', '=IF($I3=$J3, "Yes", "No")', '=IF($I4=$J4, "Yes", "No")',
                      '=IF($I5=$J5, "Yes", "No")', '=IF($I6=$J6, "Yes", "No")', '=IF($I7=$J7, "Yes", "No")',
                      '=IF($I8=$J8, "Yes", "No")', '=IF($I9=$J9, "Yes", "No")', ]

# Save the results to an Excel file
excel_writer = pd.ExcelWriter('results.xlsx', engine='xlsxwriter')
result_df.to_excel(excel_writer, sheet_name='Results', index=False)
excel_writer.close()

# Display the plots
plt.show()
