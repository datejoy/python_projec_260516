# numpy
- 傳出ndArray(外部資料結構)

## ndArray
- 不用for in
- 無欄/列名稱 (數值的表格)
- 機器/深度學習 都是放ndArray


# pandas

## DataFrame (多筆資料)
- 將ndArray包起來，寫給人類看的
- 有欄位/列的名稱

### 選取列的方法
- iloc[n]           依位置選取第n列
- iloc[a:b] 切割    依位置選取a~b-1列
- loc[a:b]         依index標籤取
- loc[a:b]          依index標籤取(含b)

### 更多選取方法
- query()   
- loc[] + 條件 
- nlargest()
- nsmallest()
- between()
- isin()
- str.contains()

*後方全部用名稱呼叫
**沒限定數量的位置呼叫

## Series (單筆資料)
- 沒有欄位名，只有索引值
- 兩個series即組成DataFrame

# stack 堆疊資料
- 長資料

# unstack 不堆疊資料
- 寬資料