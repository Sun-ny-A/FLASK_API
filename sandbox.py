#ex of how to use dict update 


instructor_dict = {'name':'dylan','class':'matrix'}


# instructor_dict.update({'class':'matrix','hobby':'running pool table'})

instructor_dict |= {'class':'matrix','hobby':'running pool table'}

print(instructor_dict)