import aiohttp
from io import BytesIO
from config import COEIROINK_API_URL, KOSIRAZU_SPEAKER_UUID


async def talk(session, text, style_id):

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

    async with aiohttp.ClientSession() as session:
        async with session.post(
            COEIROINK_API_URL,
            headers={"Content-Type": "application/json"},
            json=query,
        ) as response:

            response.raise_for_status()

            audio_bytes = await response.read()

    return BytesIO(audio_bytes)
