if __name__ == '__main__':
    from alg import *
    from utils import *
    from getters_text import *
    from font_loader import load_font

else:
    from .alg import *
    from .utils import *
    from .getters_text import *
    from .font_loader import load_font

import io
import os
from dataclasses import dataclass

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Flowable
)

from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet, PropertySet
from reportlab.lib import colors
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT

PAGE_W = 1080  # 381 мм
PAGE_H = 1350  # 476.3 мм

MARGIN = 100
BLOCK_SPACING = 20


@dataclass
class Text:
    text: str
    style: PropertySet


class SVGFlowable(Flowable):
    def __init__(self, svg_path, width, height):
        super().__init__()
        print(svg_path)
        self.svg_path = svg_path
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        if not os.path.exists(self.svg_path):
            return

        drawing = svg2rlg(self.svg_path)

        if drawing is None:
            return

        # Масштабируем SVG под заданные размеры
        scale_x = self.width / drawing.width if self.width else 1
        scale_y = self.height / drawing.height if self.height else 1
        scale = min(scale_x, scale_y)

        # Центрирование по ширине страницы
        x_offset = (PAGE_W - drawing.width) / 2

        self.canv.saveState()
        self.canv.translate(x_offset, 0)
        self.canv.scale(scale, scale)
        renderPDF.draw(drawing, self.canv, 0, 0)
        self.canv.restoreState()

# ===============================
# CUSTOM ROUNDED BLOCK
# ===============================
class ParagraphWithBorderSVG(Flowable):
    def __init__(self, paragraph, border_color, svg_path=None, svg_width=50, svg_height=50, border_width=1, border_radius=6, padding=10):
        Flowable.__init__(self)
        self.paragraph = paragraph
        self.border_color = border_color
        self.svg_path = svg_path
        self.svg_width = svg_width
        self.svg_height = svg_height
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding

    def wrap(self, availWidth, availHeight):
        width, height = self.paragraph.wrap(availWidth - 2 * self.padding, availHeight)
        self.width = availWidth
        self.height = max(height + 2 * self.padding, self.svg_height + 2 * self.padding)
        return self.width, self.height

    def draw(self):
        self.canv.saveState()

        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(self.border_width)

        self.canv.roundRect(
            0,
            0,
            self.width,
            self.height,
            self.border_radius,
            stroke=1,
            fill=0
        )

        # Отрисовка абзаца
        p_width, p_height = self.paragraph.wrap(self.width - 2 * self.padding, self.height - 2 * self.padding)
        self.paragraph.drawOn(self.canv, self.padding, self.height - self.padding - p_height)

        # Отрисовка SVG-иконки
        if self.svg_path and os.path.exists(self.svg_path):
            try:
                drawing = svg2rlg(self.svg_path)
                if drawing is not None:
                    # Масштабируем SVG до нужных размеров
                    scale_x = self.svg_width / drawing.width
                    scale_y = self.svg_height / drawing.height
                    scale = min(scale_x, scale_y)

                    # Центрируем SVG в правой части блока
                    svg_y = (self.height - self.svg_height) / 2
                    svg_x = self.width - self.svg_width - self.padding

                    # Сохраняем текущее состояние канвы
                    self.canv.saveState()
                    # Перемещаем начало координат в нужное место
                    self.canv.translate(svg_x, svg_y)
                    # Масштабируем и отрисовываем SVG
                    self.canv.scale(scale, scale)
                    renderPDF.draw(drawing, self.canv, 0, 0)
                    # Восстанавливаем состояние канвы
                    self.canv.restoreState()
            except Exception as e:
                print(f"Error loading SVG: {e}")

        self.canv.restoreState()


class RoundedTableWithBorder(Flowable):
    def __init__(self, table, width, height, border_color=HexColor("#B39E91"), border_width=2, border_radius=5, padding=0):
        super().__init__()
        self.table = table
        self.width = width
        self.height = height
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding

    def wrap(self, availWidth, availHeight):
        return self.width, self.height

    def draw(self):
        c = self.canv
        c.saveState()

        # Рисуем закруглённую рамку
        c.setStrokeColor(self.border_color)
        c.setLineWidth(self.border_width)
        c.roundRect(0, 0, self.width, self.height, self.border_radius, stroke=1, fill=0)

        # Перемещаем канву внутрь рамки (padding)
        c.translate(self.padding, self.padding)

        # Отрисовываем таблицу
        self.table.wrapOn(c, self.width - 2 * self.padding, self.height - 2 * self.padding)
        self.table.drawOn(c, 0, 0)

        c.restoreState()


