from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


def load_font():
    # Загрузка шрифта Times New Roman
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanItalic', 'timesi.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanItalicBold', 'timesbi.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanBold', 'timesbd.ttf'))