#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 10 14:11:23 2019

@author: adorman
"""

from music21 import *
import random

import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
warnings.filterwarnings("ignore", message="numpy.ufunc size changed")

Tresillo = '10010010'



######## function 1 - pattern ##########
# the function pattern accepts an integer and duration. It converts the integer to binary and 
# uses that 1's and 0's to create onsets and rests of length 'duration.' Duration is doubled the 
# value to fit with music21's quarterLength default. 

# example: 
# pattern (128, 1/8) - note: 128 = 0b10000000
# [0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125, -0.125]

# pattern (230, 1/8)
# [0.125, 0.125, 0.125, -0.125, -0.125, 0.125, 0.125, -0.125]

def pattern(index, duration):
    pat = bin(index)[2:]
    notes = { '1': str(duration), '0': str(duration * -1)}
    result = []
    for i in range(len(pat)):
        if pat[i] == '0':
            result.append(duration * -1)
        elif pat[i] == '1':
            result.append(duration)
    return result


#### Creates a rhythm from a number by converting it to binary

def RhythmFromNumber (index):
    return(BinRhythm(bin(index)[2:]))

    # example: RhythmFromNumber(211).show()

    # s = stream.Stream()
    # for x in map (RhythmFromNumber, [200, 205, 210]):
    #     s.append(x)
    
    # s.show()



##### BinRhythm uses the tinyNotation interface to convert a binary number into 
##### a stream. Pitch is always b4. 

def BinRhythm (tiny):
    notes = { '1': 'b8 ', '0': 'r8 ' }
    result = ''
    for i in range(len(tiny)):
        result += notes[tiny[i]]

    s = converter.parse("tinyNotation: " + result)
#   s.show()
    return s



def interleave (a, b):
    if len(a) != len(b):
        pass
    string = ''
    for i in range(len(a)):
        string += a[i]
        string += b[i]
        string += ' '
    return string
        

# positive counts how many positive numbers are in a list
    
def positive(lengths):
    counter = 0
    for i in lengths:
        if i >0 :
            counter +=1
    return (counter)

'''

to_do      recursive function SPAN PITCHES   
 fix make_omn to just go by durations
'''

def make_omn(lengths, pitch_string):
        
    pitches = pitch_string.split()
    
                
    if len(pitches) > positive(lengths):
        lengths = repeat_to_length (lengths, len(pitches) + how_many_negatives (lengths))
        pitches = repeat_to_length (pitches, len(lengths))
    
    else:
        lengths = repeat_to_length (lengths, len(pitches) + how_many_negatives (lengths))
    
        '''
        add rests to pitches list
        '''
#    print(lengths)
#    pitches = add_rests_to_pitches (pitches, lengths)
#    lengths = repeat_to_length (lengths, len(pitches) + how_many_rs(pitches) )
#    pitches = repeat_to_length (pitches, len(lengths))
#    print(pitches)
    
    stream1 = stream.Stream()
        
    for i in range(len(lengths)):
        if lengths[i] >= 0:
            n1 = chord.Chord(add_space(pitches[i]))
            n1.duration.quarterLength = (4 * lengths[i])
            stream1.append(n1)
        else:
            r1 = note.Rest()
            r1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(r1)
            
    stream1.show()
    return stream1
    


 
    

'''
repeat_to_length expand a list to a given length
'''


def repeat_to_length(string_to_expand, length):
    return (string_to_expand * (int(length/len(string_to_expand))+1))[:length]


 

'''
add_rests_to_pitches prepares the pitches variable to include 'r' whereever there will be a rest 
'''

def add_rests_to_pitches (pitches, lengths):
    new_pitches = []
    counter = 0 
    for i in lengths:
        if i < 0 :
            new_pitches.append('r')
        else:
            new_pitches.append(pitches[counter])
            counter += 1
    return new_pitches
    

'''
make_list_pitches expects a list of pitches with octaves and a list of lengths. 
It prepares to pitches list
then makes both lists the same length (through repetition)
then creates a stream that uses both lists through isorhtyhm
'''

def make_list_pitches (pitch_string, lengths):

    pitches = pitch_string.split()
    
    pitches = add_rests_to_pitches (pitches, lengths)
    
    
    if len(lengths) > len (pitches):
        pitches = repeat_to_length (pitches, len(lengths))
#    else:
#        lengths = repeat_to_length (lengths, len(pitches))

    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        n1 = note.Note()
        if lengths[i] >= 0:
            n1.duration.quarterLength = (4 * lengths[i])
            n1.pitch.name = pitches[i]
            stream1.append(n1)
        else:
            n1 = note.Rest()
            n1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(n1)
    stream1.show()
    return stream1

'''
binary_rhythm_map
'''

def binary_rhythm_map(binary_num, duration):
    result = []
    for i in range(len(binary_num)):
        if binary_num[i] == '0':
            result.append(duration * -1)
        elif binary_num[i] == '1':
            result.append(duration)
    return result

def how_many_negatives(a_list):
    counter = 0
    for i in a_list:
        if i <0 :
            counter +=1
    return counter

def how_many_rs(a_list):
    counter = 0
    for i in a_list:
        if i == 'r' :
            counter +=1
    return counter


''' 
'''

def makeBinaryRhythm (binary_num, pitch_string, duration, title = '', composer = ''):

    pitches = pitch_string.split()

    
    '''
    create lengths from binary number entered as a string
    '''
    lengths = binary_rhythm_map(binary_num, duration)
    '''
    make pitches and duration lists the same length
    '''

    if (len(lengths) + how_many_negatives (lengths)) > len (pitches):
        pitches = repeat_to_length (pitches, len(lengths))
    else:
        lengths = repeat_to_length (lengths, len(pitches))

    '''
    add rests to pitches list
    '''
    
    pitches = add_rests_to_pitches (pitches, lengths)
    lengths = repeat_to_length (lengths, (len(pitches)))



    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        n1 = note.Note()
        if lengths[i] >= 0:
            n1.duration.quarterLength = (4 * lengths[i])
            n1.pitch.name = pitches[i]
            stream1.append(n1)
        else:
            n1 = note.Rest()
            n1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(n1)
#    if display == '':
#        stream1.show()
#    else:
#        stream1.show(display)
    stream1.insert(0, instrument.Piano())
    stream1.insert(0, metadata.Metadata())
    stream1.metadata.title = title
    stream1.metadata.composer = composer

    return stream1

'''
prompt user for input
'''

#input_string = input("Enter a list pitches separated by space ")
#pitches  = input_string.split()
#binary_num = str(input("Enter a binary number for durations "))
#duration = float(input("Enter a duration "))
#
#print (pitches)

#print (binary_num)
#
#x = make_list_binary (pitches, binary_num, duration)
#
#x.show()


'''
example 

x = make_list_binary(['c4', 'd4', 'eb4', 'f4'] * 8, '10110110101011', 1/8)

x.show()

'''





def add_space (str):
    new_string = ''
    for i in range (len(str)):
        new_string += str[i]
        if str[i].isdigit():
            new_string += ' '
    return new_string



def biRhythm(numerator, denominator, pulse_duration, repetitions = 1, time_sig = '4/4', upper_pitches = 'c5', lower_pitches = 'c4', composer = 'you'):
    
    ts = meter.TimeSignature(time_sig)
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p0.insert(0, instrument.Piano())
    

    p1 = stream.Part(id='part1')
    p1.append(ts)    
    p1.insert(0, instrument.Piano())    

    dur0 = pulse_duration*denominator*4
    dur1 = pulse_duration*numerator*4
    
    upper = upper_pitches.split()
    lower = lower_pitches.split()

    
    for i in range (denominator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = upper[i % len(upper)]
        p0.append(n1)
        
    for i in range (numerator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = lower[i % len(lower)]
        p1.append(n1)
#    s.insert(0, metadata.Metadata())
#    s.metadata.title = 'title'
    s.insert(0, p0)
    s.insert(0, p1)  
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Bi Rhythm" + str(numerator) + "/" + str (denominator)  
    s.metadata.composer = composer
#    if display == 'inline':
#        s.show()
#    else: 
#        s.show(display)
#    s.insert(0, instrument.Guitar())
    
    return s




def intervalCycle(start, delta, number_of_steps):
    l = []
    if type(delta) == int:
        for i in range(number_of_steps):
            l.append(start)
            start += delta
        return l
    elif type(delta) == list:
        for i in range(number_of_steps):
            for j in delta:
                l.append(start)
                start += j
        return l
    

def midiToStream(midi_notes):
    stream1 = stream.Stream()

    for i in midi_notes:
        n1 = note.Note()
        n1.pitch.midi = i
        stream1.append(n1)
        
    return stream1
        
    
def replaceDurations(stream2, durations):
    stream1 = stream.Stream()
    counter = 0
    for i in stream2.pitches:
        n1 = note.Note()
        n1.pitch = i
        n1.duration.quarterLength = (4 * durations[counter])
        counter = (counter + 1) % len(durations)
        print(i)
        stream1.append(n1)
    stream1.show()
    
def cycletoNotes (start_note, delta, number_of_steps, output = ''):
    n1 = note.Note()
    n1.pitch.name = start_note
    start = n1.pitch.midi
    x = midiToStream(intervalCycle(start, delta, number_of_steps))
    x.show(output)
    return x

''' rotates a pitch string by given number of pitches (takes into account the existence of octaves and possibility of alternation of pitch'''


def rotatePitchString (pitch_list, how_much_to_rotate):
    x = -1 * how_much_to_rotate
    return (pitch_list[x:] + pitch_list [:x])


''' alternate_list_binary expects two pitch strings and a binary number and duration.
    it attaches pitch string 1 with the 1's in the binary number
    and pitch string 2 with the 0's in the binary number
'''

def alternate_list_binary (pitch_string1, pitch_string2, binary_num, duration, display = ''):
    output = []
    s1 = pitch_string1.split()
    s2 = pitch_string2.split()    
    for i in binary_num: 
        if i == '1':
            output += s1[:1]
            s1 = s1[-1:] + s1[:-1] 
        elif i == '0':
            output += s2[:1]
            s2 = s2[-1:] + s2[:-1]            
    
    stream1 = stream.Stream()
    
    for i in output:
        n1 = note.Note()
        n1.duration.quarterLength = 4*duration
        n1.pitch.name = i
        stream1.append(n1)
    if display == '':
        stream1.show()
    else: 
        stream1.show(display)

    return (stream1)
    
def numRhythm (numerical_list, pitches, duration, title = '', composer = ''):
    pitchlist = pitches.split()
    x = len (pitchlist)

    stream1 = stream.Stream()
    ts1 = meter.TimeSignature('4/4') # assumes two partitions
    stream1.timeSignature=ts1
            
    for i in range(len(numerical_list)):
        n1 = note.Note()
        n1.duration.quarterLength = 4 * numerical_list[i] * duration 
        n1.pitch.name = pitchlist [i % x]
        stream1.append(n1) 

#    stream2 = stream.Stream()
    

#    if display == '':
#        stream1.show()
#    else: 
#        stream1.show(display)
    stream1.insert(0, instrument.Piano())
    stream1.insert(0, metadata.Metadata())
    stream1.metadata.title = title
    stream1.metadata.composer = composer


    return (stream1)

def retro (pitch_list):
    str = ' '
    x = pitch_list.split()
    x.reverse()
    return (str.join(x) + ' ')
    

def division_biRhythm(numerator, denominator, division_duration, repetitions = 1, time_sig = '4/4', upper_pitches = 'c5', lower_pitches = 'c4', composer = 'you'):
    
    ts = meter.TimeSignature(time_sig)
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p0.insert(0, instrument.Piano())
    

    p1 = stream.Part(id='part1')
    p1.append(ts)    
    p1.insert(0, instrument.Piano())    

    dur0 = division_duration*4/numerator
    dur1 = division_duration*4/denominator
    
    
    
    for i in range (denominator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = 'c5'
        p0.append(n1)
        
    for i in range (numerator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = 'c4'
        p1.append(n1)
#    s.insert(0, metadata.Metadata())
#    s.metadata.title = 'title'
    s.insert(0, p0)
    s.insert(0, p1)  
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Bi Rhythm" + str(numerator) + "/" + str (denominator)  
    s.metadata.composer = composer
#    if display == 'inline':
#        s.show()
#    else: 
#        s.show(display)
#    s.insert(0, instrument.Guitar())
    
    return s

# Python3 program to convert a list 
# of integers into a single integer 
def convert(list): 
      
    # Converting integer list to string list 
    s = [str(i) for i in list] 
      
    # Join list items using join() 
    res = int("".join(s)) 
      
    return(res) 
  
    
'''
Bjorklund function from - https://github.com/brianhouse/bjorklund

The MIT License (MIT)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''


def bjorklund(steps, pulses):
    steps = int(steps)
    pulses = int(pulses)
    if pulses > steps:
        raise ValueError    
    pattern = []    
    counts = []
    remainders = []
    divisor = steps - pulses
    remainders.append(pulses)
    level = 0
    while True:
        counts.append(divisor // remainders[level])
        remainders.append(divisor % remainders[level])
        divisor = remainders[level]
        level = level + 1
        if remainders[level] <= 1:
            break
    counts.append(divisor)
    
    def build(level):
        if level == -1:
            pattern.append(0)
        elif level == -2:
            pattern.append(1)         
        else:
            for i in range(0, counts[level]):
                build(level - 1)
            if remainders[level] != 0:
                build(level - 2)
    
    build(level)
    i = pattern.index(1)
    pattern = pattern[i:] + pattern[0:i]
    return pattern

def E(steps, pulses):
    return (str(convert(bjorklund (steps, pulses))))



def biRhythm2(numerator, denominator, pulse_duration, repetitions = 1, time_sig = '4/4', upper_pitches = 'c5', lower_pitches = 'c4', composer = 'you'):
    
    ts = meter.TimeSignature(time_sig)
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p0.insert(0, instrument.Piano())
    

    p1 = stream.Part(id='part1')
    p1.append(ts)    
    p1.insert(0, instrument.Piano())    

    dur0 = pulse_duration*denominator*4
    dur1 = pulse_duration*numerator*4
    
    
    
    for i in range (denominator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = 'c5'
        p0.append(n1)
        
    for i in range (numerator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = 'c4'
        p1.append(n1)
#    s.insert(0, metadata.Metadata())
#    s.metadata.title = 'title'
    s.insert(0, p0)
    s.insert(0, p1)  
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Bi Rhythm" + str(numerator) + "/" + str (denominator)  
    s.metadata.composer = composer
#    if display == 'inline':
#        s.show()
#    else: 
#        s.show(display)
#    s.insert(0, instrument.Guitar())
    
    return s


def triRhythm(numerator, denominator, third, pulse_duration, repetitions = 1, time_sig = '4/4', upper_pitches = 'c5', lower_pitches = 'c4', middle_pitches = 'g4', composer = 'you'):
    
    ts = meter.TimeSignature(time_sig)
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p0.insert(0, instrument.Piano())
    

    p1 = stream.Part(id='part1')
    p1.append(ts)    
    p1.insert(0, instrument.Piano())    

    p2 = stream.Part(id='part2')
    p2.append(ts)    
    p2.insert(0, instrument.Piano())    

    
    dur0 = pulse_duration*denominator*4
    dur1 = pulse_duration*numerator*4
    dur2 = pulse_duration*third*4
    
    upper = upper_pitches.split()
    middle = middle_pitches.split()
    lower = lower_pitches.split()
    
    
    for i in range (denominator * third * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = upper[i % len(upper)]
        p0.append(n1)
        
    for i in range (numerator * third * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = lower[i % len(lower)]
        p1.append(n1)

        
    for i in range (numerator * denominator * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur2
        n1.pitch.name = middle[i % len(middle)]
        p2.append(n1)
        
#    s.insert(0, metadata.Metadata())
#    s.metadata.title = 'title'
    s.insert(0, p0)
    s.insert(0, p1) 
    s.insert(0, p2)
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Tri Rhythm" + str(numerator) + "/" + str (denominator)  + "/" +str (third)
    s.metadata.composer = composer
#    if display == 'inline':
#        s.show()
#    else: 
#        s.show(display)
#    s.insert(0, instrument.Guitar())
    
    return s


def fractioning (numerator, denominator, pulse_duration, repetitions = 1, time_sig = '3/4' , upper_pitches = 'c5', lower_pitches = 'c4', middle_pitches = 'g4', composer = 'you'):
    ts = meter.TimeSignature(time_sig)
    s = stream.Score(id='mainScore')
    p0 = stream.Part(id='part0')
    p0.append(ts)
    p0.insert(0, instrument.Piano())
    

    p1 = stream.Part(id='part1')
    p1.append(ts)    
    p1.insert(0, instrument.Piano())    

    p2 = stream.Part(id='part2')
    p2.append(ts)    
    p2.insert(0, instrument.Piano())    

    
    dur0 = pulse_duration*denominator*4
    dur1 = pulse_duration*numerator*4
    dur2 = dur1
    
    upper = upper_pitches.split()
    middle = middle_pitches.split()
    lower = lower_pitches.split()
    
    
    for i in range (denominator * 2 * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur1
        n1.pitch.name = upper[i % len(upper)]
        p0.append(n1)
        
    for i in range (numerator * 2 * repetitions):
        n1 = note.Note()
        n1.duration.quarterLength = dur0
        n1.pitch.name = lower[i % len(lower)]
        p1.append(n1)

    r1 = note.Rest()
    r1.duration.quarterLength = pulse_duration*denominator*numerator*2
    p2.append(r1)
    
    for i in range (numerator * denominator  ):
        n1 = note.Note()
        n1.duration.quarterLength = dur2
        n1.pitch.name = middle[i % len(middle)]
        p2.append(n1)
        
#    s.insert(0, metadata.Metadata())
#    s.metadata.title = 'title'
    s.insert(0, p0)
    s.insert(0, p1) 
    s.insert(0, p2)
    s.insert(0, metadata.Metadata())
    s.metadata.title = "Fractioning Rhythm" + str(numerator) + "/" + str (denominator)  
    s.metadata.composer = composer
#    if display == 'inline':
#        s.show()
#    else: 
#        s.show(display)
#    s.insert(0, instrument.Guitar())
    
    return s

def timelineCircle(pulses, onsets):

    import matplotlib.pyplot as plt
    import numpy as np

    (fig, ax) = plt.subplots(figsize = (6,6))
    
    def kex(N):
        alpha=2*np.pi/N
        alphas = alpha*np.arange(N)
        coordX = np.cos(alphas)
        coordY = np.sin(alphas)

        return np.c_[coordX, coordY, alphas]

    
    
    coord = []
    N = pulses
    points = kex(N)
    r = 1.2
    ax.scatter(points[:,0], points[:,1])
    offset = int((pulses - (pulses / 4) -1)) # necessary so the circle begins at the top
    reverse = pulses - 1 # necessary in order to label the dots clockwise
    modified_onsets = []

    for x in onsets:
        if (pulses % 2) == 0:
            modified_onsets.append(int(pulses /4) - x) # even number of pulses
        else: 
            modified_onsets.append(1 + int(pulses /4) - x) # odd number of pulses

    # create the circle 
    
    for i in range(0,N):
        a = points[i - offset ,2] 
        x,y = (r*np.cos(a), r*np.sin(a))
        if points[i,0] < 0: a = a - np.pi
        ax.text(x,y, str(reverse-i), ha="center", va="center",
                    bbox=dict(facecolor = "none", edgecolor ="red"))
    
    for i in modified_onsets:
        coord.append([points[i][0], points[i][1]]) #add polygon 
    
    coord.append(coord[0]) #repeat the first point to create a 'closed loop'

    xs, ys = zip(*coord) #create lists of x and y values

    plt.plot(xs,ys) 

    ax.axis("off")

    plt.show()
    
    return plt

''' the following function converts a numerical representation into onsets in a cycyle '''
    
def numToOnsets(lst):
    onsets = sum(lst)
    res = []
    counter = 0
    for i in lst:
        res.append(counter)
        counter += i
    return res
    
''' the following function plots a numerical represenation '''

def plotNumeric(timeline):
    pulses = sum (timeline)
    timelineCircle (pulses, numToOnsets(timeline))
    
    
def isorhythm (lengths, pitch_string, title = 'title', composer = 'composer'):
        
    pitches = pitch_string.split()
    

    if (len(lengths) + how_many_negatives (lengths)) > len (pitches):
        pitches = repeat_to_length (pitches, len(lengths))
    else:
        lengths = repeat_to_length (lengths, len(pitches))

    '''
    add rests to pitches list
    '''
    
    pitches = add_rests_to_pitches (pitches, lengths)
    lengths = repeat_to_length (lengths, (len(pitches)))



    stream1 = stream.Stream()
    
    for i in range(len(lengths)):
        n1 = note.Note()
        if lengths[i] >= 0:
            n1.duration.quarterLength = (4 * lengths[i])
            n1.pitch.name = pitches[i]
            stream1.append(n1)
        else:
            n1 = note.Rest()
            n1.duration.quarterLength = (-4 * lengths[i]) 
            stream1.append(n1)
#    if display == '':
#        stream1.show()
#    else:
#        stream1.show(display)
    stream1.insert(0, instrument.Piano())
    stream1.insert(0, metadata.Metadata())
    stream1.metadata.title = title
    stream1.metadata.composer = composer

    return stream1



def onsets(binary_list):
    result = []
    for i in range(len(binary_list)):
        if binary_list[i] == '1':
            result.append(i)
    return (result)


def plotBinaryRhythm(binary_list):
    onset_list = onsets(list(binary_list))
    pulses = len(binary_list)
    print ("number of pulses is: " + str(pulses)) 
    print ("onsets are on " + str(onset_list) + " pulses")
    timelineCircle (pulses, onset_list)
#    timelineCircle (len(binary_list), onsets(list(binary_list)))



def PCStoPitches(PCS_list, octave_list):
    res = '' 
    for i in PCS_list:
        if i == 0: 
            res += 'C' + str(random.choice(octave_list)) + ' '
        elif i == 1: 
            res += 'C#' + str(random.choice(octave_list)) + ' '
        elif i == 2: 
            res += 'D'+ str(random.choice(octave_list)) + ' '
        elif i == 3: 
            res += 'Eb'+ str(random.choice(octave_list)) + ' '
        elif i == 4:
            res += 'E'+ str(random.choice(octave_list)) + ' '
        elif i == 5:
            res += 'F'+ str(random.choice(octave_list)) + ' '
        elif i == 6:
            res += 'F#'+ str(random.choice(octave_list)) + ' '
        elif i == 7: 
            res += 'G'+ str(random.choice(octave_list)) + ' '
        elif i == 8: 
            res += 'G#'+ str(random.choice(octave_list)) + ' '
        elif i == 9: 
            res += 'A'+ str(random.choice(octave_list)) + ' '
        elif i == 10: 
            res += 'Bb'+ str(random.choice(octave_list)) + ' '
        elif i == 11:
            res += 'B'+ str(random.choice(octave_list)) + ' '
    return (res)

def sortAscMidi(score):
    # get the pitch number for each note
    temp = [i.pitch.midi for i in score.flat.notes]
    
    # and sort them in ascending order
    temp.sort()
    temp = list(dict.fromkeys(temp))
    return (temp)


def sortAsc(s):
    res = ''
    for x in sortAscMidi(s):
        p = str(pitch.Pitch(x))
        res += p + ' '
    return (res)


def sortChordAsc(s):
    res = ''
    for x in sortChordAscMidi(s):
        p = str(pitch.Pitch(x))
        res += p + ' '
    return (res)
    
    
def sortChordAscMidi(score):
    # get the pitch number for each note
    temp = [i.pitch.midi for i in score.notes]
    
    # and sort them in ascending order
    temp.sort()
    temp = list(dict.fromkeys(temp))
    return (temp)


def showChord(chord):
    showScore(makeBinaryRhythm('1', sortChordAsc(pc_set), 1/4))

def T(n = 0, original_set = []):
    return [(element + n) % 12 for element in original_set] 

def I(n = 0, original_set = []):
    return [(n - element)%12 for element in original_set] 

def showandplay(s):
    showScore(s)
    sp = midi.realtime.StreamPlayer(s)
    sp.play()
    
def sortAsc (chord):
    s = stream.Stream()
    for i in (chord):
        s.append(i)
    
    s.show()
    
def plotPCSet (the_set):
    timelineCircle(12, the_set)
