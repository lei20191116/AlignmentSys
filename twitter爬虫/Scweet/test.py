from queue import Queue

qurl = Queue()

datelist = []
for y in range(2010, 2022):
    for i in range(1, 13):
        date1 = "{y}-{m}-1".format(y=y, m=i)
        date2 = "{y}-{m}-14".format(y=y, m=i)
        datelist.append(date1)
        datelist.append(date2)
print(datelist)
for i in range(len(datelist)):
    print(i)
    if i != 287:
        qurl.put((datelist[i], datelist[i + 1]))
print(qurl)