class ParagraphWithBorder(Flowable):
    def __init__(self, paragraph, border_color, border_width=1, border_radius=5, padding=10):
        Flowable.__init__(self)
        self.paragraph = paragraph
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        self.padding = padding

    def wrap(self, availWidth, availHeight):
        width, height = self.paragraph.wrap(availWidth - 2 * self.padding, availHeight)
        self.width = availWidth
        self.height = 94
        return self.width, self.height

    def draw(self):
        self.canv.saveState()
        self.canv.setFillColor(Color.TableBackground)
        self.canv.setStrokeColor(self.border_color)
        self.canv.setLineWidth(self.border_width)

        self.canv.roundRect(
            0,
            0,
            self.width,
            self.height,
            self.border_radius,
            stroke=1,
            fill=1
        )

        # Отрисовка абзаца
        p_width, p_height = self.paragraph.wrap(self.width - 2 * self.padding, self.height - 2 * self.padding)
        self.paragraph.drawOn(self.canv, self.padding, self.height - self.padding - p_height)

        self.canv.restoreState()
# ===============================
# HEADER
# ===============================


def draw_header(canvas, doc):
    canvas.saveState()

    header_height = 70
    y = PAGE_H - header_height - 100

    canvas.setFillColor(HexColor("#ECE7E4"))
    canvas.setStrokeColor(colors.white)
    canvas.setLineWidth(2)

    canvas.roundRect(
        MARGIN,
        y,
        PAGE_W - MARGIN * 2,
        header_height,
        8,
        fill=1,
        stroke=1
    )

    canvas.setFillColor(HexColor("#8A6E5B"))
    canvas.setFont("Cremona", 30)
    canvas.drawCentredString(
        PAGE_W / 2,
        y + header_height / 2 + 4,
        "институт цифровой психологии и коучинга"
    )

    canvas.setFont("Vasek", 30)
    canvas.drawCentredString(
        PAGE_W / 2,
        y + header_height / 2 - 25,
        "По методу Изиды Кадыровой"
    )

    canvas.restoreState()

# ===============================
# STYLES
# ===============================

def create_styles():
    styles = getSampleStyleSheet()

    styles.add(
        ParagraphStyle(
            name="MATRIX",
            fontName=MATRIX_FONT,
            fontSize=MATRIX_SIZE,
            leading=MATRIX_LEADING,
            textColor=MATRIX_COLOR,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="table_header",
            fontName=TABLE_HEADER_FONT,
            fontSize=TABLE_HEADER_SIZE,
            leading=TABLE_HEADER_LEADING,
            textColor=TABLE_HEADER_COLOR,
            alignment=TA_CENTER,
        )
    )
    styles.add(
        ParagraphStyle(
            name="main_table",
            fontName=TABLE_MAIN_FONT,
            fontSize=TABLE_MAIN_SIZE,
            leading=TABLE_MAIN_LEADING,
            textColor=TABLE_MAIN_COLOR,
            alignment=TA_LEFT,
            leftIndent=20
        )
    )

    styles.add(
        ParagraphStyle(
            name="header",
            fontName=HEADER_FONT,
            fontSize=HEADER_SIZE,
            leading=HEADER_LEADING,
            textColor=HEADER_COLOR,
            spaceBefore=HEADER_SPACE,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="subheader",
            fontName=SUBHEADER_FONT,
            fontSize=SUBHEADER_SIZE,
            leading=SUBHEADER_LEADING,
            textColor=SUBHEADER_COLOR,
            alignment=TA_CENTER,
        )
    )

    styles.add(
        ParagraphStyle(
            name="main",
            fontName="OpenSans",
            fontSize=MAIN_SIZE,
            leading=MAIN_LEADING,
            textColor=Color.Main,
            spaceAfter=MAIN_SPACE
        )
    )
    styles.add(
        ParagraphStyle(
            name="highlihted",
            fontName="OpenSansBold",
            fontSize=MAIN_SIZE,
            leading=MAIN_LEADING,
            textColor=Color.Highlighted,
            spaceAfter=MAIN_SPACE
        )
    )

    styles.add(
        ParagraphStyle(
            name="name",
            fontName="OpenSans",
            fontSize=NAME_SIZE,
            leading=MAIN_LEADING,
            textColor=Color.Highlighted,
            spaceAfter=MAIN_SPACE,
            leftIndent=10,
            rightIndent=200,
        )
    )

    styles.add(ParagraphStyle(
        name="StrategiyaStyle",
        fontName="Cremona",
        fontSize=36,
        alignment=TA_CENTER,
        leading=36,
        textColor=Color.Highlighted,
        leftIndent=30,
        rightIndent=30,
    ))

    styles.add(ParagraphStyle(
        name="AristotelStyle",
        fontName="Vasek",
        fontSize=50,
        alignment=TA_RIGHT,
        leading=50,
        textColor=Color.Highlighted,
    ))

    styles.add(
        ParagraphStyle(
            name="DateStyle",
            fontName="OpenSansItalic",
            fontSize=14,
            leading=14,  # line-height: 100%
            alignment=TA_RIGHT,
            textColor=HexColor(Color.Main),
        )
    )

    styles.add(
        ParagraphStyle(
            name="WhiteTitle",
            fontName="OpenSans",
            fontSize=34,
            alignment=TA_CENTER,
            textColor=colors.white
        )
    )

    styles.add(
        ParagraphStyle(
            name="WhiteSubtitle",
            fontName="OpenSans",
            fontSize=20,
            alignment=TA_CENTER,
            textColor=colors.white
        )
    )

    styles.add(ParagraphStyle(
        name="TableHeader",
        fontName="OpenSansBold",
        fontSize=22,
        alignment=TA_CENTER,
        textColor=colors.white,
        leading=30
    ))

    styles.add(ParagraphStyle(
        name="TableText",
        fontName="OpenSans",
        fontSize=22,
        leading=31,
        leftIndent=10
    ))

    return styles

