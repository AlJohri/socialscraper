from tasks import add
result = add.delay(4, 4)

print result.get() # block
print result.ready()