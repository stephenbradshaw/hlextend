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


reference = [ 'abc',
'The quick brown fox jumped over the lazy dog',
'The quick brown fox jumped over the lazy dog.',
"abcdbcdecdefdefgefghfghighijhijkijkljklmklmnlmnomnopnopq",
urandom(30)]


# comparitive hash generation test with hashlib, check basic hash generation functionality
for alg in algorithms: 
	for a in range(0,256):
		string = 'A'*a
		h = hashlib.new(alg)
		h.update(string)
		test1 = h.hexdigest()
		s = hlextend.new(alg)
		s.hash(string)
		test2 = s.hexdigest()
		if not test1 == test2:
			print alg + ' no match for string of length ' + str(a)
			print 'Hashlib:  ' + test1
			print 'Hlextend: ' + test2
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
			print 'Reference value check failed for ' + alg + ' on value ' + ref
			print 'Hashlib:  ' +  hhex
			print 'Hlextend: ' + shex
			raise TerminateTest('Verification failure')



# various checks of the hash length extension functionality
for alg in algorithms:
	print 'Testing extension function for ' + alg	
	for secLen in xrange(10, 130, 20):
		secret = 'B' * secLen
		for knownLen in xrange(60, 130, 1):
			known = 'A' * knownLen
			for appendLen in xrange(10,50, 10):
				append = 'CCC' * appendLen
				sh = hashlib.new(alg)
				sh.update(secret+known)
				startHash = sh.hexdigest()
				s = hlextend.new(alg)
				appendVal = s.extend(append, known, secLen, startHash, raw=True)			
				appendVal1 = ''.join([byter(ord(a)) for a in appendVal])
				appendHash = s.hexdigest()			
				sh.update(appendVal.replace(known, ''))
				newHash = sh.hexdigest()
				if not appendHash == newHash:
					gh = hlextend.new(alg)
					gh.hash(secret+appendVal)
					print 'Algorithm: ' + alg
					print 'Start hash: ' + startHash
					print 'Appen hash: ' + appendHash
					print 'Newa  hash : ' + gh.hexdigest()
					print 'New   hash: ' + newHash
					print 'Secret: ' + secret
					print 'Known: ' + known
					print 'Base append: ' + append
					print appendVal1
					raise TerminateTest('Verification failure')
				


