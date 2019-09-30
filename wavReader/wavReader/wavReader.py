import librosa
import numpy as np
import matplotlib.pyplot as plt
import librosa.display
import pretty_midi
import mir_eval.display


def specShow(filePath):
    y, sr = librosa.load(filePath)
    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)
    plt.figure(figsize = (12,8))
    librosa.display.specshow(D, y_axis='linear', x_axis='time')
    plt.ylim(0,1500)
    plt.colorbar(format='%+2.0f dB')
    plt.title('Log-frequency power spectrogram')
    plt.show()
    C = librosa.feature.chroma_cqt(y=y, sr=sr)
    plt.figure(figsize = (12,8))
    librosa.display.specshow(C, y_axis='chroma', x_axis='time')
    plt.colorbar()
    plt.title('Chromagram')
    plt.show()

def plot_piano_roll(pm, start_pitch, end_pitch, fs=100):
                    librosa.display.specshow(pm.get_piano_roll(fs)[start_pitch:end_pitch], 
                    hop_length=1, sr=fs, x_axis='time', 
                    y_axis='cqt_note',fmin=pretty_midi.note_number_to_hz(start_pitch))



if __name__ == '__main__':
    filePath =  'C:\\Users\\von SolIII\\Desktop\\Praeludium & Fuga No. 1 in C Major - Praeludium BWV 846.wav'
    specShow(filePath)
    '''
    pm = pretty_midi.PrettyMIDI('C:\\Users\\von SolIII\\Desktop\\wtk1-prelude1.mid')
    plt.figure(figsize=(12, 4))
    plot_piano_roll(pm, 24, 84)
    plt.show()
    '''