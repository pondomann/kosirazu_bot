import json
import requests
from io import BytesIO
from config import KOSIRAZU_SPEAKER_UUID
from config import COEIROINK_API_URL


def talk(text, style_id):
    
    query = {
        "speakerUuid": KOSIRAZU_SPEAKER_UUID,
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
        COEIROINK_API_URL,
        headers={"Content-Type": "application/json"},
        data=json.dumps(query),
    )

    response.raise_for_status()

    # 音声をメモリ内に保存し、返す
    return BytesIO(response.content)
