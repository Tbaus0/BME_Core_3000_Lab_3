"""
lab3_module.py
This module consists of three functions.
Generally, this module can be used to test playing an octave using sounddevice,
create a chord of different octave and volumes value, and convert the result of an fft, in magnitude, to
decibels. 
This code is relatively flexible and can be used to test the sounddevice package on a compiler,
create hearing aid filters, and convert a magnitude to decibels for bode plots.

Authors: Thomas Bausman & Lincoln Lewis

Changelog:
11-20-23 @ 7:55PM
Lincoln Lewis - Adding comments and starting to follow general lab instructions XD

11-21-23 @ 6:34AM
Thomas - Finished part 1

11-25-23 @ 6:30PM
Added all comments for part 2
and some code hehe

12-1-23 @ 6:30 PM
Lincoln Lewis - Finished pretty much with the whole thing
finished commenting everything and it looks bueno

"""

import numpy as np
import sounddevice as sd


def test_octave(duration, octaves_up, volume):
    """
    test_octave plays a 1kHz tone followed by a note
    in a different octave. It does this by hardcoding a sampling frequency, settings a time vector,
    and creating a tone using cosines. It does this a second time and plays both of them to test it.
    It takes the following inputs:
    :param duration: an integer representing the duration of each tone
    :param octaves_up: n X 1 array of signed floats that represent the values of the octaves (n) we tried
    :param volume: a signed float that represents the amplitude, 'volume' that is used to multiply the tone
    :return:
    """

    # set the time vector
    fs = 44100  # freq in Hz
    time = np.arange(0, duration, 1 / fs)

    # frequency of 1kHz
    freq = 1000
    # create tone
    tone_1 = np.cos(2 * np.pi * freq * time)

    # adjust frequency according to input
    freq2 = 1000 * (2 ** octaves_up)
    # create new tone
    tone_2 = volume * np.cos(2 * np.pi * freq2 * time)

    # play sounds
    sd.play(tone_1, samplerate=fs)
    sd.wait()  # wait for first tone to finish
    sd.play(tone_2, samplerate=fs)


def make_chord(all_octaves_up, all_volumes):
    """
    make_chord creates a chord that contains all of the notes in
    all_octaves_up
    It sets the duration to be one second, hardcodes the sampling frequency, and creates a time and tone array.
    It then iterates through each index in all_octaves_up, and creates a tone (using cosines) at different frequencies, and 
    multiplies it by each volume in the all_volumes array. 
    We then add each tone to the chord and return the chord.
    :param all_octaves_up: n X 1 array of signed floats that represent the values of the octaves (n) we tried
    :param all_volumes: n X 1 array of unsigned - 16 bit floats that represent the array of volumes (n) we played each tone at
    :return: plays each tone (different volumes) of the all_octaves_up param
    """
    # initial variables - time, fs, duration and set the tone to 0
    duration = 1
    fs = 44100
    time = np.arange(0, duration, 1 / fs)
    tone = 0

    # for loop to iterate through each index in all_octaves_up
    for octaves_index in range(len(all_octaves_up)):
        # set the frequency to be 1000 times each index^2 of all_octaves_up
        freq = 1000 * (2 ** all_octaves_up[octaves_index])
        # add it onto the tone with the cos wave
        tone = tone + (all_volumes[octaves_index] * np.cos(2 * np.pi * freq * time))
    # create the chord
    chord = tone / (len(all_octaves_up) * 5)  # added a multiplier of 5 due to distorted sound output
    return chord


def convert_to_db(fft_result):
    """
    convert_to_db will take an fft result and convert it to db units,
    for the purpose of creating bode plots
    This is done by taking the magnitude of our function to get the amplitude,
    and then squaring each amplitude value and normalizing it to max power, while taking 
    the absolute value of it
    
    :param fft_result: n X 1 array of signed 16 bit floats that represent the result of a fast fourier transform,
    where n represents the number of amplitude's in the array :return: the power of the fft result, in decibels,
    an n X 1 array of signed 16 bit floats, where n represents the number of power values in the array
    """

    # get the max power of the array
    max_power = max(fft_result) ** 2
    # find the power_db by taking the log10 of the squared absolute value of the fft_result, divided by our max power
    # to normalize
    power_db = 10 * np.log10(np.square(abs(fft_result)) / max_power)  # then multiply by 10
    # return
    return power_db