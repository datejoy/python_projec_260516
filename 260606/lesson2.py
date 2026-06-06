# 自訂function 前面要加def
def main():
    print("這是main function的命名空間")
    m = 53
    print(n)


# 只要不在function裡面，所有地方(不管if還是for)的程式區塊中，變數皆為全域變數

if(__name__ == '__main__' ):
    n = 10
    print('我是主執行檔，主執行檔會執行程式區塊')
    print(n)
    main()


