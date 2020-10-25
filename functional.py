def replace_(str_, old, new):
    str2 = ""
    a = 0
    for i in range(len(str_) - len(old) + 2):
        print(str(i))
        for j in range(len(old)):
            print("-- " + str(j))
            if old[j] == str_[i]:
                i += 1
                a += 1
                if a == len(old):
                    str2 += new
            else:
                a = 0
                str2 += str_[i]
                break
    return str2


def del_duplic_chars(str_, char):
    count_chars = 0
    str_output = ""
    len_str = len(str_)
    for i in range(len_str):
        if str_[i] == char:
            count_chars += 1
            if count_chars <= 1:
                str_output += char
        else:
            count_chars = 0
            str_output += str_[i]
    return str_output
