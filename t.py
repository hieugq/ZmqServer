import json

s = "b[b'R01', b'TraCuu', b'DSNhanVien', 'ALL']"
s = s.strip('b[]')

l = [x for x in s.split(',')]
l.append('test')

req = [b'R01', b'TraCuu', 'DSNhanVien', 'ALL']

print(5/2)
print(round(2.5, 1))