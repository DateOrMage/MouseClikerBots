# test gui

def test_func():
    res = 0
    for i in range(26):
        # if i > 20:
        #     return res
        if i == 25:
            yield res
            break
        if i % 5 == 0:
            yield i
        res += i


if __name__ == '__main__':
    result = test_func()
