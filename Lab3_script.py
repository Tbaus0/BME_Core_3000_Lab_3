"""
Created on Tue Nov 21 13:11:04 2023

File Name: Lab3_script.py

This script is used to make a custom filter for a persons hearing so that all tones played from headphones come
out at an equal volume. To do this an equal loudness filter is created based on 10 trial inputs from the user.
from the trial inputs a filter is made so that when convolved with any chord or multiple different octaves 
they will all play at equal loudness. This filter can be used on everyday speech as well. The script will give you 
three figures, one depicting the steps toward the filter and relative loudness, one showing the filter in both time domain
and frequancy domain, and one showing the difference bewteen the filtered and non-filtered speech test.

@authors: Thomas Bausman and Lincoln Lewis

"""

# %%import libraries
import numpy as np
import sounddevice as sd
from matplotlib import pyplot as plt
from scipy import fft
from scipy.io.wavfile import read

import lab3_module as lm

# %%part 1
# first print statement
print(
    'side note: computer volume at 30 with beats earbuds with a duration of 3. The lowest step down I could hear is '
    'at -4.5 octaves down, with volume'
    '\n at a constant 1 which does not effect second tone volume. The highest step up I could hear is'
    '\n at 5 octaves up')

# create graphs arrays
all_octaves_up = np.array([-4.5, -3.45, -2.4, -1.35, -0.7, 0, 0.75, 1.8, 2.85, 3.9, 4.5])
all_volumes = np.array([10, 6, 3.1, 2, 1.3, 1, 1.2, 1.8, 2.7, 4, 5])
# load our chord, set sampling frequency and play the chord
chord = lm.make_chord(all_octaves_up, all_volumes)
fs = 44100
sd.play(chord, fs)
# 'nother print statement
print('I feel that there may still be a little difference in volume but I can hear most of the notes when'
      "\n they are played together in a chord. It's still hard to tell them apart due to the amount of tones played "
      "at once"
      "\n for the most part there is equal physical volume to my ears. The higher frequencies may stand out a tad more"
      "\n just because it's annoying to hear")

# %%
"""
PART 2
"""
# calculate the fourier transform of the chord and convert it to decibels
fft_result = fft.rfft(chord)
power_dB = lm.convert_to_db(fft_result)
# calculate the frequencies on the x from the all_octaves_up array
frequencies = 1000 * (2 ** all_octaves_up)
# plot all_volumes vs frequency
plt.figure(1, clear=True)
plt.subplot(3, 1, 1)
plt.scatter(frequencies, all_volumes)
# annotate
plt.title('Inferred ffrt')
plt.xlabel('Frequency (Log(Hz))')
plt.ylabel('volume (dB)')
plt.xscale('log')
plt.xlim(0, 10 ** 5)
plt.grid()
# plot the power of the chord
plt.subplot(3, 1, 2)
plt.plot(power_dB)
# annotate
plt.xlabel('Frequency (Log(Hz))')
plt.ylabel('volume (dB)')
plt.xscale('log')
plt.xlim(0, 10 ** 5)
plt.grid()
plt.savefig("graphs/all_volumes_freq.png")
# 'nother print statement
print("This plot shows the relative volumes because it was normalized when it was put into"
      "\n the 'convert_to_db' module. This means that all the volumes are relative to the "
      "\n to the maximum volume. The amplitude of each peak shows how close together"
      "\n the max power and the power at that frequency is. The graph in the first subplot"
      "\n shows what power was chosen for each frequency by us, the listener")

# get the frequencies of the fourier transform and interpolate it with all_volumes
f_fft = fft.rfftfreq(len(fft_result), 1 / fs)
volume_fft = np.interp(f_fft, frequencies, all_volumes)
# convert to decibels
volume_fft_dB = lm.convert_to_db(volume_fft)

