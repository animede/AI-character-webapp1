from llama_cpp import Llama
from fastapi import FastAPI,Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

model_path="mmnga/japanese-stablelm-instruct-gamma-7b-gguf"
model_name="japanese-stablelm-instruct-gamma-7b-q4_K_M.gguf"
# LLMの準備
llm = Llama.from_pretrained(
               repo_id=model_path,
               filename=model_name,
               n_gpu_layers=35,
               n_ctx=2048
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
     temperature:float = 0.6
     repeat_penalty:float = 1.0
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

    prompt = sys_msg+"\n\n" + "### 指示: "+"\n" + user_query + "\n\n"  +  "### 入力:" +"\n"+ user + "\n\n"  +  "### 応答:"
    # 推論の実行
    output = llm(
        prompt,
        stop=["### 入力","\n\n### 指示"],
        max_tokens=max_token,
        top_k = top_k ,
        top_p = top_p,
        temperature=get_temperature,
        repeat_penalty=repeat_penalty,
        frequency_penalty  =frequency_penalty,
        echo=False,
        )
    print(output["choices"][0]["text"])
    ans = output["choices"][0]["text"]

    result=200
    return {'message':result, "out":ans,"all_out":output }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)
