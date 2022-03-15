# Write : function (text)
{
    write (Str text)+'\n'
	
}
# Input : function (type)
{
    #x : input
    if type = 'int'
        return Int x
    else if type = 'float'
        return Float x
    else if type = 'string'
        return Str x
    else
        return null
}
# len : function (list)
{
	return Len list
}
# conv : function (type, var)
{
	if type = 'int'
        return Int var
    else if type = 'float'
        return Float var
		
    else if type = 'string'
        return Str var
    else
        return null
}
# is_set : function (var)
{
	if var = null
		return False
	else
		return True
}

# is_instance : function (var , type)
{
	if conv(type,var) = var
		return True
	else
		return False
		
}

# pow : function (p , w)
{
	if w = 0
		return 1
	else
		return p * pow(p,w-1)
}