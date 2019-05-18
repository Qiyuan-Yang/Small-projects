import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display

filePath = 'C:\\Users\\von SolIII\\Desktop\\BWV126CoroErhalt uns Herr bei deinem Wort.wav'
y, sr = librosa.load(filePath)
D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
plt.figure(figsize = (12,8))
plt.subplot(2,2,1)
librosa.display.specshow(D, y_axis='log')
plt.colorbar(format='%+2.0f dB')
plt.title('Log-frequency power spectrogram')
C = librosa.feature.chroma_cqt(y=y, sr=sr)
plt.subplot(2,2,2)
librosa.display.specshow(C, y_axis='chroma')
plt.colorbar()
plt.title('Chromagram')
cent = librosa.feature.spectral_centroid(y=y, sr=sr)
plt.subplot(2, 2, 3)
plt.semilogy(cent.T, label='Spectral centroid')
plt.ylabel('Hz')
plt.xticks([])
plt.xlim([0, cent.shape[-1]])
plt.show()