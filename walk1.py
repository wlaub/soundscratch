import math
import random

import sounddevice as sd

def fixed(f):
    return lambda i: f

def sliding(f1, f2, N):
    return lambda i: f1*(1-i/float(N))+f2*(i/float(N))

def walk():
    r = random.random()*2-1
    return 1 if r > 0 else -.99

def tone(N):
    def func(phase):
        coeffs = [2**n/12. for n in range(4)]    
        v = sum([x*math.sin(phase*(i+N)) for i,x in enumerate(coeffs)])
        return v
    return func

def do_sound(vals, f, l, phase, w, tfunc, wfunc = walk):
    accum = 0
    for i in range(int(l)):
        vals.append(tfunc(phase))
        phase += 6.28*(f(i)+accum)/fs
        accum += w*wfunc()
    return phase


fdiv = 20.
N = 15000
f = 100./fdiv
fs = 44100
ratio = 3

w = .1/fdiv

l1 = 2
l2 = 5
ls = .5

phase = 0
vals = []

for j in range(10):
    f+=walk()/fdiv
    ratio += .01*walk()
    f1 = ratio*f
    f2 = f

    phase = do_sound(vals, fixed(f1), N*(l1-ls), phase, w, tone(15+j))
    phase = do_sound(vals, sliding(f1, f2, N*ls), N*ls, phase, w, tone(15+j))
    phase = do_sound(vals, fixed(f2), N*l2, phase, w, tone(15+j))

sd.play(vals, blocking = True, samplerate=fs)

