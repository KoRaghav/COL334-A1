import os, sys
dest = sys.argv[1]

exceeded = True
c = 1
print("traceroute to " + dest)
while (exceeded):
    alt = None
    print('\u2006',c, end='   ')
    for i in range(3):
        x = [y.split() for y in os.popen('ping '+dest+' -c1 -w1 -t'+str(c)).read().split('\n')]
        if x[1]:
            curExceeded = x[1][-1]=='exceeded'
            exceeded &= curExceeded
            if curExceeded:
                destDom = x[1][1]
                destIP = x[1][2]
                if destIP[:8]=="icmp_seq": destIP = '('+destDom+')'
            else:
                destDom = x[1][3]
                destIP = x[1][4][:-1]
                if destIP[:8]=="icmp_seq":
                    destDom = destDom[:-1]
                    destIP = '('+destDom+')'
            z = [y.split() for y in os.popen('ping '+ destIP[1:-1] +' -c1 -w1').read().split('\n')]
            if z[1] and z[1][-1]!='exceeded':
                key, value = z[1][-2].split('=')
                value += ' ms'
            else:
                value = ' *'
            if destIP != alt:
                print(destDom,' '+ destIP, value, end=' ')
                alt = destIP
            else:
                print(value, end=' ')
        else:
            print(' *',end=' ')
    print('')
    c+=1

