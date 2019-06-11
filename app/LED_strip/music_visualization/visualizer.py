from __future__ import print_function
from __future__ import division
import time
import numpy as np
from scipy.ndimage.filters import gaussian_filter1d
import config
from microphone import Microphone
import dsp
import led

_time_prev = time.time() * 1000.0
"""The previous time that the frames_per_second() function was called"""

_fps = dsp.ExpFilter(val=config.FPS, alpha_decay=0.2, alpha_rise=0.2)
"""The low-pass filter used to estimate frames-per-second"""


def frames_per_second():
    """Return the estimated frames per second

    Returns the current estimate for frames-per-second (FPS).
    FPS is estimated by measured the amount of time that has elapsed since
    this function was previously called. The FPS estimate is low-pass filtered
    to reduce noise.

    This function is intended to be called one time for every iteration of
    the program's main loop.

    Returns
    -------
    fps : float
        Estimated frames-per-second. This value is low-pass filtered
        to reduce noise.
    """
    global _time_prev, _fps
    time_now = time.time() * 1000.0
    dt = time_now - _time_prev
    _time_prev = time_now
    if dt == 0.0:
        return _fps.value
    return _fps.update(1000.0 / dt)


def memoize(function):
    """Provides a decorator for memoizing functions"""
    from functools import wraps
    memo = {}

    @wraps(function)
    def wrapper(*args):
        if args in memo:
            return memo[args]
        else:
            rv = function(*args)
            memo[args] = rv
            return rv
    return wrapper


@memoize
def _normalized_linspace(size):
    return np.linspace(0, 1, size)


def interpolate(y, new_length):
    """Intelligently resizes the array by linearly interpolating the values

    Parameters
    ----------
    y : np.array
        Array that should be resized

    new_length : int
        The length of the new interpolated array

    Returns
    -------
    z : np.array
        New array with length of new_length that contains the interpolated
        values of y.
    """
    if len(y) == new_length:
        return y
    x_old = _normalized_linspace(len(y))
    x_new = _normalized_linspace(new_length)
    z = np.interp(x_new, x_old, y)
    return z


