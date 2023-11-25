def get_bin_salt(seed, mail):
    seed = seed #110
    a = mail

    bin_ = '{0:016b}'.format(seed)

    salted = ""
    for i,j in enumerate(a[:-1]):
        if(bin_[i] == "1"):
            salted += str(j+".")
        else:
            salted += j

    salted += str(a[-1]) #last digit of mail
    return salted

#print(get_bin_salt(3,"meowkingkitten314"))