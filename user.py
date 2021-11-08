class user_information:
    username=['1',
    '2',
    '3',
    '4',
    '']
    userpsk=['',
    '',
    '',
    '',
    '']
    cnuser=['嘤嘤嘤',
    '二二二',
    '三三三',
    'fff',
    'test']
    userid=0
    def searchcount(name,psk):
        nameflag=0
        for num in range(0,len(user_information.username)):
            if name==user_information.username[num]:
                if psk==user_information.userpsk[num]:
                    nameflag=1
                    user_information.userid=num
                    return 1
                else:
                    return 2   
        if nameflag==0:
            return 3



   