import requests
from requests import Response
import pandas as pd
from pathlib import Path
import report as rpt    #自訂module




def main():
    # 台北市 youbike 2.0 WEB API 網址
    url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

    # 使用requests套件裡面的get()，執行後會傳出 Response 的實體
    response:Response = requests.get(url)

    # 使用 Response 中的 preperty 為 ststus_code，如果取得的數字是200則成功，反之則失敗
    if response.status_code == 200:

        # 使用 Response 實體中的json()實體方法，會傳出list的資料結構
        data:list[dict] = response.json()

        # list[dict] -> DataFrame
        # 引數名稱呼叫 ex: pd.DataFrame(data = data)
        # 引數值呼叫: 一般直接放引數
        # df為DataFrame的實體
        # 實體中有: 實體屬性、實體方法
        df:pd.DataFrame = pd.DataFrame(data)
        # Iterable 可重複讀取 (list, dict, dataframe)

        # print(df.head(10))
        # print(df.tail(10))

        # output_file = Path(__file__).with_name("youbike_report.pdf")
        # output path 為輸出的檔案的絕對路徑
        output_file = Path(__file__).with_name("youbike_report.pdf")
        
        # 呼叫自訂function，此function目的為儲存檔案
        rpt.export_to_pdf(df, output_file)

    else:
        print("下載失敗")

if __name__ == '__main__':
    main()