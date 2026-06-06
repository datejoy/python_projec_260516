import requests
# import 名稱進來，可以不用每次都寫 requests.Response
# 但不import Response也可以用Response，只是比較麻煩要多打字
from requests import Response # , Session ← 可以一次引進多個

url:str = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

def main():
    # python 不像C#等，需要去new Class，可以直接實體化
    response:Response = requests.get(url)
    print(type(response))

    if response.status_code == 200:
        data:list = response.json()
        print("下載成功")
        print(type(data))
        print(len(data)) # len() 查串列資料的長度
        print(data[0])
        print(type(data[0])) # data:list[dict]
    else:
        print("下載失敗")
        print(response.status_code)


if __name__ == "__main__":
    main()