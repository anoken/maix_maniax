# MAix MAniaX

<img src="https://github.com/anoken/maix_maniax/blob/master/images/001.png" width="400">

「MAix MAniaX 」のサポートページです。

# 紹介
Sipeed MaixはKendryte K210というSoCを搭載しており、小さいマイコンの中で、ディープラーニングを使った画像処理を高速に動かすことができる、今話題のデバイスです。本書は、Sipeed Maixの基礎から、深層学習モデルの作り方、Maixの最新情報、AIOTの応用事例まで、Maixを使い倒すための情報をたくさん盛り込んでいます。

あなたも本書とMaixで、AIOTの世界を体験してみませんか！？


本書は、
BOOTH<br> 
https://booth.pm/ja/items/1774794<br> 
<br> 
で取り扱っています。


# 目次

第1 章Maix の紹介

1.1 Sipeed Maix とは
1.2 Kendryte K210 とは？ 
1.3 M5StickV/UnitV とは
1.4 K210 のデバイスが続々登場
1.5 Kendryte K210の後継K510 


第2 章Maix の開発環境

2.1 Kendryte K210 の開発環境
2.2 MaixPy のファームウェアを書き込む
2.2.1 ファームウェアのダウンロード
2.2.2 kflash GUI のダウンロード
2.2.3 Kflash GUI でファームウェアを書き込む
2.3 MaixPy IDE のダウンロード
2.3.1 MaixPy IDE の使い方
2.3.2 MaixPy IDE でターミナルを起動する


第3 章MaixPy を使ってみる

3.1 カメラの画像をディスプレイに表示する
3.2 画像を保存する
3.3 画像を読み取る
3.4 動画を録画する
3.5 動画を再生する
3.6 スピーカからWAV ファイルを再生する
3.7 マルチスレッドで並列実行する
3.8 NumPy-like な行列演算ライブラリulab を使う


第4 章TensorFlow/Keras で深層学習のモデルを作る

4.1 Windows Subsystem for Linux のインストール
4.2 TensorFlow/Keras をインストール
4.3 GPU 対応TensorFlow/Keras をインストール
4.3.1 学習モデル変換ツールnncase をインストールする
4.4 MobileNet でクラス分類をする
4.4.1 MobileNet とは？ 
4.4.2 画像を用意する
4.4.3 TensorFlow/Keras でMobileNet のベースモデルを読み込む
4.4.4 TensorFlow/Keras でクラス分類のモデルを作成する
4.4.5 TensorFlow/Keras でMobileNet の学習を行う
4.4.6 Maixduino で実行する
4.4.7 クラス分類のデータセット
4.4.8 Google から画像をダウンロードしてデータセットを作る
4.5 YOLOv2 でオブジェクト検出をする
4.5.1 YOLOv2 とは？ 
4.5.2 画像とアノテーションを用意する
4.5.3 アノテーションを作成する
4.5.4 TensorFlow/Keras でYOLOv2 のモデルを読み込む
4.5.5 TensorFlow/Keras で学習を開始する
4.5.6 Maixduino で実行する
4.5.7 オブジェクト認識のデータセット


第5 章Maixduino でネットワーク通信

5.1 ネットワークと接続する
5.1.1 ESP32 へのファームウェアの書き込み
5.1.2 ESP32 ファームウェア書き込みツールのダウンロード
5.1.3 Wi-Fi 通信のアクセスポイントをスキャンする
5.1.4 Maix とUbuntu でTCP 通信する
5.1.5 Maix とUbuntu でUDP 通信する
5.1.6 Web から画像をダウンロードする
5.2 ESP32 とK210 でシリアル通信をする
5.2.1 Arduino IDE のインストール
5.2.2 arduino-esp32 のインストール
5.2.3 K210 とESP32 でUART で通信する
5.2.4 K210 とESP32 とでSPI 通信する


第6 章MaixPy でお顔を認識する

6.1 お顔を認識する
6.1.1 Maix のシリアル番号の取得
6.1.2 Sipeed の学習モデルの入手
6.1.3 Maixduino への書き込み
6.1.4 仕組み
6.2 MaixPy のカスタマイズ
6.2.1 MaixPy Configration 
6.2.2 ファームウェアのコンパイル
6.2.3 MaixPy のシステムメモリとKPU メモリを調整する


第7 章MyStickV ＋を作ってみよう

7.1 M5StickV とM5StickC でキミだけのMyStickV+ 
7.2 インターフォンを見守る「見守りアラート」
7.2.1 見守りアラート
7.2.2 見守りアラートの仕組み
7.2.3 M5StickV とUnitV の検出
7.2.4 見守りアラートの実装
7.3 あなたの動きを見守る「Cheering Watch」
7.3.1 M5StickV で加速度センサーの読み取り
7.3.2 加速度センサーの読み取り値を画像データに変換する
7.3.3 TensorFlow/Keras で加速度データでモーションの学習を
行う
7.3.4 CheeringWatch の実装
7.3.5 CheeringWatch をクラウドサービスAmbient に接続する

