import io

from reportlab.platypus import SimpleDocTemplate, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER, TA_LEFT

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


MAIN_SIZE = 22
HIGHLIGHTED_SIZE = 22
BIG_SIZE = 34

PAGE_W = 1000
PAGE_H = 1300

# Стиль для шапки
header_style = ParagraphStyle(
    name='HeaderStyle',
    fontName='OpenSansBold',
    fontSize=BIG_SIZE,
    alignment=1,
    textColor=Color.Highlighted,
    leading=BIG_SIZE + 4
)

# Текст шапки
header_text = "институт цифровой психологии и коучинга"
subheader_text = "По методу Изиды Кадыровой"

subheader_style = ParagraphStyle(
    name='SubHeaderStyle',
    fontName='Vasek',
    fontSize=BIG_SIZE - 6,
    leading=(BIG_SIZE - 6) + 2,
    alignment=1,
    textColor=Color.Highlighted
)


def header_canvas(canvas, doc):
    canvas.saveState()

    usable_width = doc.width  # ширина между полями

    vertical_padding = 12   # отступ сверху и снизу внутри синего блока
    gap_between = 6         # расстояние между заголовком и подзаголовком

    # ===== Параграфы =====
    header_para = Paragraph(header_text, header_style)
    subheader_para = Paragraph(subheader_text, subheader_style)

    header_w, header_h = header_para.wrap(usable_width, 200)
    sub_w, sub_h = subheader_para.wrap(usable_width, 200)

    total_text_height = header_h + gap_between + sub_h

    # ===== Позиция блока =====
    block_height = total_text_height + vertical_padding * 2
    # print(block_height, doc.height, doc.bottomMargin)
    block_y = PAGE_H - block_height - 80

    # 🔵 Рисуем фон строго по границам документа
    canvas.setFillColor("#ECE7E4")  # твой синий
    canvas.rect(
        doc.leftMargin,
        block_y,
        usable_width,
        block_height,
        stroke=0,
        fill=1
    )

    # ===== Рисуем текст =====
    current_y = block_y + block_height - vertical_padding - header_h
    header_para.drawOn(canvas, doc.leftMargin + (usable_width - header_w) / 2, current_y)
    current_y -= (gap_between + sub_h)
    subheader_para.drawOn(canvas, doc.leftMargin + (usable_width - sub_w) / 2, current_y)

    canvas.restoreState()


def get_header_height(doc):
    usable_width = doc.width

    vertical_padding = 12
    gap_between = 6

    header_para = Paragraph(header_text, header_style)
    subheader_para = Paragraph(subheader_text, subheader_style)

    _, header_h = header_para.wrap(usable_width, 200)
    _, sub_h = subheader_para.wrap(usable_width, 200)

    total_text_height = header_h + gap_between + sub_h
    return total_text_height + vertical_padding * 2


