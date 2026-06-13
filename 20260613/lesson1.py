# import requests
# import pandas as pd

# def main():
#     url = "https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json"

#     response:requests.Response = requests.get(url)

#     if response.status_code == 200:
#         data:list[dict] = response.json()
#         print(type(data))
#         print(type(data[0]))

#         # list[dict] -> DataFrame   
#         df = pd.DataFrame(data)

#         print(df.head())

#     else:
#         print("下載失敗")

# if __name__ == '__main__':
#     main()



import requests
from requests import Response
import pandas as pd
from pathlib import Path


def export_to_pdf(df: pd.DataFrame, output_path: Path) -> None:
    # 延遲匯入：只有真的要輸出 PDF 時才需要 reportlab
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet
        from reportlab.pdfbase import pdfmetrics
        from reportlab.pdfbase.cidfonts import UnicodeCIDFont
        from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle
    except ModuleNotFoundError:
        print("缺少套件 reportlab，請先安裝：pip install reportlab")
        return

    # 註冊可顯示中文的字型（macOS / Linux 常可直接使用）
    font_name = "STSong-Light"
    pdfmetrics.registerFont(UnicodeCIDFont(font_name))

    # 挑選適合放進報表的欄位，避免欄位太多導致版面混亂
    preferred_columns = ["sno", "sna", "sarea", "ar", "tot", "sbi", "bemp", "mday"]
    columns = [col for col in preferred_columns if col in df.columns]

    if not columns:
        print("找不到可輸出的欄位，無法建立 PDF。")
        return

    table_rows = df[columns].fillna("").astype(str).values.tolist()
    rows_per_page = 35

    doc = SimpleDocTemplate(
        str(output_path),
        pagesize=landscape(A4),
        rightMargin=18,
        leftMargin=18,
        topMargin=18,
        bottomMargin=18,
    )

    styles = getSampleStyleSheet()
    title_style = styles["Title"]
    title_style.fontName = font_name

    story = [
        Paragraph("YouBike 即時資料報表", title_style),
        Spacer(1, 12),
    ]

    for index in range(0, len(table_rows), rows_per_page):
        chunk = table_rows[index:index + rows_per_page]
        table_data = [columns] + chunk

        col_widths = []
        for col in columns:
            if col in ("sna", "ar"):
                col_widths.append(135)
            elif col == "mday":
                col_widths.append(120)
            else:
                col_widths.append(62)

        table = Table(table_data, repeatRows=1, colWidths=col_widths)
        table.setStyle(
            TableStyle(
                [
                    ("FONTNAME", (0, 0), (-1, -1), font_name),
                    ("FONTSIZE", (0, 0), (-1, -1), 8),
                    ("BACKGROUND", (0, 0), (-1, 0), colors.lightblue),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
                    ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ]
            )
        )

        story.append(table)

        if index + rows_per_page < len(table_rows):
            story.append(PageBreak())

    doc.build(story)
    print(f"PDF 已產生：{output_path}")

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
        output_file = Path.cwd().with_name("youbike_report.pdf")
        
        # 呼叫自訂function，此function目的為儲存檔案
        export_to_pdf(df, output_file)

    else:
        print("下載失敗")

if __name__ == '__main__':
    main()