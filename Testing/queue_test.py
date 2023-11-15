#A quick test of how queues work in python

import queue
q = queue.Queue()
q.put("test")
q.put("woah")

while q.qsize() != 0:
    print(q.get())