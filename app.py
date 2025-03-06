import speech_recognition as sr
import arabic_reshaper
from bidi.algorithm import get_display
from tkinter import *
from tkinter import font, filedialog


root = Tk()
root.geometry("500x400")  
root.title("التعرف على الكلام")

def voiceReco():
    """التعرف على الصوت من الميكروفون وتحويله إلى نص"""
    recognizer = sr.Recognizer()
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=0.2)
        audio = recognizer.listen(mic)
        try:
            text = recognizer.recognize_google(audio, language='ar-AR')
            display_text(text)
        except sr.UnknownValueError:
            display_text("لم يتم التعرف على الصوت")
        except sr.RequestError:
            display_text("خطأ في الاتصال بخدمة التعرف على الصوت")

def fileReco():
    """رفع ملف صوتي وتحويله إلى نص"""
    file_path = filedialog.askopenfilename(filetypes=[("ملفات صوتية", "*.wav;*.mp3")])
    if not file_path:
        return
    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
            text = recognizer.recognize_google(audio, language='ar-AR')
            display_text(text)
    except sr.UnknownValueError:
        display_text("لم يتم التعرف على الصوت في الملف")
    except sr.RequestError:
        display_text("خطأ في الاتصال بخدمة التعرف على الصوت")

def display_text(text):
    """عرض النص في واجهة المستخدم"""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    textF.delete("1.0", "end")
    textF.insert(END, bidi_text)
    textF.tag_add("center", "1.0", "end")


ButtonFont = font.Font(size=15)
LabelFont = font.Font(size=12)

Label(root, text="النص سوف يظهر هنا", font=LabelFont).pack(pady=10)

textF = Text(root, height=5, width=52, font=LabelFont)
textF.tag_configure("center", justify='center')
textF.pack(pady=10)


button_frame = Frame(root)
button_frame.pack(pady=20)

Button(button_frame, text='🎤 استمع', font=ButtonFont, command=voiceReco).pack(side=LEFT, padx=10)


root.mainloop()
