class user_information:
    username=['cqy',
    'hyl',
    'zzy',
    'mdh',
    '']
    userpsk=['19990331cqy',
    '',
    '',
    '',
    '']
    cnuser=['陈祺遥',
    '韩远亮',
    '张智阳',
    '马登辉',
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



   