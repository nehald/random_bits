from  tt import foo

class bar(foo):
	def __init__(self):
		foo.__init__(self)
	def c(self):
		print 'c'
	def d(self):
		print 'd'


B = bar()
B.a()
print B.aa
