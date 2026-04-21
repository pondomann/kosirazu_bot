import json
import requests
from io import BytesIO

def talk(text, style_id):
    
    query = {
        "speakerUuid": "a00cb8a6-a6f9-11ed-9210-0242ac1c000c",
        "styleId": style_id,
        "text": text,
        "speedScale": 1.0,
        "volumeScale": 1.0,
        "prosodyDetail": [],
        "pitchScale": 0.0,
        "intonationScale": 1.0,
        "prePhonemeLength": 0.1,
        "postPhonemeLength": 0.5,
        "outputSamplingRate": 24000,
    }

 # 音声合成を実行
    response = requests.post(
        "http://127.0.0.1:50032/v1/synthesis",
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )

    response.raise_for_status()

    # 音声をメモリ内に保存し、返す
    return BytesIO(response.content)
