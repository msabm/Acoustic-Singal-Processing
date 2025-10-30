# Acoustic Signal Processing

## Introduction
In today's world, audio signals hold vital information, making their analysis crucial across various fields. This project delves into audio processing and analysis, exploring techniques to extract insights from audio recordings. By combining digital signal processing, spectral analysis, and pattern recognition, this project showcases an approach to understanding information within audio signals.

This project aims to create a pipeline for audio analysis, encompassing steps like recording, signal filtering, spectrogram computation, constellation mapping, and data interpretation. Each step is designed to extract significant information from the audio signal for applications ranging from audio quality assessment to information encoding.

---

## Methodology
The methodology employed in this project involves a systematic approach to extract meaningful insights from audio recordings. The process encompasses several distinct steps, each contributing to the comprehensive analysis of audio signals.

### Audio Recording and Sampling
The initial step involves selecting an appropriate sampling frequency to accurately capture the nuances of the audio signal. Audio is recorded using the chosen sampling frequency and predefined duration, resulting in a digital representation of the audio waveform.

### Signal Filtering
After recording, the audio signal undergoes filtering to isolate specific frequency components of interest. Bandpass filters with predefined cutoff frequencies are applied, producing a filtered audio signal that removes unwanted noise and interference.

### Spectral Analysis and Spectrogram Computation
The filtered audio signal is analyzed using the Short-Time Fourier Transform (STFT), which breaks down the signal into constituent frequency components over short time intervals. Complex STFT values are converted into amplitude values to compute a spectrogram, visually representing frequency distribution over time.

### Constellation Map Generation
A constellation map is created by identifying local maxima in the spectrogram. Parameters such as distance thresholds define which maxima qualify as significant points. This simplifies complex spectrogram data into a representation highlighting patterns and relationships.

### Data Point Extraction and Processing
Data points are extracted from the constellation map and sorted based on a predefined criterion. Each point is assigned a binary value based on its frequency, translating frequency information into binary format.

### Parity Bit Calculation
To ensure data integrity, parity bits are calculated for the processed binary values. Data is grouped into rows, typically containing eight values per row. Each row's parity bit acts as a checksum to detect potential errors or discrepancies.

### Interpretation and Visualization
Processed data is interpreted to decode embedded information in the audio signal. Results are visualized using spectrograms and constellation maps, aiding comprehension of extracted insights.

### Application and Analysis
The methodology is applied to various audio recordings to assess effectiveness across different scenarios. Results are analyzed to draw conclusions regarding project objectives and potential applications.

### Documentation and Reporting
Comprehensive documentation is maintained, including parameter settings, code implementation, and rationale behind decisions. The culmination of the project is a report summarizing the methodology, results, and insights gained from audio signal analysis.

---

## Description of the Code
The code implements the methodology as follows:

- **Audio Recording and Sampling**: Uses a sampling frequency of 44,000 Hz and a duration of 14 seconds to ensure high-fidelity audio capture. Adjustments to either parameter require recalibration of the other.
  
- **Signal Filtering**: Bandpass filters with lowcut and highcut frequencies set at 4,800 Hz and 7,200 Hz respectively isolate the desired frequency range. A fourth-order filter is used, with normalization to the Nyquist frequency.
  
- **Spectral Analysis and Spectrogram Computation**: Applies STFT to the filtered audio signal. Complex STFT values are converted to amplitude to create a spectrogram, providing a visual representation of frequency variations over time.
  
- **Constellation Map Generation**: `compute_constellation_map` identifies local maxima in the spectrogram. Parameters `dist_freq`, `dist_time`, and `thresh` determine which points are included.
  
- **Data Point Extraction and Processing**: Extracted points are sorted using `np.lexsort((points[:, 0], points[:, 1]))` and converted to binary format based on frequency values.
  
- **Parity Bit Calculation**: Ensures data integrity by calculating parity bits for rows of binary data.
  
- **Interpretation and Visualization**: Results are interpreted and visualized using `librosa.display.specshow`, enabling intuitive understanding of the extracted information.
  
- **Application and Analysis**: The methodology is tested across multiple audio recordings to evaluate performance and adaptability.

The code closely follows the methodology and ensures accurate signal representation, highlighting the project's commitment to thorough analysis and clear interpretation.

---

## Conclusion
This project successfully applies a systematic methodology to analyze audio signals, extracting meaningful insights through a well-structured code. By meticulously adhering to the methodology's guidelines, the code efficiently captures and processes sound data. The interdependent nature of parameters like sampling frequency and duration is managed adeptly, ensuring the accuracy of signal representation. Through a cohesive fusion of theory and practical implementation, this project demonstrates the efficacy of the proposed methodology in real-world applications, underscoring its value in the field of audio signal analysis.

---