def create_pdf(name: str, date_of_birth_str: str) -> tuple[bytes, str]:
    pdf_buffer = io.BytesIO()

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

    elements: list[Flowable] = []

    # Стили текста
    styles = getSampleStyleSheet()

    doc = SimpleDocTemplate(pdf_buffer, pagesize=(PAGE_W, PAGE_H), leftMargin=80, rightMargin=80, topMargin=130, bottomMargin=20)
    header_height = get_header_height(doc)
    doc.topMargin = header_height + 120  # + небольшой дополнительный отступ
    frame = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,  # Вычитаем пространство шапки

        id='normal'
    )
    # PageTemplate с нашей функцией header
    template = PageTemplate(id='with_header', frames=frame, onPage=header_canvas)
    doc.addPageTemplates([template])

    styles.add(ParagraphStyle(
        name='OpenSansCenter',
        fontName='OpenSans',
        fontSize=MAIN_SIZE,
        alignment=TA_CENTER,
        leading=40  # Межстрочный интервал
    ))

    styles.add(ParagraphStyle(
        name='OpenSansNormal',
        fontName='OpenSans',
        fontSize=22,
        leading=30  # Увеличенный межстрочный интервал
    ))
    styles.add(ParagraphStyle(
        name='Table',
        fontName='OpenSans',
        alignment=1,
        leading=20,
        splitLongWords=0,   # ← ВАЖНО
        wordWrap='CJK'      # помогает корректнее переносить
    ))

    create_text(elements, alignment=2, space_after=10, space_before=150,
                text=f'<font name="OpenSansItalic" size="12" color={Color.Main}>Дата составления документа {datetime.now().strftime('%d.%m.%Y')}</font>'
                )

    create_text(elements, alignment=2, space_after=5, leading=32, text=f"""
                    <font name="Vasek" size="{42}" color={Color.Highlighted}>«Познание начинается с удивления»</font>
                """)

    create_text(elements, alignment=2, space_after=75, leading=32, text=f"""
        <font name="Vasek" size="{42}" color={Color.Highlighted}>Аристотель</font>
    """)

    create_text(elements, alignment=1, left_indent=30, space_after=38, leading=32, text=f"""
        <font name="OpenSans" size="{BIG_SIZE}" color={Color.Highlighted}>Цифровая психология - стратегия счастливой жизни.</font>
    """)

    create_text(elements, left_indent=35, alignment=0, space_after=30, text=f"""
        <font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color="{Color.Highlighted}">{name} </font>
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">(дата рождения {date_of_birth_str} - {week_day_of_birth}) {chislo_soznaniya} / {chislo_deystviya}</font>"
    """)

    create_text(elements, left_indent=35, alignment=0, space_after=40, leading=32, text=f"""
        <font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Энергия имени {name.upper()}</font>
        <font name="OpenSans" size="{HIGHLIGHTED_SIZE}" color={Color.Black}> - {name_energy_digit} {name_energy_description}</font>
    """)

    create_orange_rect(elements, doc.width, 110, f"""
    <font name="OpenSans" size="{BIG_SIZE}" color="{Color.TableText}">Ваше Число сознания - {chislo_soznaniya}</font><br/>
    <font name="OpenSans" size="{HIGHLIGHTED_SIZE}" color="{Color.TableText}">(Положительные и отрицательные аспекты программы ума)</font>
    """)

    pl_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Планета</font>"""
    planeta = f"""{pl_text}
        <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}> – {planet_by_soznanie}</font>
    """

    brief_description_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Краткое описание личности по дате рождения:</font>"""
    brief_description = f"""{brief_description_text}<br/>
    <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>
        {name}, {brief_by_soznanie}</font>
    """

    vector_sozn_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Сознание направлено на</font>"""
    vector_sozn = f"""{vector_sozn_text}
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {soznanie_napravleno_by_soznanie}</font>
    """

    ego_hochet_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Ваше эго хочет:</font>"""
    ego_hochet = f"""{ego_hochet_text}
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {ego_hochet_by_soznanie}</font>
    """

    realizatsia_duwi_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Реализация души</font>"""
    realizatsia_duwi = f"""{realizatsia_duwi_text}
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {realizatsia_duwi_by_soznanie}</font>
    """
    princip_communicatsii_text = f"""<font name="OpenSansBold" size="{HIGHLIGHTED_SIZE}" color={Color.Highlighted}>Принцип коммуникации: </font>"""
    princip_communicatsii = f"""{princip_communicatsii_text}
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> {princip_communicatsii_by_soznanie}</font>
    """

    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=planeta)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=brief_description)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=vector_sozn)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=ego_hochet)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=realizatsia_duwi)
    create_text(elements, alignment=0, space_after=20, space_before=12, leading=40, text=princip_communicatsii)

    # Формируем содержимое ячеек
    positive_text: str = format_list(positive_aspect_by_soznanie)
    negative_text: str = format_list(negative_aspect_by_soznanie)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['OpenSansNormal']),
         Paragraph(negative_text, styles['OpenSansNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    tip_mishlenia_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Тип мышления - </font>"""
    tip_mishlenia = f"""{tip_mishlenia_text}
        <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}> {mind_type}</font>
    """
    mishlenie_desk = f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{mind_type_desc}</font>"""

    create_text(elements, alignment=0, space_after=0, space_before=12, leading=40, text=tip_mishlenia)
    create_text(elements, alignment=0, space_after=0, space_before=0, leading=40, text=mishlenie_desk)

    # Формируем содержимое ячеек
    ego_enjoys_by_text: str = format_list(ego_enjoys_by)
    ego_destroys_by_text: str = format_list(ego_destroys_by)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >Эго наслаждается</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >Эго разрушается</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(ego_enjoys_by_text, styles['OpenSansNormal']),
         Paragraph(ego_destroys_by_text, styles['OpenSansNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    create_text(elements, alignment=0, space_after=30, space_before=10,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Триггеры (ситуации, вызывающие негативные эмоции):</font>""")

    triggers_text: str = format_list(triggets_list)

    create_text(elements, alignment=0, space_before=15, space_after=45, left_indent=20, leading=20, text=triggers_text)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Цвет<br/>Вашего<br/>ЧС</font>', ParagraphStyle(name='', alignment=1, leading=30)),
         Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Цвет<br/>аксессуаров<br/>(кошелёк)</font>', ParagraphStyle(name='', alignment=1, leading=30)),
         Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Цветовая<br/>гамма<br/>одежды</font>', ParagraphStyle(name='', alignment=1, leading=30)),
         Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Ваш<br/>день<br/>недели</font>', ParagraphStyle(name='', alignment=1, leading=30)),
         Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Энергии цифр</font>', ParagraphStyle(name='', alignment=1, leading=30), )],
        [
            "", "", "", "",
            Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Лучшая</font>', ParagraphStyle(name='', alignment=1, leading=30)),
            Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Хорошая</font>', ParagraphStyle(name='', alignment=1, leading=30)),
            Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Нейтральная</font>', ParagraphStyle(name='', alignment=1, leading=30)),
            Paragraph(f'<font name="OpenSansBold" size="{18}" color={Color.TableText}>Отрицательная</font>', ParagraphStyle(name='', alignment=1, leading=30)),
        ],
        [Paragraph(f'<font name="OpenSans" size="{20}">{color_chs}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{color_wallet}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{color_gamma_clothes}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{week_day}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{best_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{good_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{neutral_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="OpenSans" size="{20}">{worst_digit_energy}</font>', styles['Table'])]
    ]

    # Создаем таблицу с 8 колонками
    side_padding = 20  # сколько хочешь отступ

    table_width = doc.width - side_padding * 2
    table = Table(
        data,
        colWidths=[
            table_width * 0.125,
            table_width * 0.125,
            table_width * 0.125,
            table_width * 0.125,
            table_width * 0.11,
            table_width * 0.11,
            table_width * 0.15,
            table_width * 0.165
        ]
    )

    # Настраиваем стиль таблицы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (7, 0), Color.TableBackground),
        ('BACKGROUND', (0, 1), (7, 1), Color.TableBackground),
        ('GRID', (0, 0), (-1, -1), 1, Color.Table),
        ('LEFTPADDING', (0, 0), (-1, -1), 1),
        ('RIGHTPADDING', (0, 0), (-1, -1), 1),
        ('TOPPADDING', (0, 0), (-1, -1), 15),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
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
    create_text(elements, alignment=0, space_after=10, space_before=12, leading=40, text=bolezni)

    create_orange_rect(elements, doc.width, 80, f"""
    <font name="OpenSansBold" size="{26}" color="{Color.TableText}">Ваше Число действия (жизненный путь) - {chislo_deystviya}</font><br/>
    """)

    opisanie_chislo_deistviya_text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Краткое описание по Числу действия: </font>"""
    opisanie_chislo_deistviya = f"""{opisanie_chislo_deistviya_text}<br/>
        <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{opisanie_by_chislo_deistviya}</font>
    """

    create_text(elements, alignment=0, space_after=10, space_before=12, leading=40, text=opisanie_chislo_deistviya)

    # Формируем содержимое ячеек
    positive_text: str = format_list(positive_aspect_by_deistvie)
    negative_text: str = format_list(negative_aspect_by_deistvie)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText} >В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['OpenSansNormal']),
         Paragraph(negative_text, styles['OpenSansNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    create_text(elements, alignment=0, space_before=10, space_after=20, leading=30,
                text=f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}> При выполнении Задачи по трансформации сознания, Ваше Число действия (жизненного пути) изменится с {chislo_deystviya} на {new_chislo_deystviya}. При этом у Вас откроются неограниченные возможности.</font>""")

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='OpenSansBold',
        fontSize=MAIN_SIZE,
        alignment=TA_CENTER,
        textColor=Color.TableText,
        leading=30))

    styles.add(ParagraphStyle(
        name='TableContent',
        fontName='OpenSans',
        fontSize=MAIN_SIZE,
        leftIndent=10,
        alignment=TA_LEFT,
        leading=30))
    styles.add(ParagraphStyle(
        name='TableContentBold',
        fontName='OpenSansBold',
        fontSize=MAIN_SIZE,
        alignment=TA_LEFT,
        textColor=Color.Highlighted,
        leading=40,
        leftIndent=20,
        spaceBefore=20))
    styles.add(ParagraphStyle(
        name='TableContentSub',
        fontName='OpenSans',
        fontSize=MAIN_SIZE,
        alignment=TA_LEFT,
        leading=30,
        leftIndent=30,  # Отступ слева для подпунктов
        spaceBefore=12,  # Отступ сверху для подпунктов
        textColor=Color.Main
    ))
    # Обновленные стили для подпунктов с отступом сверху

    data = [
        [
            Paragraph(f"Врожденные действия - {chislo_deystviya}", styles['TableHeader']),
            Paragraph(f"Измененные действия - {new_chislo_deystviya}", styles['TableHeader'])
        ],
        [
            [
                Paragraph("• В негативном аспекте (-):", styles['TableContentBold']),
                Paragraph(negative_aspect_vrozhdennogo_deystviya, styles['TableContentSub']),
                Spacer(1, 12),
                Paragraph("• В позитивном аспекте (+):", styles['TableContentBold']),
                Paragraph(positive_aspect_vrozhdennogo_deystviya, styles['TableContentSub'])
            ],
            [
                Paragraph("• При выполнении Задачи по трансформации сознания:", styles['TableContentBold']),
                Paragraph(
                    pri_vipolnenii_transformatsii,
                    styles['TableContentSub'])
            ]
        ]
    ]

    table = Table(data, colWidths=[doc.width / 2] * 2, rowHeights=[70, None])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color.TableBackground),
        ('GRID', (0, 0), (-1, -1), 1, Color.Highlighted),
        ('BOX', (0, 0), (-1, -1), 1, Color.TableBackground),  # Внешняя рамка
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Вертикальное выравнивание по центру для первой строки
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Вертикальное выравнивание по верхнему краю для остальных строк
    ]))

    elements.append(KeepTogether([
        table,
    ]))
    elements.append(Spacer(1, 20))

    create_orange_rect(elements, doc.width, 120, f"""
    <font name="OpenSansBold" size="{BIG_SIZE}" color="white">Ваш вектор жизни – {vector_zhizni}</font><br/>
    <font name="OpenSans" size="{HIGHLIGHTED_SIZE}" color="white">(Сфера - предназначения)</font>
    """)

    create_text(elements, alignment=0, space_before=15, leading=38, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">(Вектор жизни - показатель направленности в жизни, т.е. совокупность энергий, через
    которые человек приходит либо к стагнации и разрушению, либо к самореализации в жизни.
    Самореализация — процесс, который заключается в реализации человеком своих
    способностей, потенциалов и талантов, в каком-либо виде деятельности)</font>""")
    create_text(elements, alignment=0, space_before=10, space_after=20, leading=28, text=f"""
        <font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">
        Ваш вектор жизни направлен на
        </font>
        <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">
        {napravlenie_by_vector_zhizni}
        </font>""")


    # Создание таблицы для прямоугольника
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText}>Стагнация (отсутствие развития)</font>', ParagraphStyle(name='', alignment=1, leading=26)),
         Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.TableText}>Реализация (развитие потенциала)</font>', ParagraphStyle(name='', alignment=1, leading=26))],
        [Paragraph(f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{stagnatsia_by_vector_zhizni}</font>""", ParagraphStyle(name='', leading=36, leftIndent=20)),
         Paragraph(f"""<font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{realizatsia_by_vector_zhizni}</font>""", ParagraphStyle(name='', leading=36, leftIndent=20))]
    ]

    table = Table(data, colWidths=[doc.width / 2] * 2, rowHeights=[80, None])  # Ширина прямоугольника равна ширине страницы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (7, 0), Color.TableBackground),
        ('GRID', (0, 0), (-1, -1), 1, Color.TableBackground),  # Черная обводка
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное центрирование текста
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное центрирование текста
        ('TOPPADDING', (1, 0), (1, 1), 15),  # Отступ сверху
        ('BOTTOMPADDING', (1, 0), (1, 1), 15),  # Отступ снизу
    ]))
    elements.append(KeepTogether([
    table,
]))
    elements.append(Spacer(1, 25))

    create_orange_rect(elements, doc.width, 110, f"""
    <font name="OpenSansBold" size="{BIG_SIZE}" color="{Color.TableText}">Ваша Задача по трансформации сознания - {nomer_zadachi_ot_tvortsa}</font><br/>
    <font name="OpenSans" size="{HIGHLIGHTED_SIZE}" color="{Color.TableText}">(Задача от Творца)</font>
    """)

    create_zadacha_ot_tvortsa_func(elements)

    create_text(elements, alignment=1, space_before=20, space_after=20, leading=28, text=f"""<font name="OpenSans" size="{28}"
    color="{Color.Highlighted}">Формула задачи (стратегия счастливой жизни)</font>""")

    draw_formula_zadachi_tvortsa_func(elements)

    create_text(elements, alignment=0, space_before=30, space_after=40, leading=32, text=f"""
    <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Аффирмация</font>
    <font name="OpenSans" size="{MAIN_SIZE}"> (утверждение, помогающее создать положительный психологический
    настрой. Многократное повторение воздействует на подсознание и помогает создать новую
    модель мышления) </font>
    <font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>- {affirmatsia}</font>
    """)

    create_orange_rect(elements, doc.width, 120, f"""
    <font name="OpenSansBold" size="{BIG_SIZE}" color="{Color.TableText}">Ваша матрица врождённых энергий</font><br/>
    <font name="OpenSans" size="{HIGHLIGHTED_SIZE}" color="{Color.TableText}">(врожденные качества и компетенции личности)</font>
    """)

    elements.append(Spacer(1, 30))

    data: list = [
        ['3' * energy_matrix[2], '6' * energy_matrix[5], '9' * energy_matrix[8]],
        ['2' * energy_matrix[1], '5' * energy_matrix[4], '8' * energy_matrix[7]],
        ['1' * energy_matrix[0], '4' * energy_matrix[3], '7' * energy_matrix[6]]
    ]
    for e, i in enumerate(data):
        for e2, j in enumerate(i):
            data[e][e2] = Paragraph(f'<font name="OpenSans" size="{BIG_SIZE}" color="{Color.Highlighted}">{j}</font>', styles['OpenSansCenter'])

    table = Table(data, colWidths=100, rowHeights=100)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, Color.Highlighted),  # Черная обводка
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное центрирование текста
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное центрирование текста
    ]))
    elements.append(KeepTogether([
    table,
]))

    create_text(elements, alignment=0, space_before=20, space_after=20, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>В Вашей матрице заложены следующие энергии:</font>""")
    create_matrix_energy(elements, est_energy)

    create_text(elements, alignment=0, space_after=20, space_before=20, leading=28,
                text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>В Вашей матрице отсутствуют следующие энергии:</font>""")
    create_matrix_energy(elements, net_energy)

    create_text(elements, alignment=0, space_after=20, space_before=20, leading=28,
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

    create_orange_rect(elements, doc.width, 100, f"""
    <font name="OpenSansBold" size="{BIG_SIZE}" color="{Color.TableText}">Ваш личный год {datetime.now().year} г. - {lichniy_god}</font><br/>
    """)

    text = f"""
    <font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">{lichniy_god_description}</font><br/><br/>
    """
    if lichniy_god_sub_description is not None:
        text += f"""
            <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">{lichniy_god_sub_description}</font>
        """

    create_text(elements, alignment=0, space_after=20, space_before=15, leading=15, text=text)

    # Формируем содержимое ячеек
    positive_text = f"""<font name="OpenSans" size="{MAIN_SIZE}">{positive_aspect_by_lichny_god}</font>"""
    negative_text = f"""<font name="OpenSans" size="{MAIN_SIZE}">{negative_aspect_by_lichny_god}</font>"""

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.TableText}">В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.TableText}">В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['OpenSansNormal']),
         Paragraph(negative_text, styles['OpenSansNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    text = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>Рекомендации на этот год:</font>
    <font name="OpenSans" size="{MAIN_SIZE}" color={Color.Main}>{recomendations_na_god}</font>"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=40, text=text)

    text = f"""<font name="OpenSansBold" size="{BIG_SIZE}" color={Color.Highlighted}>{name}, я от всей души желаю Вам успеха!</font>"""
    create_text(elements, alignment=1, space_after=10, space_before=100, leading=34, text=text)

    # Создание PDF
    doc.build(elements, onFirstPage=header_canvas, onLaterPages=header_canvas)

    pdf_buffer.seek(0)
    file_path: str = f'{name}_{date_of_birth_str}.pdf'

    return pdf_buffer.read(), file_path


load_font()

if __name__ == '__main__':
    pdf = create_pdf('Osman', '03.03.2026')

    with open('ex.pdf', 'wb') as f:
        f.write(pdf[0])
