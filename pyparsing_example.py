from pyparsing import punc8bit,OneOrMore,nums,Word, alphas,Group
import pymongo
# define grammar
quotes = '"'
colon = ":"
title = quotes+"title"+quotes


punc = '/'+"("+")"+"."+"-"+","+"'"+"&"+"?"+"!"+"*"+"+"+"#"+"@" 
punc = punc +"%"+"="+";"+"~"+"`"+"|"+"$"+"\\" 
val = quotes+Group(OneOrMore(Word(alphas+nums+punc)))+quotes

lbracket = '{'
rbracket = '}'
lparen = "("
rparen = "("
# sample line from file 
## (12 {"title":"Autism fooo"}) 

val = Word(nums)+lbracket+title+colon+val+rbracket
for i in open("/tmp/nohup.out"):
	try:
		strng = i[1:-1]   
     		val_array= val.parseString(strng)
		print val_array[0]," ".join(val_array[5])
	except:
		pass;
