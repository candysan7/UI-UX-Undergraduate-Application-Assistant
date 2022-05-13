def qadd(additionals, major, act,  activism, community):
    query = ''
    if 'Homeless' in additionals:
        query = 'category = "Homeless"'
    if 'Adopted/Foster Child/Orphan' in additionals:
        if query == '':
            query = 'category = "Adopted/Foster Child/Orphan"'
        else:
            query = query + ' or category = "Adopted/Foster Child/Orphan"'
    if 'Single Parent Household' in additionals:
        if query == '':
            query = 'category =  "Single Parent"'
        else:
            query = query + ' or category = "Single Parent"'        
    if 'LGBTQ+' in additionals:
        if query == '':
            query = 'category = "LGBTQ+"'
        else:
            query = query + ' or category ="LGBTQ+"'    
    if 'First Generation' in additionals:
        if query == '':
            query = 'category = "First Generation"'
        else:
            query = query + ' or category = "First Generation"'
    if 'Immigrant' in additionals:
        if query == '':
            query = 'category = "Immigrant"'
        else:
            query = query + ' or category = "Immigrant"'    
    if 'Native American' in additionals:
        if query == '':
            query = 'category = "Native American"'
        else:
            query = query + ' or category = "Native American"'
    if 'Female' in additionals:
        if query == '':
            query = 'category = "Women"'
        else:
            query = query + ' or category = "Women"'        
    if community == 'Yes':
        if query == '':
            query = 'category = "Community"'
        else:
            query = query + ' or category = "Community"'  
    if activism == 'Yes':
        if query == '':
            query = 'category = "Activism"'
        else:
            query = query + ' or category = "Activism"'        
    if act >= 19:
        if query == '':
            query = '(category = "Academic" and act <= ' + str(act) + ')'
        else:
            query = query + ' or (category = "Acamemic" and act <= ' + str(act) + ')'
    if major == 'Other':
        query = query + ';'
    else:
        query = query + ' or category = "' + major + '";'
    if query == ";":
        return 'category = "x";'
    else:
        return query