def grep(pattern):
    print("Looking for ", pattern)
    while True:
        line = (yield) # wait for a message
        if pattern in line:
            print(line)

g = grep("juice") # create the grep coroutine
next(g) # start the grep coroutine
g.send("rum, water, sugar, lime juice")
g.send("better something alcoholic")
g.send("How to cook with verjuice?")
g.close()