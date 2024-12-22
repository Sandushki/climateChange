# Bu komut, bizim ses dosyalarımızı transkripsiyon işlemimizi yapmak adına içeri aktardığımız komuttur.
import speech_recognition as sr

# Mikrofon değerini bir değişkenin içine atamak
mic = sr.Microphone()
# Analog formatta ses kaydının kaydedildiği değer
recog = sr.Recognizer()

def recognize():
    # Bir mikrofon nesnesini alarak (mic), ve bu nesneyi kullanarak ses kaydı yapacağımız bir kod bloğu oluşturur.
    # Bu sayede, kodbloğu tamamlandığında otomatik olarak mikrofon kapanır.
    with mic as audio_file:
        #print('Lütfen konuşun...')
        # Mikrofon üzerinden alınan ilk ses kayıtlarını kullanarak ortam gürültüsünü analiz eder. 
        # Bu sayede, daha sonraki ses kayıtlarında ortam gürültüsünün etkisi azaltılı
        recog.adjust_for_ambient_noise(audio_file)
        # Analog formattan sesin dijital ortama aktarılması işidir.
        audio = recog.listen(audio_file)
        #print('Sesler yazıya çevriliyor...')

        return recog.recognize_google(audio, language='tr-TR')
