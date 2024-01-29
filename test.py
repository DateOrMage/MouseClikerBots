# test gui

a = '3.00010'

sp = a[a.find('.'):]
fp = a[:a.find('.')]
new_sp = ''
flag = False
for el in sp[::-1]:
    if el == '0' and not flag:
        pass
    else:
        flag = True
        new_sp += el
new_sp = new_sp[::-1]
print(fp+new_sp)