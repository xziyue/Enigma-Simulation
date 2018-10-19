import re

pat = '\((\w*)\)'

text = '(AR) (BD) (CO) (EJ) (FN) (GT) (HK) (IV) (LM) (PW) (QZ) (SX) (UY)'
text = re.sub('\\s', '', text)

res = re.findall(pat, text)

final = ''
for str in res:
    final += '(\emph{{{}}})'.format(str)


print(final)