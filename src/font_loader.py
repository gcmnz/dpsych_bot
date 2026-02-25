from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.pdfmetrics import registerFontFamily

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
FONTS_DIR = BASE_DIR / ".." / "fonts"
print(FONTS_DIR)


def load_font():
    # Загрузка шрифта Times New Roman
    pdfmetrics.registerFont(TTFont('OpenSans', f'{FONTS_DIR}/opensans/OpenSans-Regular.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansBold', f'{FONTS_DIR}/opensans/OpenSans-Bold.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansItalic', f'{FONTS_DIR}/opensans/OpenSans-Italic.ttf'))
    pdfmetrics.registerFont(TTFont('OpenSansBoldItalic', f'{FONTS_DIR}/opensans/OpenSans-BoldItalic.ttf'))
    registerFontFamily(
        'OpenSans',
        normal='OpenSans',
        bold='OpenSansBold',
        italic='OpenSansItalic',
        boldItalic='OpenSansBoldItalic'
    )

    pdfmetrics.registerFont(
        TTFont('Vasek', f'{FONTS_DIR}/vasek/Vasek.ttf')
    )
    pdfmetrics.registerFontFamily(
        'Vasek',
        normal='Vasek',
    )

    pdfmetrics.registerFont(
        TTFont('Cremona', f'{FONTS_DIR}/cremona/Cremona_Sans_RUS.ttf')
    )
    pdfmetrics.registerFontFamily(
        'Cremona',
        normal='Cremona',
    )


# load_font()

print("DIR EXISTS:", FONTS_DIR.exists())
print("FILES:", list(FONTS_DIR.iterdir()))
