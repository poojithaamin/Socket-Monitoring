#Network socket monitoring tool
# pylint: disable-msg=C0103
from collections import defaultdict, Counter
import psutil
import operator

conn_list = []
for p in psutil.net_connections(kind='tcp'):
    #Check if laddr, raddr and pid exists
    if  any(p.laddr) and any(p.raddr) and p.pid is not None:
        laddr_var = str(p.laddr)
        laddr_var = laddr_var.replace(',', '@')
        laddr_var = laddr_var.translate(None, "()'' ")
        raddr_var = str(p.raddr)
        raddr_var = raddr_var.replace(',', '@')
        raddr_var = raddr_var.translate(None, "()'' ")
        conn_var = (p.pid, laddr_var, raddr_var, p.status)
        conn_list.append(conn_var)

#Implement without using group by
"""
#Get number of connections per process
freq = Counter(process[0] for process in conn_list)

#Group by PID and sort the output by the number of connections
conn_list = sorted(conn_list, key=operator.itemgetter(0))
sorted_list = sorted(conn_list, key=lambda i: freq[i[0]], reverse=True)

#Print the sorted list
print '\"pid\",\"laddr\",\"raddr\",\"status\"'
for field in sorted_list:
    print '"%s","%s","%s","%s"' %(field[0], field[1], field[2], field[3])
"""

#Implement using group by
conn_list.sort(key = itemgetter(0))

#Group by PID and sort the output by the number of connections
group_list = [list(v) for k,v in groupby(conn_list, key = itemgetter(0) )]
group_list.sort(key = len, reverse=True)

group_list=list( chain.from_iterable(group_list))
print '\"pid\",\"laddr\",\"raddr\",\"status\"'
for field in group_list:
    print '"%s","%s","%s","%s"' %(field[0], field[1], field[2], field[3])

