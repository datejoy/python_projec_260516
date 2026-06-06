# 自訂function
def main():
    print("這是main function的命名空間")
    print(n)


if(__name__ == '__main__' ):
    n = 10
    print('我是主執行檔，主執行檔會執行程式區塊')
    print(n)
    main()