# ===============================
# SIMPLE TABLE
# ===============================

def add_table(elements, header1, header2, col1, col2, styles, data=None, left_padding=20, right_padding=20):
    # Данные таблицы
    if data is None:
        data = [
            [
                Paragraph(header1, styles['table_header']),
                Paragraph(header2, styles['table_header'])
            ],
            [
                Paragraph(col1, styles['main_table']),
                Paragraph(col2, styles['main_table'])
            ]
        ]

    # Создаем таблицу
    table = Table(data, colWidths=[PAGE_W / 2 - MARGIN] * 2, hAlign='CENTER')

    # Стиль таблицы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor("#A99283")),  # цвет заголовков
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Vasek'),
        ('FONTSIZE', (0, 0), (-1, -1), 12),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, HexColor("#A99283")),
        ('BOX', (0, 0), (-1, -1), 2, Color.Table),
        # Отступы
        ('LEFTPADDING', (0, 0), (-1, -1), left_padding),  # слева 20
        ('RIGHTPADDING', (0, 0), (-1, -1), right_padding),  # справа тоже
        ('TOPPADDING', (0, 0), (-1, -1), 20),  # сверху 20
        ('BOTTOMPADDING', (0, 0), (-1, -1), 20),  # снизу 20
    ]))
    elements.append(KeepTogether([table, Spacer(1, BLOCK_SPACING)]))


# ===============================
# MAIN PDF
# ===============================

