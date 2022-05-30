# DSAI-HW3

## 使用說明
建構虛擬環境
```
pipenv --python 3.8
```
安裝相依套件
```
pipenv install
```
進入虛擬環境
```
pipenv shell
```
運行主程式
```
python main.py
```

## 資料觀察
Consumption

根據下方折線圖，可觀察發現各筆資料的曲線趨勢類似，僅具有數值上的差異

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/consumption_data.png)

Generation

根據下方折線圖，可觀察發現各筆資料的曲線趨勢類似，僅具有數值上的差異

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/generation_data.png)

## 預處理

因 Consumption, Generation data 的 pattern 之間相似，所以我將各筆資料(同一timestamp)加總取平均，預期作為資料。

而資料又再切分為：訓練資料、驗證資料和測試資料；其比例為：0.7：0.1：0.2

下方圖片是訓練資料以 rolling window = 24 (一天) 呈現的摺線圖。

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/training_data_rolling.png)

## 模型

這次作業選用的模型是 GRU，結構如下

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/model%20summary.png)

Consumption training loss

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/consumption_training_loss.png)

Generation training loss

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/generation_training_loss.png)

## 預測結果

下方呈現的是使用測試資料與模型預測結果的圖片

Consumption

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/consumption_prediction_real.png)

Generation

![](https://github.com/eggtower/DSAI-HW3/blob/master/image/generation_prediction_real.png)
