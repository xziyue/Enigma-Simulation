import re
import json
from alphabet_conversion import *
from enigma_entity import *

json_obj = None
with open('enigma_spec.json', 'r') as infile:
    json_obj = json.load(infile)

def CancelBlank(text):
    return re.sub(r'\s', r'', text)

regex_extract_within_parenthesis = r'\(([^)]+)\)'
def ParseRotorPattern(text):
    forward = [None] * 26
    cycles = re.findall(regex_extract_within_parenthesis, CancelBlank(text))
    existedCode = set()
    for cycle in cycles:
        for i in range(len(cycle)):
            code = Alph2Int(cycle[i])
            assert code not in existedCode
            existedCode.add(code)
            if i == len(cycle) - 1:
                forward[code] = Alph2Int(cycle[0])
            else:
                forward[code] = Alph2Int(cycle[i + 1])
    assert len(existedCode) == 26
    return forward

def ParseReflectorPattern(text):
    forward = [None] * 26
    cycles = re.findall(regex_extract_within_parenthesis, CancelBlank(text))
    existedCode = set()
    for cycle in cycles:
        assert len(cycle) == 2
        codes = [Alph2Int(cycle[0]), Alph2Int(cycle[1])]
        for code in codes:
            assert code not in existedCode
            existedCode.add(code)
        forward[codes[0]] = codes[1]
        forward[codes[1]] = codes[0]
    assert len(existedCode) == 26
    return forward

def ParsePlugboards(jsonObj):
    plugboardRoot = jsonObj['plugboards']
    result = []
    for item in plugboardRoot:
        plugboard = Plugboard()
        plugboard.name = item['name']
        pairs = re.findall(regex_extract_within_parenthesis, CancelBlank(item['pattern']))
        for pair in pairs:
            plugboard.Plug(Alph2Int(pair[0]), Alph2Int(pair[1]))
        result.append(plugboard)
    return result


def ParseRotors(jsonObj):
    rotorRoot = jsonObj['rotors']
    result = []
    for item in rotorRoot:
        rotor = Rotor()
        rotor.name = item['name']
        rotor.forward = ParseRotorPattern(item['pattern'])
        rotor.forwardReference = [Int2Alph(i) for i in rotor.forward]
        rotor.notch = [Alph2Int(i) for i in item['notch'].strip().split(' ')]
        rotor.GenerateBackward()
        result.append(rotor)
    return result

def ParseReflectors(jsonObj):
    reflectorRoot = jsonObj['reflectors']
    result = []
    for item in reflectorRoot:
        reflector = Reflector()
        reflector.name = item['name']
        reflector.forward = ParseReflectorPattern(item['pattern'])
        reflector.forwardReference = [Int2Alph(i) for i in reflector.forward]
        result.append(reflector)
    return result

class EnigmaDatabase:
    rotors = None
    reflectors = None
    plugboards = None

    def __init__(self):
        self.rotors = []

enigma_database = EnigmaDatabase()
enigma_database.rotors = ParseRotors(json_obj)
enigma_database.reflectors = ParseReflectors(json_obj)
enigma_database.plugboards = ParsePlugboards(json_obj)





