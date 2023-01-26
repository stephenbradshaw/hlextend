import hlextend
sha = hlextend.new('sha1')

print(sha.extend(b'file', b'hello', 10, '52e98441017043eee154a6d1af98c5e0efab055c'))
print(sha.hexdigest())
