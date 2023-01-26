hlextend
========

Pure Python Hash Length Extension module.

Currently supports SHA1, SHA256 and SHA512, more algorithms will
be added in the future.


Create a hash by calling one of the named constuctor functions:
sha1(), sha256(), and sha512(), or by calling new(algorithm).

The hash objects have the following methods:

	hash(message):      

	    Feeds data into the hash function using the normal interface.

	extend(appendData, knownData, secretLength, startHash):

	    Performs a hash length extension attack.  Returns the bytestring to
	    use when appending data.

	hexdigest():        

	    Returns a hexlified version of the hash output.


Assume you have a hash generated from an unknown secret value concatenated with
a known value, and you want to be able to produce a valid hash after appending 
additional data to the known value.

If the hash algorithm used is one of the vulnerable functions implemented in
this module, is is possible to achieve this without knowing the secret value
as long as you know (or can guess, perhaps by brute force) the length of that
secret value.  This is called a hash length extension attack. 


Given an existing sha1 hash value '52e98441017043eee154a6d1af98c5e0efab055c',
known data of 'hello', an unknown secret of length 10 and data you wish
to append of 'file', you would do the following to perform the attack:

	>>> import hlextend
	>>> sha = hlextend.new('sha1')
	>>> print(sha.extend(b'file', b'hello', 10, '52e98441017043eee154a6d1af98c5e0efab055c'))
	b'hello\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00xfile'
	>>> print(sha.hexdigest())
	c60fa7de0860d4048a3bfb36b70299a95e6587c9


The unknown secret (of length 10), that when hashed appended with 'hello' produces
a SHA1 hash of '52e98441017043eee154a6d1af98c5e0efab055c', will then produce 
a SHA1 hash of 'c60fa7de0860d4048a3bfb36b70299a95e6587c9' when appended with the output 
from the extend function above.

If you are not sure of the exact length of the secret value, simply try the above
multiple times specifying different values for the length to brute force.
