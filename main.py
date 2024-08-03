from gigachat.models import Chat, Messages, MessagesRole
from dotenv import load_dotenv
from gigachat import GigaChat
from gtts import gTTS
import threading
import tempfile
import pyaudio
import pygame
import vosk
import json
import time
import os

load_dotenv()
credentials = os.getenv("CREDENTIALS")
output_file_path = os.path.join(tempfile.gettempdir(), "recognized_text.txt")
vosk.SetLogLevel(-1)
model = vosk.Model(lang="ru")
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16,
                channels=1,
                rate=16000,
                input=True,
                frames_per_buffer=8192)


def msg(text):
    tts = gTTS(text=text, lang="ru", slow=False)
    rand = time.time()
    tts.save(os.path.join(tempfile.gettempdir(), f"{rand}_tts.mp3"))
    pygame.mixer.init()
    pygame.mixer.music.load(os.path.join(tempfile.gettempdir(), f"{rand}_tts.mp3"))
    pygame.mixer.music.play()


def main():
    with open(output_file_path, "a", encoding="utf-8") as output_file:
        print("Начало прослушивания.")
        th = threading.Thread(target=msg, args=["готов принимать ответы"])
        th.start()
        th.join()
        while True:
            data = stream.read(4096)
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                recognized_text = result['text']

                output_file.write(recognized_text + "\n")

                if "нейро" in recognized_text.lower() or "вопрос" in recognized_text.lower() or "окей" in recognized_text.lower():
                    payload = Chat(
                        messages=[
                            Messages(
                                role=MessagesRole.SYSTEM,
                                content=f"Ты ИИ бот для помощи пользователю. Ты работаешь в виде программы на ПК. "
                                        f"Текущая дата: {time.ctime(time.time())}"
                                        f"Пользователь ПК: {os.getlogin()}"
                            ),
                            Messages(
                                role=MessagesRole.USER,
                                content=recognized_text
                            )
                        ],
                        temperature=0.5,
                        max_tokens=500,
                    )

                    giga = GigaChat(credentials=credentials, verify_ssl_certs=False)
                    r = giga.chat(payload)

                    print(f"Нейро: {r.choices[0].message.content}")
                    threading.Thread(target=msg, args=[r.choices[0].message.content]).start()

                if "стоп" in recognized_text.lower() or "выход" in recognized_text.lower() or "выключить" in recognized_text.lower() or "остановка" in recognized_text.lower():
                    print("Остановка...")
                    break

        stream.stop_stream()
        stream.close()

        p.terminate()


if __name__ == '__main__':
    main()
