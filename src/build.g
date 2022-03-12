# Write : function (text,end)
{
    write (Str text)+(Str end)
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
# conv : function (type,var)
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

# __version__ : '0.1'