r_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                       alpha_decay=0.2, alpha_rise=0.99)
g_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                       alpha_decay=0.05, alpha_rise=0.3)
b_filt = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                       alpha_decay=0.1, alpha_rise=0.5)
common_mode = dsp.ExpFilter(np.tile(0.01, config.N_PIXELS // 2),
                       alpha_decay=0.99, alpha_rise=0.01)
p_filt = dsp.ExpFilter(np.tile(1, (3, config.N_PIXELS // 2)),
                       alpha_decay=0.1, alpha_rise=0.99)
gain = dsp.ExpFilter(np.tile(0.01, config.N_FFT_BINS),
                     alpha_decay=0.001, alpha_rise=0.99)



class Visualizer:
    def __init__(self):
        self._prev_spectrum = np.tile(0.01, config.N_PIXELS // 2)
        self.p = np.tile(1.0, (3, config.N_PIXELS // 2))
        self.effects = {
            "spectrum": self.spectrum_viz,
            "scroll": self.scroll_viz,
            "energy": self.energy_viz,
            "wavelength": self.wavelength_viz,
        }
        self.current_effect = None
        self.microphone = Microphone()
        self.set_effect()

    def start(self, TODO=None):
        self.microphone.start(self.update)

    def stop(self):
        self.microphone.stop()

    def update(self, audio_samples):
        # Map filterbank output onto LED strip
        audio_samples = self.microphone.update(audio_samples)
        new_viz = self.current_effect(audio_samples)
        led.pixels = new_viz
        led.update()

    def get_current_effect(self, effect):
        return self.current_effect

    def set_effect(self, pattern=''):
        self.current_effect = getattr(self, pattern+'_viz', self.scroll_viz)
        print('Set current effect to: ', self.current_effect)

    def spectrum_viz(self, y):
        """Effect that maps the Mel filterbank frequencies onto the LED strip"""
        y = np.copy(interpolate(y, config.N_PIXELS // 2))
        common_mode.update(y)
        diff = y - self._prev_spectrum
        self._prev_spectrum = np.copy(y)
        # Color channel mappings
        r = r_filt.update(y - common_mode.value)
        g = np.abs(diff)
        b = b_filt.update(np.copy(y))
        # Mirror the color channels for symmetric output
        r = np.concatenate((r[::-1], r))
        g = np.concatenate((g[::-1], g))
        b = np.concatenate((b[::-1], b))
        output = np.array([r, g,b]) * 255
        return output

    def wavelength_viz(self, y):
        y = np.copy(interpolate(y, config.N_PIXELS // 2))
        common_mode.update(y)
        # Color channel mappings
        r = r_filt.update(y - common_mode.value)
        g = np.abs(diff)
        b = b_filt.update(np.copy(y))
        r = np.array([j for i in zip(r,r) for j in i])
        output = np.array([colour_manager.full_gradients[self.board][config["color_mode"]][0][
                                    (config.N_PIXELS if config["Wavelength"]["reverse_grad"] else 0):
                                    (None if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["reverse_grad"] else config.N_PIXELS):]*r,
                           colour_manager.full_gradients[self.board][config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["color_mode"]][1][
                                    (config.N_PIXELS if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["reverse_grad"] else 0):
                                    (None if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["reverse_grad"] else config.N_PIXELS):]*r,
                           colour_manager.full_gradients[self.board][config["Wavelength"]["color_mode"]][2][
                                    (config.N_PIXELS if config_opts["Wavelength"]["reverse_grad"] else 0):
                                    (None if config["Wavelength"]["reverse_grad"] else config.N_PIXELS):]*r])
        colour_manager.full_gradients[self.board][config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["color_mode"]] = np.roll(
                    colour_manager.full_gradients[self.board][config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["color_mode"]],
                    config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["roll_speed"]*(-1 if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["reverse_roll"] else 1),
                    axis=1)
        output[0] = gaussian_filter1d(output[0], sigma=config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["blur"])
        output[1] = gaussian_filter1d(output[1], sigma=config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["blur"])
        output[2] = gaussian_filter1d(output[2], sigma=config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["blur"])
        if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["flip_lr"]:
            output = np.fliplr(output)
        if config.settings["devices"][self.board]["effect_opts"]["Wavelength"]["mirror"]:
            output = np.concatenate((output[:, ::-2], output[:, ::2]), axis=1)
        return output

    def scroll_viz(self, y):
        """Effect that originates in the center and scrolls outwards"""
        y = y**2.0
#y = np.copy(interpolate(y, config.N_PIXELS // 2))
        gain.update(y)

        y = np.clip(y, 0, 1)
        #y /= gain.value
        #y *= 255.0
        lows = y[:len(y) // 6]
        mids = y[len(y) // 6: 2 * len(y) // 5]
        high = y[2 * len(y) // 5:]
        # max values
        lows_max = np.max(lows)
        mids_max = float(np.max(mids))
        high_max = float(np.max(high))
        # indexes of max values
        # map to colour gradient
        RED=(255,0,0)
        GREEN=(0,255,0)
        BLUE=(0,0,255)
        lows_val = (np.array(RED) * lows_max).astype(int)
        mids_val = (np.array(GREEN) * mids_max).astype(int)
        high_val = (np.array(BLUE) * high_max).astype(int)
        r = int(np.max(y[:len(y) // 3]))
        g = int(np.max(y[len(y) // 3: 2 * len(y) // 3]))
        b = int(np.max(y[2 * len(y) // 3:]))
        # Scrolling effect window
        self.p[:, 1:] = self.p[:, :-1]
        BLUR = 0.2
        self.p = gaussian_filter1d(self.p, sigma=BLUR)
        self.p[0, :1] = lows_val[0] + mids_val[0] + high_val[0]
        self.p[1, :1] = lows_val[1] + mids_val[1] + high_val[1]
        self.p[2, :1] = lows_val[2] + mids_val[2] + high_val[2]
        # Create new color originating at the center
        #self.p[0, 0] = r
        #self.p[1, 0] = g
        #self.p[2, 0] = b
        # Update the LED strip
        return np.concatenate((self.p[:, ::-1], self.p[:, ::1]), axis=1)

    def energy_viz(self, y):
        """Effect that expands from the center with increasing sound energy"""
        y = np.copy(y)
        gain.update(y)
        y /= gain.value
        # Scale by the width of the LED strip
        y *= float((config.N_PIXELS // 2) - 1)
# OTHER LIB
#y = np.copy(interpolate(y, config.settings["devices"][self.board]["configuration"]["N_PIXELS"] // 2))
#self.prev_spectrum = np.copy(y)
#spectrum = np.copy(self.prev_spectrum)
#spectrum = np.array([j for i in zip(spectrum,spectrum) for j in i])
        # Map color channels according to energy in the different freq bands
        scale = 0.9
        r = int(np.mean(y[:len(y) // 3]**scale))
        g = int(np.mean(y[len(y) // 3: 2 * len(y) // 3]**scale))
        b = int(np.mean(y[2 * len(y) // 3:]**scale))
        # Assign color to different frequency regions
        self.p[0, :r] = 255.0
        self.p[0, r:] = 0.0
        self.p[1, :g] = 255.0
        self.p[1, g:] = 0.0
        self.p[2, :b] = 255.0
        self.p[2, b:] = 0.0
        p_filt.update(self.p)
        self.p = np.round(p_filt.value)
        # Apply substantial blur to smooth the edges
        self.p[0, :] = gaussian_filter1d(self.p[0, :], sigma=4.0)
        self.p[1, :] = gaussian_filter1d(self.p[1, :], sigma=4.0)
        self.p[2, :] = gaussian_filter1d(self.p[2, :], sigma=4.0)
        # Set the new pixel value
# OTHER LIB
#if config.settings["devices"][self.board]["effect_opts"]["Energy"]["mirror"]:
#    p = np.concatenate((self.output[:, ::-2], self.output[:, ::2]), axis=1)
#else:
#    p = self.output
#return p
        return np.concatenate((self.p[:, ::-1], self.p), axis=1)


#fft_plot_filter = dsp.ExpFilter(np.tile(1e-1, config.N_FFT_BINS),
#                         alpha_decay=0.5, alpha_rise=0.99)
if __name__ == '__main__':
    # Initialize LEDs
    # Start listening to live audio stream
    vis = Visualizer()
    vis.start()
