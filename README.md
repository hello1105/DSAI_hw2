# DSAI_hw2

<br />

## 一、I

1. 我覺得一支股票的漲跌應該有某種趨勢，因此漲跌的出現次數與數值，也會以某種特定的機率出現，所以我統計每日close的漲、跌幅比例，並以testing data第一天的資料為基準，隨機產生之後N天的資料。<br /><br />
2. 我認為training data與testing data若存在相同的趨勢，以這個方法得到資料最大值與最小值，應該會接近實際的情況，未來N天的股價會在這個範圍內浮動，為了避免極端值得出現，我將這個過程重複999次，並去除頭尾後取平均。<br /><br />
3. 得到了預測的最大、最小值，便開始決定action，若當天的股價接近最大值就進行出售，若接近最小值則買入，我將賣出、買入價格設定為最接近最大、最小值的40%（ex: max=160, min=150，若股價為156以上就賣出，154以下就買入）。<br /><br />
4. 在讀入下一天的資料前，我先計算今日的漲跌，並根據這個數值調整賣出、買入的價錢（若股票漲了10塊，預測的最大、最小值都要跟著上升10塊）。<br /><br />
5. 重複3、4步驟直到全部完成。<br /><br />

<br />

## 二、執行方法

進入資料夾後執行python trader.py --training "Training Data" --testing "Testing Data" --output output.csv