def create_pdf(name: str, date_of_birth_str: str):
    date_of_birth: datetime = datetime.strptime(date_of_birth_str, "%d.%m.%Y")

    chislo_soznaniya: int = count_date_to_digit(date_of_birth_str[:2])
    chislo_deystviya: int = count_date_to_digit(date_of_birth_str)
    name_energy_digit: int = count_name_energy_digit(name)
    vector_zhizni: int = count_vector_zhizni(chislo_deystviya)
    lichniy_god: int = count_lichniy_god(date_of_birth_str[:5])

    date_of_birth_str: str = date_of_birth.strftime('%d.%m.%Y')
    week_day_of_birth: str = week_days[date_of_birth.strftime('%A')]

    name_energy_description: str = get_name_energy_description(name_energy_digit)
    planet_by_soznanie: str = get_planet_by_soznanie(chislo_soznaniya)
    planet_pic_name: str = f"{get_planet_pic_by_soznanie(chislo_soznaniya)}.svg"
    brief_by_soznanie: str = get_brief_by_soznanie(chislo_soznaniya)
    soznanie_napravleno_by_soznanie: str = get_soznanie_napravleno_by_soznanie(chislo_soznaniya)
    ego_hochet_by_soznanie: str = get_ego_hochet_by_soznanie_by_soznanie(chislo_soznaniya)
    realizatsia_duwi_by_soznanie: str = get_realizatsia_duwi_by_soznanie_by_soznanie(chislo_soznaniya)
    princip_communicatsii_by_soznanie: str = get_princip_communicatsii_by_soznanie(chislo_soznaniya)

    positive_aspect_by_soznanie: list[str] = get_positive_aspect_by_soznanie(chislo_soznaniya)
    negative_aspect_by_soznanie: list[str] = get_negative_aspect_by_soznanie(chislo_soznaniya)

    mind_type: str = get_mind_type_by_soznanie(chislo_soznaniya)
    mind_type_desc: str = get_mind_type_desc_by_soznanie(chislo_soznaniya)

    ego_enjoys_by: list[str] = get_ego_enjoys_by_soznanie(chislo_soznaniya)
    ego_destroys_by: list[str] = get_ego_destroys_by_soznanie(chislo_soznaniya)

    triggets_list: list[str] = get_triggets_list(chislo_soznaniya)

    color_chs: str = get_color_chs_by_soznanie(chislo_soznaniya)
    color_wallet: str = get_color_wallet_by_soznanie(chislo_soznaniya)
    color_gamma_clothes: str = get_color_gamma_clothes_by_soznanie(chislo_soznaniya)
    week_day: str = get_week_day_by_soznanie(chislo_soznaniya)
    best_digit_energy: str = get_best_digit_energy_by_soznanie(chislo_soznaniya)
    good_digit_energy: str = get_good_digit_energy_by_soznanie(chislo_soznaniya)
    neutral_digit_energy: str = get_neutral_digit_energy_by_soznanie(chislo_soznaniya)
    worst_digit_energy: str = get_worst_digit_energy_by_soznanie(chislo_soznaniya)

    bolezni_by_soznanie: str = get_bolezni_by_soznanie(chislo_soznaniya)

    opisanie_by_chislo_deistviya: str = get_opisanie_by_chislo_deistviya(chislo_deystviya)

    positive_aspect_by_deistvie: list[str] = get_positive_aspect_by_deistvie(chislo_deystviya)
    negative_aspect_by_deistvie: list[str] = get_negative_aspect_by_deistvie(chislo_deystviya)

    new_chislo_deystviya: int = get_new_chislo_deystviya(chislo_deystviya)

    negative_aspect_vrozhdennogo_deystviya: str = get_negative_aspect_vrozhdennogo_deystviya(chislo_deystviya)
    positive_aspect_vrozhdennogo_deystviya: str = get_positive_aspect_vrozhdennogo_deystviya(chislo_deystviya)
    pri_vipolnenii_transformatsii: str = get_pri_vipolnenii_transformatsii(chislo_deystviya)

    napravlenie_by_vector_zhizni: str = get_napravlenie_by_vector_zhizni(vector_zhizni)
    stagnatsia_by_vector_zhizni: str = get_stagnatsia_by_vector_zhizni(vector_zhizni)
    realizatsia_by_vector_zhizni: str = get_realizatsia_by_vector_zhizni(vector_zhizni)

    nomer_zadachi_ot_tvortsa: int = get_nomer_zadachi_ot_tvortsa(chislo_soznaniya)

    create_zadacha_ot_tvortsa_func = get_create_zadacha_ot_tvortsa_func(nomer_zadachi_ot_tvortsa)
    draw_formula_zadachi_tvortsa_func = get_draw_formula_zadachi_tvortsa_func(nomer_zadachi_ot_tvortsa)

    affirmatsia: str = get_affirmatsia(nomer_zadachi_ot_tvortsa)

    energy_matrix: list[int] = get_energy_matrix(date_of_birth_str)  # [0-9] кол-во чисел

    est_energy: list[str] = get_est_energy_by_matrix(energy_matrix)  # [массив строк]
    net_energy: list[str] = get_net_energy_by_matrix(energy_matrix)  # [массив строк]

    net_energy_nums: list[int] = get_net_energy_nums_by_matrix(energy_matrix)  # [массив цифр]

    lichniy_god_description: str = get_lichniy_god_description(lichniy_god)
    lichniy_god_sub_description: str = get_lichniy_god_sub_description(lichniy_god)

    positive_aspect_by_lichny_god: str = get_positive_aspect_by_lichny_god(lichniy_god)
    negative_aspect_by_lichny_god: str = get_negative_aspect_by_lichny_god(lichniy_god)

    recomendations_na_god: str = get_recomendations_na_god(lichniy_god)

    load_font()
    styles = create_styles()

    buffer = io.BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(PAGE_W, PAGE_H),
        leftMargin=MARGIN,
        rightMargin=MARGIN,
        topMargin=200,
        bottomMargin=50
    )

    elements = []
    elements.append(
        Paragraph(
            f"Дата составления документа {datetime.now().strftime('%d.%m.%Y')}",
            styles['DateStyle']
        )
    )

    elements.append(
        Paragraph(
            "«Познание начинается с удивления»",
            styles['AristotelStyle']
        )
    )
    elements.append(
        Paragraph(
            "Аристотель",
            styles['AristotelStyle']
        )
    )
    elements.append(Spacer(0, 40))
    elements.append(
        Paragraph(
            "Цифровая психология - стратегия счастливой жизни.",
            styles['StrategiyaStyle']
        )
    )
    elements.append(Spacer(0, 50))

    name_p = Paragraph(
        f"""<font name="OpenSansBold" size="{NAME_SIZE}" color="{Color.Highlighted}">
                            {name}
                        </font>
                        <font name="OpenSans" size="{NAME_SIZE}" color="{Color.Main}">
                            (дата рождения {date_of_birth_str} - {week_day_of_birth}) {chislo_soznaniya} / {chislo_deystviya}
                        </font>
                        <br/><br/>  <!-- Перенос строки -->
                        <font name="OpenSansBold" size="{NAME_SIZE}" color="{Color.Highlighted}">Энергия имени {name}</font>
                        <font name="OpenSans" size="{NAME_SIZE}" color="{Color.Main}">- {name_energy_digit} {name_energy_description}</font>""",
        styles['name']
    )

    elements.append(
        ParagraphWithBorderSVG(
            paragraph=name_p,
            border_color=HexColor(Color.Highlighted),
            svg_path=f"icons/{planet_pic_name}",
            svg_width=100,
            svg_height=100,
            border_width=2,
            border_radius=6,
            padding=20
        )
    )

    chislo_soznaniya_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                Ваше число сознания - {chislo_soznaniya}
                            </font>
                            <br></br>
                            <font name="{SUBHEADER_FONT}" size="{SUBHEADER_SIZE}" color="{SUBHEADER_COLOR}">
                                (Положительные и отрицательные аспекты программы ума)
                            </font>""",
        styles['header']
    )
    elements.append(Spacer(0, 30))
    elements.append(
        ParagraphWithBorder(
            chislo_soznaniya_p,
            Color.TableBackground,
        )
    )

    pl_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Планета</font>"""
    planeta = f"""{pl_text}
           <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}> – {planet_by_soznanie}</font>
       """

    brief_description_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Краткое описание личности по дате рождения:</font>"""
    brief_description = f"""{brief_description_text}<br/>
        <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>
            {name}, {brief_by_soznanie}</font>
        """

    vector_sozn_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Сознание направлено на </font>"""
    vector_sozn = f"""{vector_sozn_text}
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {soznanie_napravleno_by_soznanie}</font>
        """

    ego_hochet_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Ваше эго хочет: </font>"""
    ego_hochet = f"""{ego_hochet_text}
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {ego_hochet_by_soznanie}</font>
        """

    realizatsia_duwi_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Реализация души </font>"""
    realizatsia_duwi = f"""{realizatsia_duwi_text}
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {realizatsia_duwi_by_soznanie}</font>
        """
    princip_communicatsii_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Принцип коммуникации: </font>"""
    princip_communicatsii = f"""{princip_communicatsii_text}
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {princip_communicatsii_by_soznanie}</font>
        """

    create_text(elements, alignment=0, space_after=0, space_before=20, text=planeta)
    create_text(elements, alignment=0, space_after=0, space_before=20, text=brief_description)
    create_text(elements, alignment=0, space_after=0, space_before=20, text=vector_sozn)
    create_text(elements, alignment=0, space_after=0, space_before=20, text=ego_hochet)
    create_text(elements, alignment=0, space_after=0, space_before=20, text=realizatsia_duwi)
    create_text(elements, alignment=0, space_after=20, space_before=20, text=princip_communicatsii)

    positive_text: str = format_list(positive_aspect_by_soznanie)
    negative_text: str = format_list(negative_aspect_by_soznanie)
    add_table(elements, "В позитивном аспекте (+)", "В негативном аспекте (-)", positive_text, negative_text, styles, left_padding=10, right_padding=10)

    tip_mishlenia_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Тип мышления - </font>"""
    tip_mishlenia = f"""{tip_mishlenia_text}
            <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}> {mind_type}</font>
        """
    mishlenie_desk = f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{mind_type_desc}</font>"""

    create_text(elements, alignment=0, space_after=0, space_before=15, text=tip_mishlenia)
    create_text(elements, alignment=0, space_after=20, space_before=5, text=mishlenie_desk)

    ego_enjoys_by_text: str = format_list(ego_enjoys_by)
    ego_destroys_by_text: str = format_list(ego_destroys_by)
    add_table(elements, "Эго наслаждается", "Эго разрушается", ego_enjoys_by_text, ego_destroys_by_text, styles)

    create_text(elements, alignment=0, space_after=0, space_before=10,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Триггеры (ситуации, вызывающие негативные эмоции):</font>""")
    triggers_text: str = format_triggers_list(triggets_list)
    create_text(elements, alignment=0, space_before=15, space_after=45, left_indent=10, leading=22, text=triggers_text)

    styles.add(ParagraphStyle(
        name='Table',
        fontSize=16,
        leading=18,
        fontName="OpenSans",
        textColor=HexColor("#232323"),
        alignment=TA_CENTER,
        wordWrap='CJK'
    ))
    styles.add(ParagraphStyle(
        name='TopTable',
        fontSize=16,
        leading=18,
        fontName="OpenSans",
        textColor=Color.TableText,
        alignment=TA_CENTER,
        wordWrap='CJK'
    ))

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold">Цвет<br/>Вашего<br/>ЧС</font>', styles['TopTable']),
         Paragraph(f'<font name="OpenSansBold">Цвет<br/>аксессуаров<br/>(кошелёк)</font>', styles['TopTable']),
         Paragraph(f'<font name="OpenSansBold">Цветовая<br/>гамма<br/>одежды</font>', styles['TopTable']),
         Paragraph(f'<font name="OpenSansBold">Ваш<br/>день<br/>недели</font>', styles['TopTable']),
         Paragraph(f'<font name="OpenSansBold">Энергии цифр</font>', styles['TopTable'], )],
        [
            "", "", "", "",
            Paragraph(f'<font name="OpenSans">Лучшая</font>', styles['TopTable']),
            Paragraph(f'<font name="OpenSans">Хорошая</font>', styles['TopTable']),
            Paragraph(f'<font name="OpenSans">Нейтральная</font>', styles['TopTable']),
            Paragraph(f'<font name="OpenSans">Отрицательная</font>', styles['TopTable']),
        ],
        [Paragraph(color_chs, styles['Table']),
         Paragraph(color_wallet, styles['Table']),
         Paragraph(color_gamma_clothes, styles['Table']),
         Paragraph(week_day, styles['Table']),
         Paragraph(best_digit_energy, styles['Table']),
         Paragraph(good_digit_energy, styles['Table']),
         Paragraph(neutral_digit_energy, styles['Table']),
         Paragraph(worst_digit_energy, styles['Table'])]
    ]

    # Создаем таблицу с 8 колонками
    side_padding = 20  # сколько хочешь отступ

    table_width = doc.width - side_padding * 2
    table = Table(
        data,
        colWidths=[
            table_width * 0.145,
            table_width * 0.145,
            table_width * 0.145,
            table_width * 0.145,
            table_width * 0.11,
            table_width * 0.11,
            table_width * 0.11,
            table_width * 0.12
        ],
        rowHeights=[60, 60, 100]
    )

    # Настраиваем стиль таблицы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (7, 0), Color.TableBackground),
        ('BACKGROUND', (0, 1), (7, 1), Color.TableBackground),
        ('BACKGROUND', (0, 0), (3, 1), Color.TableBackground),
        ('GRID', (0, 0), (-1, -1), 1, Color.Table),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, 0), 15),  # верхняя строка
        ('BOTTOMPADDING', (0, 1), (-1, 1), 15),  # нижняя строка
        ('TOPPADDING', (0, 1), (-1, 1), 0),  # убрать лишний padding
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное выравнивание по центру
        ('SPAN', (4, 0), (7, 0)),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (2, 0), (2, 1)),
        ('SPAN', (3, 0), (3, 1))
    ]))

    elements.append(KeepTogether([
        table,
    ]))

    bolezni_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Болезни: </font>"""
    bolezni = f"""{bolezni_text}
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {bolezni_by_soznanie}</font>
        """
    create_text(elements, alignment=0, space_after=10, space_before=12, text=bolezni)

    chislo_deystviya_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                    Ваше Число действия (жизненный путь) - {chislo_deystviya}
                                </font>""",
        styles['header']
    )
    elements.append(Spacer(0, 20))
    elements.append(
        ParagraphWithBorder(
            chislo_deystviya_p,
            Color.TableBackground,
            padding=20
        )
    )

    opisanie_chislo_deistviya_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Краткое описание по Числу действия: </font>"""
    opisanie_chislo_deistviya = f"""{opisanie_chislo_deistviya_text}<br/>
            <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{opisanie_by_chislo_deistviya}</font>
        """

    create_text(elements, alignment=0, space_after=25, space_before=20, leading=36, text=opisanie_chislo_deistviya)

    # Формируем содержимое ячеек
    positive_text: str = format_list(positive_aspect_by_deistvie)
    negative_text: str = format_list(negative_aspect_by_deistvie)
    add_table(elements, "В позитивном аспекте (+)", "В негативном аспекте (-)", positive_text, negative_text, styles)

    create_text(elements, alignment=0, space_before=10, space_after=20,
                text=f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}> При выполнении Задачи по трансформации сознания, Ваше Число действия (жизненного пути) изменится 
                с {chislo_deystviya} на {new_chislo_deystviya}. При этом у Вас откроются неограниченные возможности.</font>""")

    col1_flowables = [
        Paragraph("В негативном аспекте (-):", styles['highlihted']),
        Paragraph(negative_aspect_vrozhdennogo_deystviya, styles['main']),
        Spacer(1, 12),
        Paragraph("В позитивном аспекте (+):", styles['highlihted']),
        Paragraph(positive_aspect_vrozhdennogo_deystviya, styles['main'])
    ]

    col2_flowables = [
        Paragraph("При выполнении Задачи по трансформации сознания:", styles['highlihted']),
        Paragraph(pri_vipolnenii_transformatsii, styles['main'])
    ]

    add_table(
        elements,
        header1=f"Врожденные действия - {chislo_deystviya}",
        header2=f"Измененные действия - {new_chislo_deystviya}",
        col1=col1_flowables,
        col2=col2_flowables,
        styles=styles,
        data=[
            [
                Paragraph(f"Врожденные действия - {chislo_deystviya}", styles['table_header']),
                Paragraph(f"Измененные действия - {new_chislo_deystviya}", styles['table_header'])
            ],
            [
                col1_flowables,
                col2_flowables
            ]
        ],
    )

    vector_zhizni_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                Ваш вектор жизни - {vector_zhizni}
                            </font>
                            <br></br>
                            <font name="{SUBHEADER_FONT}" size="{SUBHEADER_SIZE}" color="{SUBHEADER_COLOR}">
                                (Сфера - предназначения)
                            </font>""",
        styles['header']
    )
    elements.append(Spacer(0, 30))
    elements.append(
        ParagraphWithBorder(
            vector_zhizni_p,
            Color.TableBackground,
        )
    )
    create_text(elements, alignment=0, space_before=15, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">(Вектор жизни - показатель направленности в жизни, т.е. совокупность энергий, через
        которые человек приходит либо к стагнации и разрушению, либо к самореализации в жизни.
        Самореализация — процесс, который заключается в реализации человеком своих
        способностей, потенциалов и талантов, в каком-либо виде деятельности)</font>""")
    create_text(elements, alignment=0, space_before=10, space_after=20, text=f"""
            <font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">
            Ваш вектор жизни направлен на
            </font>
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">
            {napravlenie_by_vector_zhizni}
            </font>""")

    add_table(elements, "Стагнация (отсутствие развития)", "Реализация (развитие потенциала)", stagnatsia_by_vector_zhizni, realizatsia_by_vector_zhizni, styles, left_padding=10, right_padding=10)

    zadacha_ot_tvortsa_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                    Ваша Задача по трансформации сознания - {nomer_zadachi_ot_tvortsa}
                                </font>
                                <br></br>
                                <font name="{SUBHEADER_FONT}" size="{SUBHEADER_SIZE}" color="{SUBHEADER_COLOR}">
                                    (Задача от Творца)
                                </font>""",
        styles['header']
    )
    elements.append(Spacer(0, 30))
    elements.append(
        ParagraphWithBorder(
            zadacha_ot_tvortsa_p,
            Color.TableBackground,
            padding=2
        )
    )
    elements.append(Spacer(0, 10))
    create_zadacha_ot_tvortsa_func(elements)

    create_text(elements, alignment=1, space_before=30, space_after=20, text=f"""<font name="Cremona" size="28"
    color="{Color.Highlighted}">Формула задачи (стратегия счастливой жизни)</font>""")
    draw_formula_zadachi_tvortsa_func(elements)

    create_text(elements, alignment=0, space_before=30, space_after=40, text=f"""
        <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Аффирмация</font>
        <font name="OpenSans" size="{MAIN_SIZE}"> (утверждение, помогающее создать положительный психологический
        настрой. Многократное повторение воздействует на подсознание и помогает создать новую
        модель мышления) </font>
        <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>- {affirmatsia}</font>
        """)

    matrix_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                        Ваша матрица врождённых энергий
                                    </font>
                                    <br></br>
                                    <font name="{SUBHEADER_FONT}" size="{SUBHEADER_SIZE}" color="{SUBHEADER_COLOR}">
                                        (врожденные качества и компетенции личности)
                                    </font>""",
        styles['header']
    )
    elements.append(
        ParagraphWithBorder(
            matrix_p,
            Color.TableBackground,
            padding=8
        )
    )

    elements.append(Spacer(1, 30))

    data = [
        ['3' * energy_matrix[2], '6' * energy_matrix[5], '9' * energy_matrix[8]],
        ['2' * energy_matrix[1], '5' * energy_matrix[4], '8' * energy_matrix[7]],
        ['1' * energy_matrix[0], '4' * energy_matrix[3], '7' * energy_matrix[6]]
    ]

    for r in range(3):
        for c in range(3):
            data[r][c] = Paragraph(
                f'<font name="{MATRIX_FONT}" size="{MATRIX_SIZE}" color="{MATRIX_COLOR}">{data[r][c]}</font>',
                styles['MATRIX']
            )

    # Размер ячеек = 260 / 3
    cell_size = 260 / 3

    table = Table(
        data,
        colWidths=[cell_size] * 3,
        rowHeights=[cell_size] * 3,
    )

    table.setStyle(TableStyle([
        ('INNERGRID', (0, 0), (-1, -1), 1.5, Color.Highlighted),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
    ]))
    rounded = RoundedMatrix(table, size=260)
    rounded.hAlign = 'CENTER'
    elements.append(
        KeepTogether([
            rounded
        ])
    )

    create_text(elements, alignment=0, space_before=20, space_after=20,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>В Вашей матрице заложены следующие энергии:</font>""")
    create_matrix_energy(elements, est_energy)

    create_text(elements, alignment=0, space_after=20, space_before=20,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>В Вашей матрице отсутствуют следующие энергии:</font>""")
    create_matrix_energy(elements, net_energy)

    create_text(elements, alignment=0, space_after=20, space_before=20,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Рекомендации по наработке отсутствующих энергий:</font>""")

    create_recomendations(elements, [
        "Стремитесь к выполнению Задачи по трансформации сознания! (Задача от Творца)",
        "Следите за чистотой питания (исключите вещества, изменяющие сознания)",
        "Соблюдайте режим дня (ранние подъёмы и отходы ко сну)",
        "Займитесь йогой",
        "Энерготерапия (регулярное прохождение энергомедитаций и энергосеансов)",
        "Занимайтесь медитативными практиками",
        "В течение дня пейте теплую воду, до 45 градусов С (на 30 кг – 1 литр воды)",
        "Ежедневно ходите от 6 км. и больше со скоростью 5 км/час и выше"
    ])
    elements.append(Spacer(1, 20))

    for competencie_num in net_energy_nums:
        create_build_competencies(elements, competencie_num)

    elements.append(Spacer(1, 10))

    chislo_deystviya_p = Paragraph(
        f"""<font name="{HEADER_FONT}" size="{HEADER_SIZE}" color="{HEADER_COLOR}">
                                        Ваш личный год {datetime.now().year} г. - {lichniy_god}
                                    </font>""",
        styles['header']
    )
    elements.append(Spacer(0, 20))
    elements.append(
        ParagraphWithBorder(
            chislo_deystviya_p,
            Color.TableBackground,
            padding=20
        )
    )
    text = f"""
    <font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">{lichniy_god_description}</font><br/>
    """
    if lichniy_god_sub_description is not None:
        text += f"""
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">{lichniy_god_sub_description}</font>
        """

    create_text(elements, alignment=0, space_after=20, space_before=20, text=text)

    # Формируем содержимое ячеек
    positive_text = f"""<font name="OpenSans" size="{MAIN_SIZE}">{positive_aspect_by_lichny_god}</font>"""
    negative_text = f"""<font name="OpenSans" size="{MAIN_SIZE}">{negative_aspect_by_lichny_god}</font>"""
    add_table(elements, "В позитивном аспекте (+)", "В негативном аспекте (-)", positive_text, negative_text, styles, left_padding=10, right_padding=10)

    text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Рекомендации на этот год:</font>
       <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{recomendations_na_god}</font>"""
    create_text(elements, alignment=0, space_before=5, space_after=15, text=text)

    text = f"""<font name="Cremona" size="{HEADER_SIZE}" color={Color.Highlighted}>{name}, я от всей души желаю Вам успеха!</font>"""
    create_text(elements, alignment=1, space_after=40, space_before=140, leading=46, left_indent=200, right_indent=200, text=text)

    s = SVGFlowable(f"icons/{planet_pic_name}", 120, 120)
    elements.append(s)

    doc.build(elements, onFirstPage=draw_header, onLaterPages=draw_header)

    buffer.seek(0)
    return buffer.read()


load_font()

if __name__ == '__main__':
    name, date = 'Natasha', '05.10.1995'
    pdf = create_pdf(name, date)

    with open(f'{name}_{date}.pdf', 'wb') as f:
        f.write(pdf)
