#!/usr/bin/env python

# test script for hlextend
import hlextend
import hashlib
from os import urandom

algorithms = hlextend.__all__

class TerminateTest(Exception):
	pass


def byter(byteVal):
    '''Helper function to return usable values for hash extension append data'''
    if byteVal < 0x20 or byteVal > 0x7e:
        return '\\x%02x' %(byteVal)
    else:    
        return chr(byteVal)


reference = [
    b'abc',
	b'The quick brown fox jumped over the lazy dog',
	b'The quick brown fox jumped over the lazy dog.',
	b'abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq',
	urandom(30)
]


# comparitive hash generation test with hashlib, check basic hash generation functionality
for alg in algorithms: 
	for a in range(0,256):
		string = b'A'*a
  
		h = hashlib.new(alg)
		h.update(string)
		test1 = h.hexdigest()
  
		s = hlextend.new(alg)
		s.hash(string)
		test2 = s.hexdigest()
  
		if not test1 == test2:
			print(alg + ' no match for string of length ' + str(a))
			print('Hashlib:  ' + test1)
			print('Hlextend: ' + test2)
			raise TerminateTest('Verification failure')


# check reference hash values
for alg in algorithms:
	for ref in reference:
		s = hlextend.new(alg)
		s.hash(ref)
		h = hashlib.new(alg)
		h.update(ref)
		hhex = h.hexdigest()
		shex = s.hexdigest()
		if not hhex == shex:
			print('Reference value check failed for ' + alg + ' on value ' + ref)
			print('Hashlib:  ' +  hhex)
			print('Hlextend: ' + shex)
			raise TerminateTest('Verification failure')



# various checks of the hash length extension functionality
for alg in algorithms:
	print('Testing extension function for ' + alg)
 
	for secLen in range(10, 130, 20):
		secret = b'B' * secLen
  
		for knownLen in range(60, 130, 1):
			known = b'A' * knownLen
   
			for appendLen in range(10, 50, 10):
				append = b'CCC' * appendLen
				sh = hashlib.new(alg)
				sh.update(secret + known)
				startHash = sh.hexdigest()
    
				s = hlextend.new(alg)
				appendVal = s.extend(append, known, secLen, startHash)
				appendVal1 = ''.join([byter(a) for a in appendVal])
				appendHash = s.hexdigest()			
				sh.update(appendVal.replace(known, b''))
				newHash = sh.hexdigest()
    
				if appendHash != newHash:
					gh = hlextend.new(alg)
					gh.hash(secret+appendVal)
					print('Algorithm: ' + alg)
					print('Start hash: ' + startHash)
					print('Append hash: ' + appendHash)
					print('New a hash : ' + gh.hexdigest())
					print('New hash: ' + newHash)
					print('Secret: ' + secret.decode())
					print('Known: ' + known.decode())
					print('Base append: ' + append.decode())
					print(appendVal1)
					raise TerminateTest('Verification failure')
