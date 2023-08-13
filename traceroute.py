import os, sys
dest = sys.argv[1]

ttl = 1
print("traceroute to " + dest)
# Continue untill ttl is exceeded
exceeded = True
while (exceeded):    
    alt = None # Stores the previous router to check if they are same
    print('\u2006',ttl, end='   ')
    for i in range(3):
        ping = [y.split() for y in os.popen('ping '+dest+' -c1 -w1 -t'+str(ttl)).read().split('\n')]
        # if router responds
        if ping[1]:            
            curExceeded = ping[1][-1]=='exceeded' # check if current router exceeds ttl
            exceeded &= curExceeded
            if curExceeded:
                destDom = ping[1][1]
                destIP = ping[1][2]
                if destIP[:8]=="icmp_seq": destIP = '('+destDom+')'
            else:
                destDom = ping[1][3]
                destIP = ping[1][4][:-1]
                if destIP[:8]=="icmp_seq":
                    destDom = destDom[:-1]
                    destIP = '('+destDom+')'
            # ping the intermediate router to determine time taken
            ping2 = [y.split() for y in os.popen('ping '+ destIP[1:-1] +' -c1 -w1').read().split('\n')]
            if ping2[1] and ping2[1][-1]!='exceeded':
                key, value = ping2[1][-2].split('=')
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
    ttl+=1