# plot the fft of volume in dB
plt.subplot(3, 1, 3)
plt.plot(volume_fft_dB)
# annotate
plt.title('Interpolated Equal Loudness Curve')
plt.xlabel('Frequency (Log(Hz))')
plt.ylabel('Power (dB)')
plt.xscale('log')
plt.xlim(0, 10 ** 5)
plt.grid()
plt.tight_layout()

print("Our loudness curve somewhat represents the loudness curve from the literature"
      "\n because the lower frequencies have the louder power and as the frequency"
      "\n get higher the power drops to maintain equal loudness. Then around 1000 Hz"
      "\n the power goes back up which is reflected in our loudness curve, however,"
      "\n right after the short increase the power goes back down in the literature and ours does not."
      "\n This difference is probably due to the lack of samples, having only 11 leaves out more precise"
      "\n changes in the equal loudness curve like the small dip from 2k-4k Hz in the literature graph.")

# %% Part 3

# take teh real fft of our filter
filter_t = fft.irfft(volume_fft)
# center the filter
filter_t_center = fft.fftshift(filter_t)
# create our special time array that centers it so that it goes from -0.5 to 0.5
t = np.arange((-1 * len(filter_t)) / (2 * fs), len(filter_t) / (2 * fs), 1 / fs)
# frequency array
freq = fft.rfftfreq(len(filter_t), 1 / fs)
# plot impulse response of equal loudness filter
plt.figure(2, clear=True, figsize=(12, 5))
plt.subplot(1, 2, 1)
# annotate
plt.title('Impulse Response of Equal Loudness Filter')
plt.plot(t, filter_t_center)
plt.xlim(-.05, .05)
plt.xlabel('time (s)')
plt.ylabel('h(t)')
plt.grid()
# plot the frequency response of the equal loudness filter
plt.subplot(1, 2, 2)
plt.plot(freq, volume_fft_dB)
# annotate
plt.xscale('log')
plt.title('Frequency Response of Equal Loudness Filter')
plt.xlabel('Frequency (Log(Hz))')
plt.ylabel('volume power (dB)')
plt.grid()
plt.subplots_adjust(top=0.88,
                    bottom=0.11,
                    left=0.125,
                    right=0.9,
                    hspace=0.2,
                    wspace=0.2)
# print statement for type of filter
print(f"From the graph, it is a low-pass filter. The lower frequencies are not being attenuated and have a gain of \n"
      f"one, where the higher frequencies are being attenuated. \nThe slope of this curve appears to be -10 dB a decade "
      f"! However, at around 1kHz, the Power starts to increase, \nbut this will eventually cut off at a certain point "
      f"to keep attenuating the higher frequencies. ")
plt.savefig("graphs/Equal_Loudness_filter.png")
# create new array of two notes with octaves and volumes
new_octaves = np.array([-2.0, 2.0])
new_volumes = np.array([1, 1])

# make notes into a chord with the function
new_chord = lm.make_chord(new_octaves, new_volumes)

# play new chord to determine loudness difference
sd.wait()
sd.play(new_chord)  # wait for previous chord to finish playing
# make the new chord play at equal loudness
convolved_chord = np.convolve(new_chord, filter_t, mode='same')
sd.wait()  # wait for previous chord to finish playing
sd.play(convolved_chord)
# print statement for which sounds louder
print(
    f"The octave -2 has a lower frequency, and since the equal loudness filter is a low-pass filter, the -2.0 octave "
    f"is louder. \n This also was heard in the sd.play(convolved_chord), and from playing the filtered chord,"
    f"the first half,\n which would be the lower frequencies, was louder while the second half (higher frequencies), "
    f"was quieter. ")
print("The two notes from new_chord are closer in volume after convolution. This is because the filter we made"
      "\n passes the lower frequencies (the one two octaves down) almost undisturbed while the higher frequency 2 octaves"
      "\n up was made quieter to even out the volumes. This makes sense because two octaves up plays at 4000 Hz"
      "\n which is where the frequency response of equal loudness filter graph goes to it's lowest.")

