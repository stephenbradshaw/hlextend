# using old python2 ide to work out discrepancies
# https://www.jdoodle.com/python-programming-online/

import hlextend
import hashlib

alg = 'sha1'
string = b'A' * 200

h = hashlib.new(alg)
h.update(string)
test1 = h.hexdigest()

s = hlextend.new(alg)
s.hash(string)
test2 = s.hexdigest()

print(test1)
print(test2)


k = ''.join([bin(a)[2:].rjust(8, "0") for a in string])
k2 = ''.join([bin(ord(a))[2:].rjust(8, "0") for a in ('A' * 200)])
