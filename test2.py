a = [1,2,3]
b = 4
c = [5, 6, 7]

for item in [b, c]:
    if type(item) == list:
        print(f"yes: {item}")
        a.extend(item)
    else:
        print(f"no: {item}")
        a.append(item)

print(a)
#print(len(a))


#a.extend(b)
#a.extend(c)
#print(a)