# %%
# """PART 4"""
filename = "test123.wav"
fs_test, test_array = read(filename)
sd.wait()
sd.play(test_array / 10000, fs_test)
''' extra credit print statement '''
print(f"If i had to guess, you needed to divide it be 100000 because of the signals bit depth. \nBit depth essentially "
      f"means the precision with which each sample can be represented, givng an 'amplitude range'. \nThis range can "
      f"be exceeded,"
      f"causing clipping or distortion of the signal, which can cause super loud playback. \nEssentially some of these "
      f"integers or floats are outside the range of bit representation. ")

# apply filter to sound
filtered_test = np.convolve(test_array, filter_t_center, mode='same')
# get the fft or our test array and the filtered test array
test_array_freq = fft.rfft(test_array)
filtered_test_fft = fft.rfft(filtered_test)
# get the x-axis for time domain and frequency domain
time_test = np.arange(0, len(test_array) * 1 / fs_test, 1 / fs_test)
test_freq = fft.rfftfreq(len(filtered_test), 1 / fs_test)
sd.wait()
sd.play(filtered_test / 10000, fs_test)
print(
    f"The filtered sound seems to be much more noisier, and the lower frequency of jangraw's speaking \n seems to "
    f"have also been amplified. This makes sense considering we are dealing with a low-pass filter.\n The noise must "
    f"be low frequency which is why it is being amplified. \n ")
# create the figure for original vs filtered in both domains
plt.figure(3, clear=True, figsize=(12, 5))
# plot time domain on first index of subplot
plt.subplot(1, 2, 1)
plt.plot(time_test, test_array)
plt.plot(time_test, filtered_test, alpha=0.7, color='orange')
plt.legend(["Original", "Filtered"], loc='upper right', frameon=True)
# annotate
plt.title("Original vs Filtered in Time Domain")
plt.xlabel('Time (s)')
plt.ylabel('Magnitude (A.U)')
plt.grid()
# print statement to describe how the filtered version looks dif
print(
    f"the filtered version has a much higher magnitude in the time domain, especially when it comes to the line noise \n"
    f"that is happening from 0 - 0.5 seconds and from 2.25 to 3 seconds. \nThe test 123 in the middle is also amplified "
    f"by nearly double. This is most likely caused by the low pass filter that pass lower frequencies and amplifies "
    f"them, \nand then attenuates the higher frequencies. This would be the cause of boost in amplitude ")

# plot frequency domain on second index of subplot
plt.subplot(1, 2, 2)
plt.plot(test_freq, lm.convert_to_db(test_array_freq))
plt.plot(test_freq, lm.convert_to_db(filtered_test_fft), alpha=0.7, color='orange')
# annotate
plt.xscale('log')
plt.title('Original vs Filtered in Frequency Domain')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Power (dB)')
plt.grid()
plt.legend(["Original", "Filtered"], loc='upper right', frameon=True)
plt.show()
print(
    f"As expected, the lower frequencies, in the range of 10Hz to 100Hz, are amplified, \n (where the gain is much "
    f"closer to 1 than the original), and at higher frequencies, the signal's frequencies are attenuating, \n "
    f"meaner that there is less power at higher frequencies. \nThis checks out with our expectations of this filter "
    f"being a low-pass filter.")
plt.savefig("graphs/Original_filtered_freq.png")

# final print statement
print(f"Someone with trouble hearing higher frequencies would have a completely opposite filter than ours, "
      f"which would be a high pass filter. \nThe general idea here is to allow the person to hear more of the higher "
      f"pitch or frequency sounds while the lower frequencies may be slightly attenuated. \nThrough their filter, "
      f"low notes would sound much quieter than high notes, where high notes would be much louder. \nThis is because "
      f"the filter required to allow this person to hear at high frequencies would be a high pass filter, which would "
      f"allow people to hear higher frequencies.")