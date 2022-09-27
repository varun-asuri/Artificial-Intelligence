import PIL, urllib.request, random, time, math, sys, io
from PIL import Image

startTime = time.time()
loc = sys.argv[2]
f = io.BytesIO(urllib.request.urlopen(loc).read()) if "http" in loc else loc
img = Image.open(f)

width, height, pix, means, colors = img.size[0], img.size[1], img.load(), [], {}
for i in range(int(sys.argv[1])):
    w, h = random.randint(0, width-1), random.randint(0, height-1)
    while pix[w, h] in means: w, h = random.randint(0, width-1), random.randint(0, height-1)
    means.append(pix[w, h])

print("Size:", width, "x", height)
print("Pixels:", width*height)
for x in range(width):
    for y in range(height):
        if pix[x, y] in colors: colors[pix[x, y]] += 1
        else: colors[pix[x, y]] = 1
mcp = max([(value, key) for key, value in colors.items()])
print("Distinct pixel count:", len(colors))
print("Most common pixel:", mcp[1], "=>", mcp[0])

oldlens, lens, groups, sums, identity, decided = [None] * len(means), [None] * len(means), [[] for i in range(len(means))], [[0, 0, 0] for i in range(len(means))], [[[] for j in range(height)] for i in range(width)], {}
while lens[0] == None or lens != oldlens:
    oldlens = [l for l in lens]
    for x in range(width):
        for y in range(height):
            if pix[x, y] not in decided: 
                distances = [math.sqrt(((k[0]-pix[x, y][0])**2)+((k[1]-pix[x, y][1])**2)+((k[2]-pix[x, y][2])**2)) for k in means]
                decided[pix[x, y]] = distances.index(min(distances))
            kmean = decided[pix[x, y]]
            groups[kmean].append(pix[x, y])
            identity[x][y] = kmean
            sums[kmean][0] += pix[x, y][0]
            sums[kmean][1] += pix[x, y][1]
            sums[kmean][2] += pix[x, y][2]
    for i in range(len(groups)):
        lens[i] = len(groups[i])
        sums[i][0] /= lens[i]
        sums[i][1] /= lens[i]
        sums[i][2] /= lens[i]
    means = sums
    groups = [[] for i in range(len(means))]
    sums = [[0, 0, 0] for i in range(len(means))]
    decided = {}

print("Final means:")
for i in range(len(means)):
    print(i+1, ":", tuple(means[i]), "=>", lens[i])
    means[i] = ( int(means[i][0]), int(means[i][1]), int(means[i][2]) )

for x in range(width):
    for y in range(height):
        r, g, b = tuple(means[identity[x][y]])
        r, g, b = int(r), int(g), int(b)
        pix[x, y] = (r, g, b)
img.save("kmeans/2021vasuri.png")

viewed, regions = set(), [0 for i in range(len(means))]
for w in range(width):
    for h in range(height):
        if (w, h) in viewed: continue
        c = means.index(pix[w, h])
        openset = [(w, h)]
        for elem in openset:
            x, y = elem
            if (x, y) in viewed: continue
            viewed.add( (x, y) )
            if x > 0 and y > 0 and pix[x-1, y-1] == pix[x, y]: openset.append( (x-1, y-1) )
            if x > 0 and pix[x-1, y] == pix[x, y]: openset.append( (x-1, y) )
            if y > 0 and pix[x, y-1] == pix[x, y]: openset.append( (x, y-1) )
            if x > 0 and y < height-1 and pix[x-1, y+1] == pix[x, y]: openset.append( (x-1, y+1) )
            if x < width-1 and y > 0 and pix[x+1, y-1] == pix[x, y]: openset.append( (x+1, y-1) )
            if x < width-1 and pix[x+1, y] == pix[x, y]: openset.append( (x+1, y) )
            if y < height-1 and pix[x, y+1] == pix[x, y]: openset.append( (x, y+1) )
            if x < width-1 and y < height-1 and pix[x+1, y+1] == pix[x, y]: openset.append( (x+1, y+1) )
        regions[c] += 1
print("Region counts:", regions)