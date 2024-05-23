<template>
  <div class="container">
    <div class="m-5">
      <div class="row">
        <div class="col-9">
          <div >
            <img  src="http://0.0.0.0:5000/video_feed"  class="img-fluid border border-dark"  alt="..." >
          </div>
          <div class="d-flex justify-content-between"" style="padding-top:5px;">
            <p  v-if="char_mode=='sakura'" class="col-4" @click="Megu_Sakura('megu')" style="color:aqua;font-size:15px;">&thinsp;&thinsp;&thinsp;&thinsp;{{chr_name1}}と会話</p>
            <p v-if="char_mode=='megu'" class="col-4" @click="Megu_Sakura('sakura')" style="color:DeepPink;font-size:15px;">&thinsp;&thinsp;&thinsp;&thinsp;{{chr_name2}}と会話</p>
            <p class="col-1" @click="CharZoom('f')" style="color:red;font-size:15px;">早い</p>
            <p class="col-1" @click="CharZoom('s')" style="color:blue;font-size:15px;">遅い</p>
            <p class="col-1" @click="CharZoom('l')" style="color:red;font-size:15px;">左へ</p>
            <p class="col-1" @click="CharZoom('r')" style="color:blue;font-size:15px;">右へ</p>
            <p class="col-1" @click="CharZoom('u')" style="color:red;font-size:15px;">上へ</p>
            <p class="col-1" @click="CharZoom('d')" style="color:blue;font-size:15px;">下へ</p>
            <p class="col-1" @click="CharZoom('in')" style="color:red;font-size:15px;">拡大</p>
            <p class="col-1" @click="CharZoom('out')" style="color:blue;font-size:15px;">縮小</p>
          </div>

          <div v-if="llm_setup==false" class="d-flex flex-row" style="padding-top:0px;">
            <div class="d-flex flex-row col-11" >
              <i v-if="voiceComGet==false" class="bi bi-mic-mute" style="font-size: 23px;vertical-align:-25px; margin-right:10px;margin-top:5px;" @click="voiceComGetGo(true)"></i>
              <i v-if="voiceComGet===true & mice_status===false" class="bi bi-mic" style="font-size: 23px;vertical-align:-15px; margin-right:10px;margin-top:5px;color:green;" @click="voiceComGetGo(false)"></i>
              <i v-if="voiceComGet===true & mice_status" class="bi bi-mic-fill" style="font-size: 23px;vertical-align:-15px; margin-right:10px;margin-top:5px;color:green;" @click="voiceComGetGo(false)"></i>
              <i v-if="voiceComGet===true & func_result==='メグと会話'" class="bi bi-mic-fill" style="font-size: 23px;vertical-align:-15px; margin-right:10px;margin-top:5px;color:green;" @click="voiceComGetGo(false)"></i>
              <i v-if="voiceComGet===true & func_result==='桜と会話'" class="bi bi-mic-fill" style="font-size: 23px;vertical-align:-15px; margin-right:10px;margin-top:5px;color:green;" @click="voiceComGetGo(false)"></i>
              <input v-if="llm_setup==false" v-model="inputText" type="text" class="form-control" style="margin-left:-0px;"   @keyup.enter="Getchat" placeholder= "会話テキスト入力・・・">
              <i v-if="llm_setup==false" class="bi bi-gear-fill" style="font-size: 23px;vertical-align:-25px; margin-left:10px;margin-top:5px;color:gray;" @click="setup_llm(true,0)"></i>
            </div>
          </div>
          <div v-if="llm_setup==true" class="col-3" >
            キャラ-1
            <input v-model="chr_name1" type="text" class="form-control" style="margin-left:-0px;"   @keyup.enter="setup_llm(false,1)" placeholder= "キャラ名入力">
          </div>
            <div v-if="llm_setup==true" class="d-flex flex-row col-11" >
            <input  v-model="inputSYS1" type="text" class="form-control" style="margin-left:-0px;"   @keyup.enter="setup_llm(false,1)" placeholder= "キャラクタ定義入力・・・">
            <i class="bi bi-gear-fill" style="font-size: 23px;vertical-align:-25px; margin-left:10px;margin-top:5px;color:red;" @click="setup_llm(false,1)"></i>
          </div>
          <div v-if="llm_setup==true" class="col-3" >
            キャラ-2
            <input v-model="chr_name2" type="text" class="form-control" style="margin-left:-0px;"   @keyup.enter="setup_llm(false,2)" placeholder= "キャラ名入力">
          </div>
            <div v-if="llm_setup==true" class="d-flex flex-row col-11" >
            <input  v-model="inputSYS2" type="text" class="form-control" style="margin-left:-0px;"   @keyup.enter="setup_llm(false,2)" placeholder= "キャラクタ定義入力・・・">
            <i class="bi bi-gear-fill" style="font-size: 23px;vertical-align:-25px; margin-left:10px;margin-top:5px;color:red;" @click="setup_llm(false,2)"></i>
          </div>
        </div>

        <div class="col-3">
          <div id="app">
          <!--   キャラクタ又は背景画像アップロード -->
            <div class="upload-zone" 
                @click="clickUploadZone"
                @dragover.prevent="dragOver" 
                @drop.prevent="handleDrop"
                @dragenter.prevent="dragEnter"
                @dragleave.prevent="dragLeave"
                :class="{ 'drag-over': isDragOver }"
                >
                ドラッグ＆ドロップまたはクリックしてキャラクタ又は背景画像をアップロード
                <input type="file"  @change="handleFileChange" ref="fileInput" hidden accept="image/*">
            </div>
            <!-- ref画像下　操作部　> -->
            <div v-if="previewUrl" class="preview">
                <img :src="previewUrl" class="img-preview" alt="Image preview">
                <div class="d-flex flex-row" style="padding-top:10px;">
                  <div v-if="plaing==false" class="d-flex justify-content-center col-7">
                    <p style="margin-top:5px;">動きリピート</p> 
                    <i class="bi bi-repeat" style="font-size: 25px; vertical-align:1.2px; margin-top:0px;margin-left:10px;color: blue;"  @click="motion('repeat')"></i>
                  </div>
                  <div v-if="plaing" class="d-flex justify-content-center col-7">
                    <p style="margin-top:5px;">動きリピート停止</p> 
                    <i class="bi bi-repeat" style="font-size: 25px; vertical-align:1.2px; margin-top:0px;margin-left:10px;color: red;"  @click="motion('stop')"></i>
                  </div>
                </div>
            </div>
            <div class="d-flex justify-content-center" style="margin-top:10px;">
              <p style="color:blue;font-size:12px;">CV:VOICEBOX 四国メタン・春日部つむぎ</p>
            </div>
          </div>
        </div>
      </div>
      <div class="d-flex flex-row" style="padding-top:10px;">
        背景
        <img src="/static/ピンク枠.png" class="col-1 img-fluid" style="padding-right:5px;padding-left:5px;" />
        <img src="/static/default.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/ピンク枠大.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/default2.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/ピンク星.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/ピンク波.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/雲.png" class="col-1 img-fluid" style="padding-right:5px;" />
        <img src="/static/ブルー.png" class="col-1 img-fluid" style="padding-right:5px;" />
      </div>
      <div class="d-flex justifyr" style="margin-top:10px;font-size:12px;color:aqua;">
        {{chr_name1}}</div>
      <div class="d-flex justifyr" style="margin-top:0px;font-size:12px;">
        {{inputSYS1}}</div>
      <div class="d-flex justifyr" style="margin-top:10px;font-size:12px;color:deeppink;"> 
        {{chr_name2}}</div>
      <div class="d-flex justifyr" style="margin-top:0px;font-size:12px;">         
        {{inputSYS2}}</div>
    </div>
  </div>
