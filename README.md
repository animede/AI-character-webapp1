# AIキャラクタアプリ　Step1〜３
１）準備

　リポジトリをクローン
　git clone https://github.com/animede/AI-character-webapp1.git

　ウエイトをHugginhFaceからダウンロードし所定のホルダに移動
 
　https://huggingface.co/UZUKI/webapp1

　isnetis.ckpt -> AI-character-webapp1/fastapi
 
　ssd_best8.pth -> AI-character-webapp1/fastapi/weights
 
　libcudart.so.11.0　はVOICEVOXでエラーのとき使用

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

　node -v  　　18以上ならok、無い、または17以下だと再インストール

　npm -v 
 

　インストール
 
　sudo apt-get install -y nodejs
 
　sudo apt install npm
 

　再インストール
 
　sudo npm cache clean
 
　sudo npm install -g n
 
　sudo n stable
 
 
　削除
 
　sudo apt purge --autoremove nodejs npm
 
　sudo apt install nodejs npm
 
　sudo npm install n -g
 



　nuxtプロジェクト作成

　mpx nuxi@altest init webapp1

　cd webapp1

　npm i

　npm i bootstrap-icons-vue bootstrap
 
　npm i bootstrap-icons

　npm run dev 確認
 

　ファイルをコピ-　AI-character-webapp1/aituber　から　webapp1

　package.json

　nuxt.config.ts

　app.vue
 
　static　ホルダー

６）フロントエンド　Nuxtを起動

　npm run dev 


６−１）２回目以降のフロントエンド起動

　ターミナルを開く

　source nuxt/bin/activate

　cd webapp1

　npm run dev 


　ブラウザーからアクセスして起動

　http://localhost:3000

　ー> FireFoxは起動してキャラは動くが問題もある

　Chrome をインストール

　Chrome から　http://localhost:3000　をアクセス



３）LLM環境

　llama-cpp-python

　mkdir -p ~/miniconda3
 
　wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
 
　bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
 
　rm -rf ~/miniconda3/miniconda.sh

　環境構築
 
　conda create -n llm
 
　conda activate llm

 
　GPUで動かす

　CMAKE_ARGS="-DLLAMA_CUDA=on"

　pip install llama-cpp-python --upgrade --force-reinstall --no-cache-dir
 



４） VOICEVOX環境

　python3 -m venv  vb

　source vb/bin/activate

　cd vb

　git clone https://github.com/VOICEVOX/voicevox_core.git

　pip install -r requirements.txt

　binary=download-linux-x64
 
　curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary} -o download

　　　sudo snap install curl   　　***上記でエラー、 必要ならば

　chmod +x download

　./download --device cuda

　pip install https://github.com/VOICEVOX/voicevox_core/releases/download/0.14.4/voicevox_core-0.14.4+cpu-cp38-abi3-linux_x86_64.whl

　binary=download-linux-x64

　curl -sSfL https://github.com/VOICEVOX/voicevox_core/releases/latest/download/${binary} -o download

　chmod +x download

　./download -o ./example/python

　cd voicevox_core

　python vox_api_server.py

　-> error: libcudart.so.11.0: cannot open shared object file: No such file or directory

　libcudart.so.11.0をHuggingFace UZUKI/webapp1 からvoicevox_coreへコピー

　python vox_api_server.py



  　




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




