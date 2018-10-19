from alphabet_conversion import *

class TwoWayMapping:
    forward = None
    backward = None
    forwardReference = None
    backwardReference = None

    def __init__(self):
        self.SetDefault()

    def SetDefault(self):
        self.forward = list(range(26))
        self.forwardReference = [Int2Alph(i) for i in self.forward]
        self.GenerateBackward()

    # given forward list, generate the backward list
    def GenerateBackward(self):
        assert len(self.forward) == 26
        self.backward = [None] * 26
        visited = set()
        for i in range(len(self.forward)):
            assert self.forward[i] not in visited
            visited.add(self.forward[i])
            self.backward[self.forward[i]] = i
        self.backwardReference = [Int2Alph(i) for i in self.backward]


class OneWayMapping:
    forward = None
    forwardReference = None

    def __init__(self):
        self.SetDefault()


    def SetDefault(self):
        self.forward = list(range(26))
        self.forwardReference = [Int2Alph(i) for i in self.forward]

class Rotor(TwoWayMapping):
    name = None
    notch = None
    pos = None

    def __init__(self):
        super(TwoWayMapping).__init__()
        self.SetDefault()
        self.name = 'noname'
        self.notch = [0]
        self.pos = 0

    def Advance(self):
        self.pos = (self.pos + 1) % 26

    '''
        The modulo arithmetic taken for GetForward()
        and GetBackward() should be comprehended in
        the following way.
    '''
    def GetForward(self, code):
        ind = (code + self.pos) % 26
        return (self.forward[ind] - self.pos) % 26

    def GetBackward(self, code):
        ind = (code + self.pos) % 26
        return (self.backward[ind] - self.pos) % 26

    def OnNotch(self):
         return (self.pos + 1) % 26 in self.notch

class Reflector(OneWayMapping):
    name = None

    def __init__(self):
        super(OneWayMapping).__init__()
        self.SetDefault()
        self.name = 'noname'

class Plugboard(TwoWayMapping):
    name = None
    plugs = None

    def __init__(self):
        super(TwoWayMapping).__init__()
        self.plugs = []
        self.SetDefault()
        self.name = 'noname'

    def Plug(self, code1, code2):
        assert code1 != code2
        allCode = []
        for item in self.plugs:
            allCode.append(item[0])
            allCode.append(item[1])
        assert code1 not in allCode
        assert code2 not in allCode
        sortedCode = sorted([code1, code2])
        self.plugs.append(sortedCode)
        self.forward[code1] = code2
        self.forward[code2] = code1
        self.GenerateBackward()

    def Unplug(self, code1, code2):
        sortedCode = sorted([code1, code2])
        index = self.plugs.index(sortedCode)
        assert index != -1
        self.forward[code1] = code1
        self.forward[code2] = code2
        self.plugs.pop(index)
        self.GenerateBackward()