</template>


<script  setup  lang="ts">
import { ref } from 'vue';
    const username = ref('test');''
    const searchText = ref('');
    const inputText = ref('');
    const sytem_answer = ref('');
    const upload_imageUrl = ref('');
    const selectedFile = ref(null);

    const file =  ref('');
    const upload_mode = ref('');
    const upload_llm = ref('image');
    const character_moving=ref('stop');
    const plaing = ref(false); 

    const previewUrl = ref(null); // プレビュー画像のURL
    const isDragOver = ref(false); // ドラッグ中のフラグ
    const fileInput = ref(null); // ファイルインプットの参照　
    const notDroped = ref(true); // ドラッグ中のフラグ

    const stream =ref(false);
    const image_mode =ref('tkh');
    const tkh_filename =ref("");

    const audioPlayer = ref(null);

    const voiceComGet = ref(false);
      const image_gen =ref("llm");
    const inputText_mode =ref("llm");
    const func_result=ref("mice_off");

    const char_mode=ref("megu");

    const zoom_val=ref("");
    const chat_wait=ref(false);

    const mice_status=ref(false);
    const pose_val=ref("Upperbody");
    const llm_setup=ref(false);
    const inputSYS1=ref("-");
    const chr_name1=ref("めぐ");
    const inputSYS2=ref("-");
    const chr_name2=ref("さくら");

    const handleFileChange = (event) => {
      const files = event.target.files;
      selectedFile.value = event.target.files[0];
      if (files.length > 0) {
        file.value = files[0];
        previewUrl.value = URL.createObjectURL(file.value); // 選択されたファイルからURLを生成してプレビュー
        notDroped.value = false; }
    };
    const handleDrop = (event) => {
      file.value = event.dataTransfer.files[0];
      if (file.value) {
        previewUrl.value = URL.createObjectURL(file.value);
        selectedFile.value=file.value;
        notDroped.value = false; }
      isDragOver.value = false;
      if (upload_llm.value=="llm"){
        image_mode.value="llm" }
      else {image_mode.value="tkh"}
      submitData(image_mode.value);
    };
    const dragOver = () => {isDragOver.value = true;};
    const dragEnter = () => {isDragOver.value = true;};
    const dragLeave = () => {isDragOver.value = false;};
    const clickUploadZone = () => {fileInput.value.click();};

    //LLMシステムプロンプト入力=キャラ定義
    const setup_llm = async (val,chr) => {
      llm_setup.value=val;
      if (llm_setup.value==true){return}
      console.log(chr)
      const formData = new FormData();
      formData.append('user_name', "test"); 
      formData.append('chr_number', chr);
      if (chr==1){
          formData.append('chr_name', chr_name1.value);
          formData.append('chr_data', inputSYS1.value)}
      else{
          formData.append('chr_name', chr_name2.value);      
          formData.append('chr_data', inputSYS2.value)}
      const response = await $fetch('http://localhost:8000/api/chr_def', {
          method: 'POST',
          body: formData,});
          if (chr==1){inputSYS1.value=response.chr_data}
          if (chr==2){inputSYS2.value=response.chr_data}
      };

    //イメージのアップロードconsole
    const submitData = async (mode) => {
      if (!selectedFile.value) return;
      const formData = new FormData();
      formData.append('file', selectedFile.value);
      formData.append('mode', mode);
      formData.append('user_name', "test");
      try {
        const blob = await $fetch('http://localhost:8000/api/upload_file', {
          method: 'POST',
          body: formData,});
        // Base64エンコードされた画像データをデコードしてオブジェクトURLを生成
        if (blob.message==200){
          const imageBlob = base64ToBlob(blob.image, 'image/png');
          upload_imageUrl.value = URL.createObjectURL(imageBlob);
          if  (blob.mode=="tkh"){
            tkh_filename.value= blob.filename}
          searchText.value= blob.filename;
          upload_mode.value=blob.mode
          character_moving.value=blob.character_moving
          //再生ボタンがstopでTKHならstreamを止める。再生中はstreamを止めない ->バックグランドが動的に変更される
          if (character_moving.value=="stop"){
            if (upload_mode.value=="tkh"){
              stream.value=false;}}
          else {stream.value=true }
        };
      } catch (error) {console.error('アップロードに失敗しました', error);}
    };

    /*    Function Key   */
    //キャラ切り替え
    const Megu_Sakura  = async (val) => {
      inputText_mode.value="llm"
      char_mode.value=val
      return
    }; 

    //キャラクタ表示ズーム
    const CharZoom = async (val) => {
      const formData = new FormData();
      formData.append('user_name', "test");    
      formData.append('mode', val);
      try {
        const response = await $fetch('http://localhost:8000/api/chara_zoom', {
          method: 'POST',
          body: formData,});
          zoom_val.value=response.zoom_val
        } catch (error) {console.error('失敗しました', error);} 
    }; 

    //キャラクタポーズズーム
    const PozeZoom = async (val) => {
      const formData = new FormData();
      formData.append('user_name', "test");    
      formData.append('mode', val);
      try {
        const response = await $fetch('http://localhost:8000/api/poze_zoom', {
          method: 'POST',
          body: formData,});
          pose_val.value=response.pose_val
        } catch (error) {console.error('失敗しました', error);} 
    }; 

    //LLMとChat  image_gen.value="gen"
    const Getchat  = async () => {
      if (image_gen.value=="gen"){
            GenImage()}
      else{
      chat_wait.value=true
      sytem_answer.value =""
      const formData = new FormData();
      formData.append('user_txt', inputText.value);
      formData.append('mode', inputText_mode.value);
      formData.append('char_mode', char_mode.value);
      formData.append('user_name', "test");
      try {
        const response = await $fetch('http://localhost:8000/api/chat', {
          method: 'POST',
          body: formData,});
          inputText.value = ""
          sytem_answer.value = response.answer_system
          Get_wav(sytem_answer.value)
          chat_wait.value=false
        } catch (error) {console.error('取得に失敗しました', error);
            chat_wait.value=false} 
      }
    };

    //wavデータ取得　現在はブラウザでは再生していない　ーー>実装予定
    const Get_wav = async (text)  => {
      const formData = new FormData();
      formData.append('user_name', "test");
      formData.append('text', text);
      formData.append('char_mode', char_mode.value);     
      // FastAPIエンドポイントからオーディオデータを取得
        const response = await fetch('http://localhost:8000/api/tts',{
          method: 'POST',
          body: formData,});
          const audioData = await response.blob();  // Blobとしてオーディオデータを取得
          const audioUrl = URL.createObjectURL(audioData);
          audioPlayer.value =  audioUrl;
          // オーディオを再生++++++ END tts +++++++
          const audio = new Audio(audioUrl);
          //audio.play().catch(error => {
          //  console.error('音声ファイルの再生に失敗しました。', error);
          //audio.play(); 
          //});
    };

    //モーションモード設定
    const motion  = async (mode) => {
      const move_type=ref("")
      if (mode=="repeat"){
        move_type.value="repeat"} 
      else{
        move_type.value="stop"
        plaing.value=false}
      character_moving.value="moving"
      stream.value=true
      plaing.value=true
      const formData = new FormData();
      formData.append('user_name', "test");
      formData.append('filename', tkh_filename.value);
      formData.append('move_type', move_type.value);
      try {
        const response = await  $fetch(`http://localhost:8000/api/tkh_move`, {
          method: 'POST',
          body: formData,});
          character_moving.value="stop";
          plaing.value=false;
      } catch (error) {console.error('画像の取得に失敗しました。', error);}
    };
     
    //voice GETボタン
    const voiceComGetGo = async (flag) => {
      voiceComGet.value = flag;
      const formData = new FormData();
      formData.append('user_name', username.value);
      formData.append('start_stop', "start");
      try {
        const response = await  $fetch(`http://localhost:8000/api/get_voice_start`, {
          method: 'POST',
          body: formData,
        });
      } catch (error) {console.error('voiceのonに失敗しました。', error);}
        // voiceComGetがtrueの場合、voice入力取得スレッドを起動
        if (voiceComGet.value) {
          voiceComGetReq(); }
    };
    
    //voice コメント取得
    const voiceComGetReq = async () => {
      if (!voiceComGet.value) return; // 終了条件
      const formData = new FormData();
      formData.append('user_name', username.value);
      try {
      const response = await  $fetch(`http://localhost:8000/api/get_voice_msg`, {
          method: 'POST',
          body: formData,});
        if (response.voice.length > 3){
            inputText.value=response.voice;
            voiceGetInst(inputText.value)
            if (func_result.value=="メグと会話"){
              image_gen.value="llm";
              stream.value=true;
              Megu_Sakura("megu");  }
            else  if (func_result.value=="桜と会話"){
              image_gen.value="llm";
              stream.value=true;
              Megu_Sakura("sakura");}
            else if (func_result.value=="リピート"){
                motion('repeat')
                voiceComGet=true
              return }
            else if (func_result.value=="停止"){
                motion('stop')
                voiceComGet=true
              return }
            else if (func_result.value=="ズームイン"){
                CharZoom('in')
                voiceComGet=true
              return }
            else if (func_result.value=="ズームアウト"){
                CharZoom('out')
                voiceComGet=true
              return }
            else if (func_result.value=="mice_on"){
                mice_status.value=true
                voiceComGetGo(true)
              return }
            else if (func_result.value=="mice_off"){
                mice_status.value=false
                voiceComGetGo(false)
              return }
            else if(image_gen.value=="llm"){
              Getchat() }
            else{
              Image2llm() }
          }
        } catch (error) {console.error('voice コメント取得に失敗しました。', error);}
      setTimeout(voiceComGetReq, 100); // 再帰的に呼び出し
    };

    function  voiceGetInst(input_text){
      // すべての文字列が含まれているかチェック
      if (["マイク", "開始"].every(substring => input_text.includes(substring))){func_result.value="mice_on"}
      else if (["マイク", "スタート"].every(substring => input_text.includes(substring))){func_result.value="mice_on"}
      else if (["マイク", "終了"].every(substring => input_text.includes(substring)) ){func_result.value="mice_off"}
      else if (["マイク", "停止"].every(substring => input_text.includes(substring))){func_result.value="mice_off"}
      else if (["マイクオフ"].every(substring => input_text.includes(substring))){func_result.value="mice_off"}
      else if (["めぐ", "会話"].every(substring => input_text.includes(substring))){func_result.value="メグと会話"}
      else if (["メグ", "会話"].every(substring => input_text.includes(substring))){func_result.value="メグと会話"}
      else if (["めぐ", "都会"].every(substring => input_text.includes(substring))){func_result.value="メグと会話"}
      else if (["メグ", "都会"].every(substring => input_text.includes(substring))){func_result.value="メグと会話"}
      else if (["桜","渡海"].every(substring => input_text.includes(substring))){func_result.value="桜と会話"}
      else if (["桜","話し"].every(substring => input_text.includes(substring))){func_result.value="桜と会話"}
      else if (["さくら","話し"].every(substring => input_text.includes(substring))){func_result.value="桜と会話"}
      else if (["さくら","会話"].every(substring => input_text.includes(substring))){func_result.value="桜と会話"}
      else if (["リピート"].every(substring => input_text.includes(substring))){func_result.value="リピート"}
      else if (["ループ停止"].every(substring => input_text.includes(substring))){func_result.value="停止"}
      else if (["ズーム","イン"].every(substring => input_text.includes(substring))){func_result.value="ズームイン"}
      else if (["ズーム","アウト"].every(substring => input_text.includes(substring))){func_result.value="ズームアウト"}     
      else{func_result.value=input_text}
      };

    // Base64文字列をBlobに変換する関数;
    function base64ToBlob(base64, mimeType) {
      const bytes = atob(base64); // Base64デコード
      let length = bytes.length;
      let out = new Uint8Array(length);
      while (length--) {
        out[length] = bytes.charCodeAt(length);}
      return new Blob([out], {type: mimeType});
    };

</script>
.value
<style scoped>
.upload-zone {
  border: 2px dashed #ccc;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}
.upload-zone_llm {
  border: 4px dashed #0000ff;
  padding: 20px;
  text-align: center;
  cursor: pointer;
}
.drag-over {
  border-color: #000;
}
.preview {
  margin-top: 20px;
}
.img-preview {
  max-width: 100%;
  height: auto;
}
.rotate {
  transform: rotate(90deg);
}

</style>
