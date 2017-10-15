# tableau_sdk_spatial_sample

テキストファイルやDBの緯度経度情報を空間ファイルに変換せずにTableauで開く方法

# 参照

こちらのソースを改修しました
https://github.com/sarahbat/Examples-using-TableauSDK/tree/master/postgisToTde

# 前提
PythonからTableau Extract Data(tde)形式の空間ファイルを作成するには以下の環境が必要になります

- TableauSDK for python
- python 2.7

#実行環境

- Mac OS X
- Python 2.7.12 (Anaconda 4.2.0 (x86_64))
- Tableau 10.4
- TableauSDK-10300.17.0915.2101


# 実行方法

```
wget https://raw.githubusercontent.com/jpatokal/openflights/master/data/airports.dat
python all_airport.py
```