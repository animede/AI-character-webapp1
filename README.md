# AIキャラクタアプリ　Step1〜３
１）準備

　リポジトリをクローン
 
　ウエイトをHugginhFaceからダウンロードし所定のホルダに移動



２）Webアプリ環境作成

python3.11とgitのインストール

ターミナルを開く

sudo apt install git

sudo apt install -y python3.11 python3.11-venv

python3.11 -m venv web

source web/bin/activate

cd  AI-character-webapp1

pip install requirements.txt


バックエンドを起動する

ターミナルを開く

source web/bin/activate

cd AI-character-webapp1/fastapi

python app.py


ストリーミングを起動

新たにターミナルを開く

source web/bin/activate

cd AI-character-webapp1/streaming

python app.py



フロントエンド　Nuxtを起動

ターミナルを開く

source web/bin/activate

cd AI-character-webapp1/aituber

node .output/server/index.mjs

ブラウザーから

http://[::]:3000

にアクセス



３）LLM環境

tbd



４） VOICEVOX環境

tbd



このソフトウエアは以下のソフトウエアが含まれています。

https://github.com/SkyTNT/anime-segmentation

LLMは以下を利用します

https://github.com/abetlen/llama-cpp-python

https://huggingface.co/stabilityai/japanese-stablelm-instruct-gamma-7b

https://huggingface.co/mmnga/japanese-stablelm-base-gamma-7b-gguf

https://huggingface.co/elyza/ELYZA-japanese-Llama-2-13b-fast-instruct/commit/6016c99cee3c5aa1b734cd6be4031aad90e53ffa

https://huggingface.co/mmnga/ELYZA-japanese-Llama-2-13b-fast-instruct-gguf


VOICEVOXは以下を利用します

https://voicevox.hiroshiba.jp/

https://github.com/VOICEVOX/voicevox_core


licence

このソフトウエアは上記各ソフトウエアのライセンスを引き継ぎます。上記ソフトウエア以外の部分はMITライセンスに準じます。




