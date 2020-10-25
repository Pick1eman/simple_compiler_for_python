string = "Slava gena214"
substring = "ava2"
string_size = 13
substring_size = 4

size = string_size - substring_size

i = 0
while i <= size:
    if string[i] == substring[0]:
        j = 1
        while j < substring_size:
            x = i + j
            if string[x] != substring[j]:
                break
            j = j + 1
        if j == substring_size:
            break
    i = i + 1

if i > size:
    i = -1

print(i)
