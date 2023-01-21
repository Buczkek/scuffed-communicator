def szyfruj(string: str, k: int):
    result = ''
    for l in string:
        if ord(l) > 122 - k:
            result += chr(ord(l) + k - 26)
        else:
            result += chr(ord(l) + k)

    return result


print(szyfruj('abcxyz', 3))
