from llama_cpp import Llama
from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# LLMの準備
model_path="mmnga/ELYZA-japanese-Llama-2-13b-fast-instruct-gguf"
model_name="ELYZA-japanese-Llama-2-13b-fast-instruct-q4_K_M.gguf"
llm = Llama.from_pretrained(
               repo_id=model_path,
               filename=model_name,
               n_gpu_layers=41,
               n_ctx=2048,
               #tensor_split=[10,10,80],
                 )

app = FastAPI()

class AnswerRequest(BaseModel):
     sys_msg : str
     user_query:str
     user:str
     talk_log_list:list =[[]]
     log_f:bool = False
     log_len :int = 0
     max_token:int = 256
     temperature:float = 0.8
     repeat_penalty:float =  1.1
     top_k:int  = 40
     top_p:float = 0.95
     frequency_penalty:float = 0.0

@app.post("/generate/")
def  genereate(gen_request: AnswerRequest):
    sys_msg         =gen_request.sys_msg
    user_query  =gen_request.user_query
    user                  =gen_request.user
    talk_log_list=gen_request.talk_log_list
    log_f                =gen_request.log_f
    log_len           =gen_request.log_len
    max_token =gen_request.max_token
    top_k              =gen_request.top_k
    top_p              =gen_request.top_p
    get_temperature     =gen_request.temperature
    repeat_penalty         =gen_request.repeat_penalty
    frequency_penalty =gen_request.frequency_penalty
    print("top_k:",top_k,"top_p:",top_p,"get_temperature :",get_temperature ,"repeat_penalty:",repeat_penalty,"frequency_penalty:",frequency_penalty)

    talk_log_list= talk_log_list[0]
     
    #prompt = "### 指示: "+ user_query + "\n\n### 入力:" + user + "\n\n"  +  "### 応答:"
    prompt ="[INST] <<SYS>>" + user_query + "<</SYS>>" + user + "[/INST]"
    print("-------------------talk_log_list-----------------------------------------------------")
    print("talk_log_list",talk_log_list)  

    #会話ヒストリ作成。プロンプトに追加する。
    log_len = int(log_len)
    if  log_f==True and log_len >0: # 履歴がTrueでログ数がゼロでなければtalk_log_listを作成
        sys_prompt=prompt.split("### 入力:")[0]
        talk_log_list.append( " \n\n"+ "### 入力:"+ " \n" + user+ " \n" )
        new_prompt=""
        for n in range(len(talk_log_list)):
            new_prompt=new_prompt + talk_log_list[n]
 
    # 推論の実行
    print(prompt)
    output = llm(
        prompt,
        #stop=["### 入力","\n\n### 指示"],
        max_tokens=max_token,
        top_k = top_k ,
        top_p = top_p,
        temperature=get_temperature,
        repeat_penalty=repeat_penalty,
        frequency_penalty  =frequency_penalty,
        echo=True,
        )
    print(output)
    print('------------------output-------------------------------------------------')
    ans=output["choices"][0]["text"]
    ans=ans.split("[/INST]")[1]

    print(ans)
    if len(talk_log_list)>log_len:
        talk_log_list=talk_log_list[2:] #ヒストリターンが指定回数を超えたら先頭(=一番古い）の会話（入力と応答）を削除
    talk_log_list.append("\n" +"###"+  "応答:"+"\n" + ans .replace("\n" ,""))
    result=200
    return {'message':result, "out":ans,"all_out":output,"prompt":prompt,"talk_log_list":talk_log_list }
     
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
