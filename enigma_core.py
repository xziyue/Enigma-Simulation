from enigma_json_parser import enigma_database
from enigma_entity import *
from alphabet_conversion import *


class Enigma:
    reflector = None
    rotors = None
    plugboard = None

    def __init__(self):
        self.reflector = Reflector()
        self.rotors = []
        self.plugboard = Plugboard()

    def RecursiveRotate(self, n, rotateThis):
        advanced = False
        rotateNext = False
        # rotateThis is true means that this rotor is forced to
        # rotate by the rotor to the right
        if rotateThis:
            advanced = True
            if self.rotors[n].OnNotch():
                rotateNext = True
            self.rotors[n].Advance()
        # the last rotor does not have a notched ring, so the next condition
        # is not considered
        if n == 0:
            return
        # check if this is on notch and not advanced
        # if so, we need to perform a double step
        if self.rotors[n].OnNotch() and not advanced:
            rotateNext = True
            self.rotors[n].Advance()
        self.RecursiveRotate(n - 1, rotateNext)

    def Step(self):
        self.RecursiveRotate(len(self.rotors) - 1, True)

    def Encrypt(self, code):
        # the code goes through the plugboard
        plugboardCode = self.plugboard.forward[code]
        # the array indicating which rotor is advanced
        #advanced = [False] * len(self.rotors)
        self.RecursiveRotate(len(self.rotors) - 1, True)
        # propagate the value through rotors
        rotorForwardCode = plugboardCode
        for i in range(len(self.rotors) - 1, -1, -1):
            rotorForwardCode = self.rotors[i].GetForward(rotorForwardCode)
        # the code reaches the reflector
        reflectedCode = self.reflector.forward[rotorForwardCode]
        # the code propagate back through rotors
        rotorBackwardCode = reflectedCode
        for i in range(len(self.rotors)):
            rotorBackwardCode = self.rotors[i].GetBackward(rotorBackwardCode)
        # the code goes back through the plugboard
        finalCode = self.plugboard.backward[rotorBackwardCode]
        return finalCode


enigma = Enigma()
enigma.reflector = enigma_database.reflectors[0]
enigma.rotors.append(enigma_database.rotors[2])
enigma.rotors.append(enigma_database.rotors[1])
enigma.rotors.append(enigma_database.rotors[0])
enigma.rotors[-3].pos = 1
enigma.rotors[-2].pos = 1
enigma.rotors[-1].pos = 1

counter = 0

while True:
    enigma.Encrypt(0)
    counter += 1
    allPos = [enigma.rotors[i].pos for i in range(3)]
    pred = all(map(lambda x : x == 1, allPos))
    if pred:
        break

print(counter)

'''
enigma.reflector = enigma_database.reflectors[0]
# enigma.plugboard = enigma_database.plugboards[0]
for i in range(3):
    enigma.rotors.append(enigma_database.rotors[i])
enigma.rotors[-3].pos = 23
enigma.rotors[-2].pos = 24
enigma.rotors[-1].pos = 25
enigma.plugboard.Plug(Alph2Int('A'), Alph2Int('Z'))
enigma.plugboard.Plug(Alph2Int('B'), Alph2Int('Y'))
enigma.plugboard.Plug(Alph2Int('C'), Alph2Int('X'))
enigma.plugboard.Plug(Alph2Int('D'), Alph2Int('W'))

print([(i, Int2Alph(i)) for i in range(26)])


plain = ''
for globalI in range(200):
    print('A', end = '')
    plain += 'A'
print(' ')

for ind, ele in enumerate(plain):
    print(Int2Alph(enigma.Encrypt(Alph2Int(ele))), end = '')

print('\ntest')
'''

'''
plain = ''
for globalI in range(780):
    ind = globalI % 26
    print(Int2Alph(ind), end = '')
    plain += Int2Alph(ind)
print(' ')

for ind, ele in enumerate(plain):
    print(Int2Alph(enigma.Encrypt(Alph2Int(ele))), end = '')
    if (ind + 1) % 4 == 0:
        print(' ', end = ' ')

print('\ntest')
'''