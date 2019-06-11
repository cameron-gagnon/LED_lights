from __future__ import print_function
from scipy.ndimage.filters import gaussian_filter1d
import time
import numpy as np
import pyaudio
import config
import dsp

class Microphone(object):
    FFT_WINDOW = np.hamming(int(config.MIC_RATE / config.FPS) * config.N_ROLLING_HISTORY)
    # Number of audio samples to read every time frame
    SAMPLES_PER_FRAME = int(config.MIC_RATE / config.FPS)

    def __init__(self):
        self.stream = None
        self.p = pyaudio.PyAudio()
        self.prev_fps_update = time.time()
        # Array containing the rolling audio sample window
        self.y_roll = np.random.rand(config.N_ROLLING_HISTORY, self.SAMPLES_PER_FRAME) / 1e16
        self.mel_smoothing = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                alpha_decay=0.5, alpha_rise=0.99)
        self.mel_gain = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
                                alpha_decay=0.01, alpha_rise=0.99)
        self._stop = True

    def update(self, audio_samples):
        # Normalize samples between 0 and 1
        y = audio_samples / 2.0**15
        # Construct a rolling window of audio samples
        self.y_roll[:-1] = self.y_roll[1:]
        self.y_roll[-1, :] = np.copy(y)
        y_data = np.concatenate(self.y_roll, axis=0).astype(np.float32)
        y_data *= 1.8

        vol = np.max(np.abs(y_data))
        if vol < config.MIN_VOLUME_THRESHOLD:
            print('No audio input. Volume below threshold. Volume:', vol)
            return np.tile(0, (3, config.N_PIXELS))
        else:
            # Transform audio input into the frequency domain
            N = len(y_data)
            N_zeros = 2**int(np.ceil(np.log2(N))) - N
            # Pad with zeros until the next power of two
            y_data *= self.FFT_WINDOW
            y_padded = np.pad(y_data, (0, N_zeros), mode='constant')
            YS = np.abs(np.fft.rfft(y_padded)[:N // 2])
            # Construct a Mel filterbank from the FFT data
            mel = np.atleast_2d(YS).T * dsp.mel_y.T
            # Scale data to values more suitable for visualization
            # mel = np.sum(mel, axis=0)
            mel = np.sum(mel, axis=0)
            mel = mel**2.0
            # Gain normalization
            self.mel_gain.update(np.max(gaussian_filter1d(mel, sigma=1.0)))
            mel /= self.mel_gain.value
            mel = self.mel_smoothing.update(mel)
            return mel

        if config.DISPLAY_FPS:
            fps = frames_per_second()
            if time.time() - 0.5 > self.prev_fps_update:
                self.prev_fps_update = time.time()
                print('FPS {:.0f} / {:.0f}'.format(fps, config.FPS))



    def start(self, callback):
        self._stop = False
        frames_per_buffer = int(config.MIC_RATE / config.FPS)

        self.stream = self.p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=config.MIC_RATE,
                        input=True,
                        frames_per_buffer=frames_per_buffer)
        overflows = 0
        prev_ovf_time = time.time()
        while True:
            try:
                y = np.fromstring(self.stream.read(frames_per_buffer, exception_on_overflow=False), dtype=np.int16)
                y = y.astype(np.float32)
                self.stream.read(self.stream.get_read_available(), exception_on_overflow=False)
                callback(y)
            except IOError:
                overflows += 1
                if time.time() > prev_ovf_time + 1:
                    prev_ovf_time = time.time()
                    print('Audio buffer has overflowed {} times'.format(overflows))

            if self._stop:
                self._cleanup()
                return

    def _cleanup(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()

    def stop(self):
        self._stop = True
