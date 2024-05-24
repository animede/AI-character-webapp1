# AIキャラクタアプリ　Step1〜３
１）準備

　リポジトリをクローン

  git clone https://github.com/animede/AI-character-webapp1.git
 
 
　ウエイトをHugginhFaceからダウンロードし所定のホルダに移動

  https://huggingface.co/UZUKI/webapp1

  isnetis.ckpt -> AI-character-webapp1/fastapi

  ssd_best8.pth -> AI-character-webapp1/fastapi/weights



２）Webアプリ環境作成

  python3.11とgitのインストール　（必要なら）

  ターミナルを開く

  sudo apt install git

  sudo apt install -y python3.11 python3.11-venv

  環境構築(web）

  python3.11 -m venv web

  source web/bin/activate

  cd  AI-character-webapp1

  pip install -r requirements.txt
  


３）バックエンドを起動する

  ターミナルを開く

  source web/bin/activate

  cd AI-character-webapp1/fastapi

  python app.py
  


４）ストリーミングを起動

  新たにターミナルを開く

  source web/bin/activate

  cd AI-character-webapp1/streaming

  python app.py


５）フロントエンド環境構築

ターミナルを開く

python3.11 -m venv nuxt

source nuxt/bin/activate

nodeのバージョンを確認

node -v  18以上ならok、無い、または17以下だと再インストール

npm -v 

再インストール




nuxtプロジェクト作成

mpx nuxi@altest init webapp1

cd webapp1

npm i

npm run dev 確認

ファイルをコピ-


６）フロントエンド　Nuxtを起動

npm run dev 


６−１）２回目以降のフロントエンド起動

ターミナルを開く

source nuxt/bin/activate

cd webapp1

npm run dev 


ブラウザーから

http://localhost:3000

にアクセス -> FireFoxは起動してキャラは動くが問題もある

Chrome をインストール

Chrome から　http://localhost:3000　をアクセス



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




