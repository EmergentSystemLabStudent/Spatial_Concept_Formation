#Place Conecpt Formation

Place_Conecpt_Formation is a framework which lets robots to 
learn infromation(iamge features, name, region etc) of place.
It is developed by Emergent System lab in Ristumeikan University.

Main Author Satoshi Ishibushi

#準備
学習するためにはデータセットが必要であり，以下のディクトリとデータが含まれている必要がある．

1) position (dirictory)
場所領域に用いるロボットの位置情報のテキストを保存するディクトリである.

2) feature_vector (directory)
場所領域に用いる画像特徴のテキストを保存するディクトリである．

3) word (directory)
場所領域に人間から与えられた言語情報のテキストを保存するディクトリである．

4) map (directory)
データを観測した環境の地図を保存するディリクトリである.

5)Environment_parameter.txt (text)
データを取得した環境の地図情報などのパラメータを記述するテキストである.

6)space_name.txt (text)
人間が与えた言語情報の種類を記述するテキストである．




#学習

cd Spacial_Concept_Formation/python/

python python gibbs_sampling_2016_10.6.py [Input dataset] [result directory name]

exmpleデータを用いる場合は以下のコマンドで行うことができる
python python gibbs_sampling_2016_10.6.py ../training_data/example example	



