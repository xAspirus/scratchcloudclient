CHAR_ORDER = [ "0","1","2","3","4","5","6","7","8","9","!",'"',"#","%", "&","'", 
               "(",")","*","+",",","-",":",";","<","=",">","?","@","[","\\","]",
               "^","_","`","{","|","}","~","$","a","A","b","B","c","C", "d","D", 
               "e","E","f","F","/",".","g","G","h","H","i","I","j","J", "k","K", 
               "l","L","m","M","n","N","o","O","p","P","q","Q","r","R", "s","S", 
               "t","T","u","U","v","V","w","W","x","X","y","Y","z","Z", " " ]


def encode_str(in_str :str):
	"""
	Encode a string into 2-digit decimal encoding
	(Check CHAR_ORDER for order)
	(Encoding function provided in Scratch Library)
	"""
	return ''.join(f'{1 + CHAR_ORDER.index(i)}:02' for i in in_str)

def decode_str(in_str :str):
	"""
	Decode a string from 2-digit decimal encoding
	(Check CHAR_ORDER for order)
	(Decoding function provided in Scratch Library)
	"""
	return ''.join(CHAR_ORDER[int(in_str[i:i+2]) - 1] for i in range(0, len(in_str), 2))

def encode_list(in_list :list):
	"""
	Encode a list of strings into 2-digit decimal encoding
	separated by 00's
	(Encoding function provided in Scratch Library)
	"""
	return '00'.join(encode_str(i) for i in in_list)

def decode_list(in_str: str):
	"""
	Decode a list of strings from 2-digit decimal encoding
	separated by 00's
	(Decoding function provided in Scratch Library)
	"""
	return [decode_str(i) for i in in_str.split('00')]
