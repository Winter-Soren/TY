def incrTime():
    for frame in lru:
        lru[frame] += 1

lru = {}
hits = 0
faults = 0
frames = int(input("Enter the Number of Frames:"))
pages = [int(x) for x in input("Enter the Pages with a Space: ").split(" ")]

for page in pages:
    if page in lru.keys():
        hits += 1
        incrTime()
        lru[page] = 0
    else:
        faults += 1
        incrTime()
        if(len(lru) < frames):
            lru[page] = 0
        else:
            key = max(lru, key=lru.get)
            del(lru[key])
            lru[page] = 0
print("No of Frames: "+str(frames))
print(lru)
print("Pages: ")
print(pages)
print("Faults: "+str(faults))
print("Average Ratio of Page Faults: "+str(faults/len(pages)))
print("Hits: "+str(hits))
print("Average Ratio of Page Hits: "+str(hits/len(pages)))
