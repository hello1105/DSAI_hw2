# You can write code above the if-main block.
import pandas as pd
import numpy as np
import random

if __name__ == "__main__":
    import argparse

    # 處理參數
    parser = argparse.ArgumentParser()
    parser.add_argument("--training", default="training_data.csv", help="input training data file name")
    parser.add_argument("--testing", default="testing_data.csv", help="input testing data file name")
    parser.add_argument("--output", default="output.csv", help="output file name")
    args = parser.parse_args()

    # 載入資料 
    training_data = np.array(pd.read_csv(args.training, header=None))
    testing_data = np.array(pd.read_csv(args.testing, header=None))
    
    # 將出現過的漲幅，存入table
    scale = len(training_data)
    table = [0] * scale
    
    for i in range(1, len(training_data)):
        table[i-1] = (training_data[i][3] - training_data[i-1][3]) / training_data[i][3]
    
    # 根據table中的漲跌資料，隨機預測未來N天的股價，並計算最大、最小值，重複999次
    pMax = np.array([0.0] * 999)
    pMin = np.array([0.0] * 999)
    for n in range(999):
        predict_data = [0] * len(testing_data)
        predict_data[0] = testing_data[0][3]
        for i in range(1, len(predict_data)):
            predict_data[i] = predict_data[i-1] + predict_data[i-1] * table[random.randint(0, scale-1)]
            pMax[n] = np.max(predict_data)
            pMin[n] = np.min(predict_data)
    
    # 將結果上個部份的結果去掉頭尾後取平均
    pMax = np.average(np.sort(pMax)[300:700])
    pMin = np.average(np.sort(pMin)[300:700])
    
    print(pMax, pMin)
    
    # 將接近最大值的數設為賣掉的價錢，接近最小值的數設為買入的價錢
    sell_price = (pMax * 60 + pMin * 40) / 100
    buy_price =  (pMax * 40 + pMin * 60) / 100
    
    print(sell_price, buy_price)
    
    # 根據當天資料與sell_price、buy_price的比較，決定明天的action
    with open(args.output, "w") as output_file:
        state = 0
        for i in range(len(testing_data)-1):
            action = 0
            if (testing_data[i][3] < buy_price) and (state != 1):
                state += 1
                action = 1
            if (testing_data[i][3] > sell_price) and (state != -1):
                state -= 1
                action = -1
            print('%d'%action)
            output_file.write("%d\n"%action)
            
            if i > 0: sell_price += testing_data[i][3] - testing_data[i-1][3]
            if i > 0: buy_price += testing_data[i][3] - testing_data[i-1][3]
