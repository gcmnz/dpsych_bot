import io

from reportlab.platypus import SimpleDocTemplate
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .alg import *
from .utils import *
from .getters_text import *


def load_font():
    # Загрузка шрифта Times New Roman
    pdfmetrics.registerFont(TTFont('TimesNewRoman', 'times.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanItalic', 'timesi.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanItalicBold', 'timesbi.ttf'))
    pdfmetrics.registerFont(TTFont('TimesNewRomanBold', 'timesbd.ttf'))


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

    doc = SimpleDocTemplate(pdf_buffer, pagesize=(595, 720), leftMargin=42, rightMargin=42, topMargin=30, bottomMargin=20)
    elements: list[Flowable] = []

    # Стили текста
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name='TimesNewRomanCenter',
        fontName='TimesNewRoman',
        fontSize=12,
        alignment=TA_CENTER,
        leading=18  # Межстрочный интервал
    ))

    styles.add(ParagraphStyle(
        name='TimesNewRomanNormal',
        fontName='TimesNewRoman',
        fontSize=12,
        leading=16  # Увеличенный межстрочный интервал
    ))
    styles.add(ParagraphStyle(
        name='Table',
        fontName='TimesNewRoman',
        alignment=1,
        leading=20
    ))

    create_text(elements, alignment=2, space_after=20,
                text=f'<font name="TimesNewRomanItalic" size="10" color={Color.Black}>Дата составления документа {datetime.now().strftime('%d.%m.%Y')}</font>'
                )

    create_text(elements, alignment=2, space_after=10, text=f"""
                    <font name="TimesNewRomanItalicBold" size="14" color={Color.Orange}>«Познание начинается с удивления»</font>
                """)

    create_text(elements, alignment=2, space_after=75, text=f"""
        <font name="TimesNewRomanItalicBold" size="14" color={Color.Orange}>Аристотель</font>
    """)

    create_text(elements, alignment=1, space_after=38, text=f"""
        <font name="TimesNewRomanItalicBold" size="14" color={Color.Blue}>Цифровая психология - стратегия счастливой жизни.</font>
    """)

    create_text(elements, alignment=1, space_after=38, text=f"""
        <font name="TimesNewRomanItalicBold" size="14" color={Color.Orange}>{name} (дата рождения {date_of_birth_str} - {week_day_of_birth}) {chislo_soznaniya} / {chislo_deystviya}</font>
    """)

    create_text(elements, alignment=1, space_after=20, text=f"""
        <font name="TimesNewRomanItalicBold" size="14" color={Color.Blue}>Энергия имени</font>
        <font name="TimesNewRomanBold" size="14" color={Color.Name}>{name.upper()}</font>
        <font name="TimesNewRoman" size="14" color={Color.Black}> - {name_energy_digit} {name_energy_description}</font>
    """)

    create_orange_rect(elements, doc.width, 50, f"""
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваше Число сознания - {chislo_soznaniya}</font><br/>
    <font name="TimesNewRomanItalic" size="14" color="white">(Положительные и отрицательные аспекты программы ума)</font>
    """)

    pl_text = f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Планета</font>"""
    planeta = f"""{pl_text}
        <font name="TimesNewRoman" size="12" color={Color.Black}> – {planet_by_soznanie}</font>
    """

    brief_description_text = f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Краткое описание личности по дате рождения:</font>"""
    brief_description = f"""{brief_description_text}<br/>
    <font name="TimesNewRoman" size="12" color={Color.Black}>
        {name}, {brief_by_soznanie}</font>
    """

    vector_sozn_text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Сознание направлено на</font>"""
    vector_sozn = f"""{vector_sozn_text}
        <font name="TimesNewRoman" size="12" color="{Color.Black}"> {soznanie_napravleno_by_soznanie}</font>
    """

    ego_hochet_text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Ваше эго хочет:</font>"""
    ego_hochet = f"""{ego_hochet_text}
        <font name="TimesNewRoman" size="12" color="{Color.Black}"> {ego_hochet_by_soznanie}</font>
    """

    realizatsia_duwi_text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Реализация души</font>"""
    realizatsia_duwi = f"""{realizatsia_duwi_text}
        <font name="TimesNewRoman" size="12" color="{Color.Black}"> {realizatsia_duwi_by_soznanie}</font>
    """
    princip_communicatsii_text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Принцип коммуникации: </font>"""
    princip_communicatsii = f"""{princip_communicatsii_text}
        <font name="TimesNewRoman" size="12" color="{Color.Black}"> {princip_communicatsii_by_soznanie}</font>
    """

    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=planeta)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=brief_description)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=vector_sozn)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=ego_hochet)
    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=realizatsia_duwi)
    create_text(elements, alignment=0, space_after=20, space_before=12, leading=18, text=princip_communicatsii)

    # Формируем содержимое ячеек
    positive_text: str = format_list(positive_aspect_by_soznanie)
    negative_text: str = format_list(negative_aspect_by_soznanie)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['TimesNewRomanNormal']),
         Paragraph(negative_text, styles['TimesNewRomanNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    tip_mishlenia_text = f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Тип мышления - </font>"""
    tip_mishlenia = f"""{tip_mishlenia_text}
        <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}> {mind_type}</font>
    """
    mishlenie_desk = f"""<font name="TimesNewRoman" size="12" color={Color.Black}>{mind_type_desc}</font>"""

    create_text(elements, alignment=0, space_after=0, space_before=12, leading=18, text=tip_mishlenia)
    create_text(elements, alignment=0, space_after=0, space_before=0, leading=18, text=mishlenie_desk)

    # Формируем содержимое ячеек
    ego_enjoys_by_text: str = format_list(ego_enjoys_by)
    ego_destroys_by_text: str = format_list(ego_destroys_by)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >Эго наслаждается</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >Эго разрушается</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(ego_enjoys_by_text, styles['TimesNewRomanNormal']),
         Paragraph(ego_destroys_by_text, styles['TimesNewRomanNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    create_text(elements, alignment=0, space_after=10, space_before=10,
                text=f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Триггеры </font><font name="TimesNewRomanItalic" size="12">(ситуации, вызывающие негативные эмоции):</font>""")

    triggers_text: str = format_list(triggets_list)

    create_text(elements, alignment=0, space_before=15, space_after=45, left_indent=20, text=triggers_text)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Цвет<br/>Вашего<br/>ЧС</font>', ParagraphStyle(name='', alignment=1, leading=15)),
         Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Цвет<br/>аксессуаров<br/>(кошелёк)</font>', ParagraphStyle(name='', alignment=1, leading=15)),
         Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Цветовая<br/>гамма<br/>одежды</font>', ParagraphStyle(name='', alignment=1, leading=15)),
         Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Ваш<br/>день<br/>недели</font>', ParagraphStyle(name='', alignment=1, leading=20)),
         Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Энергии цифр</font>', ParagraphStyle(name='', alignment=1, leading=15), )],
        [
            "", "", "", "",
            Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Лучшая</font>', ParagraphStyle(name='', alignment=1, leading=15)),
            Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Хорошая</font>', ParagraphStyle(name='', alignment=1, leading=15)),
            Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Нейтральная</font>', ParagraphStyle(name='', alignment=1, leading=15)),
            Paragraph(f'<font name="TimesNewRoman" size="12" color={Color.White}>Отрицательная</font>', ParagraphStyle(name='', alignment=1, leading=15)),
        ],
        [Paragraph(f'<font name="TimesNewRoman" size="12">{color_chs}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{color_wallet}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{color_gamma_clothes}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{week_day}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{best_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{good_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{neutral_digit_energy}</font>', styles['Table']),
         Paragraph(f'<font name="TimesNewRoman" size="12">{worst_digit_energy}</font>', styles['Table'])]
    ]

    # Создаем таблицу с 8 колонками
    table = Table(data, colWidths=[doc.width * 0.125, doc.width * 0.145, doc.width * 0.145, doc.width * 0.135,
                                   doc.width * 0.11, doc.width * 0.11, doc.width * 0.15, doc.width * 0.165])

    # Настраиваем стиль таблицы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (7, 0), Color.Orange),
        ('BACKGROUND', (0, 1), (7, 1), Color.Orange),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
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

    # Добавляем таблицу в документ
    elements.append(table)

    bolezni_text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Blue}>Болезни: </font>"""
    bolezni = f"""{bolezni_text}
        <font name="TimesNewRoman" size="12" color="{Color.Black}"> {bolezni_by_soznanie}</font>
    """
    create_text(elements, alignment=0, space_after=10, space_before=12, leading=18, text=bolezni)

    create_orange_rect(elements, doc.width, 30, f"""
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваше Число действия (жизненный путь) - {chislo_deystviya}</font><br/>
    """)

    opisanie_chislo_deistviya_text = f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Краткое описание по Числу действия: </font>"""
    opisanie_chislo_deistviya = f"""{opisanie_chislo_deistviya_text}<br/>
        <font name="TimesNewRoman" size="12">{opisanie_by_chislo_deistviya}</font>
    """

    create_text(elements, alignment=0, space_after=10, space_before=12, leading=18, text=opisanie_chislo_deistviya)

    # Формируем содержимое ячеек
    positive_text: str = format_list(positive_aspect_by_deistvie)
    negative_text: str = format_list(negative_aspect_by_deistvie)

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue} >В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['TimesNewRomanNormal']),
         Paragraph(negative_text, styles['TimesNewRomanNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    create_text(elements, alignment=0, space_before=10, space_after=20, leading=20,
                text=f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}> При выполнении Задачи по трансформации сознания, Ваше Число действия (жизненного пути) изменится с {chislo_deystviya} на {new_chislo_deystviya}. При этом у Вас откроются неограниченные возможности.</font>""")

    styles.add(ParagraphStyle(
        name='TableHeader',
        fontName='TimesNewRomanItalicBold',
        fontSize=12,
        alignment=TA_CENTER,
        textColor=Color.Blue,
        leading=14))

    styles.add(ParagraphStyle(
        name='TableContent',
        fontName='TimesNewRoman',
        fontSize=12,
        leftIndent=10,
        alignment=TA_LEFT,
        leading=14))
    styles.add(ParagraphStyle(
        name='TableContentBold',
        fontName='TimesNewRomanItalicBold',
        fontSize=12,
        alignment=TA_LEFT,
        textColor=Color.Blue,
        leading=18,
        leftIndent=20))
    styles.add(ParagraphStyle(
        name='TableContentSub',
        fontName='TimesNewRoman',
        fontSize=12,
        alignment=TA_LEFT,
        leading=17,
        leftIndent=30,  # Отступ слева для подпунктов
        spaceBefore=12  # Отступ сверху для подпунктов
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

    table = Table(data, colWidths=[doc.width / 2] * 2, rowHeights=[40, None])
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Границы ячеек
        ('BOX', (0, 0), (-1, -1), 1, colors.black),  # Внешняя рамка
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.black),  # Внутренние линии
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),  # Вертикальное выравнивание по центру для первой строки
        ('VALIGN', (0, 1), (-1, -1), 'TOP'),  # Вертикальное выравнивание по верхнему краю для остальных строк
    ]))

    elements.append(table)
    elements.append(Spacer(1, 10))

    create_orange_rect(elements, doc.width, 50, f"""
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваш вектор жизни – {vector_zhizni}</font><br/>
    <font name="TimesNewRomanItalic" size="14" color="white">(Сфера - предназначения)</font>
    """)

    create_text(elements, alignment=0, space_before=15, leading=17, text="""<font name="TimesNewRomanItalic" size="12">(Вектор жизни - показатель направленности в жизни, т.е. совокупность энергий, через
    которые человек приходит либо к стагнации и разрушению, либо к самореализации в жизни.
    Самореализация — процесс, который заключается в реализации человеком своих
    способностей, потенциалов и талантов, в каком-либо виде деятельности)</font>""")

    create_text(elements, alignment=0, space_before=10, space_after=15,
                text=f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Ваш вектор жизни направлен на {napravlenie_by_vector_zhizni}</font>""")

    # Создание таблицы для прямоугольника
    data = [
        [Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Стагнация (отсутствие развития)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Реализация (развитие потенциала)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(f"""<font name="TimesNewRoman" size="12">{stagnatsia_by_vector_zhizni}</font>""", ParagraphStyle(name='', leading=16, leftIndent=20)),
         Paragraph(f"""<font name="TimesNewRoman" size="12">{realizatsia_by_vector_zhizni}</font>""", ParagraphStyle(name='', leading=16, leftIndent=20))]
    ]

    table = Table(data, colWidths=[doc.width / 2] * 2, rowHeights=[50, None])  # Ширина прямоугольника равна ширине страницы
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Черная обводка
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное центрирование текста
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное центрирование текста
        ('TOPPADDING', (1, 0), (1, 1), 15),  # Отступ сверху
        ('BOTTOMPADDING', (1, 0), (1, 1), 15),  # Отступ снизу
    ]))
    elements.append(table)
    elements.append(Spacer(1, 10))

    create_orange_rect(elements, doc.width, 50, f"""
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваша Задача по трансформации сознания - {nomer_zadachi_ot_tvortsa}</font><br/>
    <font name="TimesNewRomanItalic" size="14" color="white">(Задача от Творца)</font>
    """)

    create_zadacha_ot_tvortsa_func(elements)

    create_text(elements, alignment=1, space_before=10, space_after=10, leading=17, text=f"""<font name="TimesNewRomanItalicBold" size="12"
    color={Color.Blue}>Формула задачи (стратегия счастливой жизни)
    </font>""")

    draw_formula_zadachi_tvortsa_func(elements)

    create_text(elements, alignment=0, space_before=10, space_after=10, leading=23, text=f"""
    <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Аффирмация</font>
    <font name="TimesNewRomanItalic" size="12">(утверждение, помогающее создать положительный психологический
    настрой. Многократное повторение воздействует на подсознание и помогает создать новую
    модель мышления)</font>
    <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>- {affirmatsia}</font>
    """)

    create_orange_rect(elements, doc.width, 50, """
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваша матрица врождённых энергий (матрица компетенций)</font><br/>
    <font name="TimesNewRomanItalic" size="14" color="white">(врожденные качества и компетенции личности)</font>
    """)

    elements.append(Spacer(1, 20))

    data: list = [
        ['3' * energy_matrix[2], '6' * energy_matrix[5], '9' * energy_matrix[8]],
        ['2' * energy_matrix[1], '5' * energy_matrix[4], '8' * energy_matrix[7]],
        ['1' * energy_matrix[0], '4' * energy_matrix[3], '7' * energy_matrix[6]]
    ]
    for e, i in enumerate(data):
        for e2, j in enumerate(i):
            data[e][e2] = Paragraph(f'<font name="TimesNewRoman" size="16">{j}</font>', styles['TimesNewRomanCenter'])

    table = Table(data, colWidths=50, rowHeights=50)
    table.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Черная обводка
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное центрирование текста
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное центрирование текста
    ]))
    elements.append(table)

    create_text(elements, alignment=1, space_before=10, space_after=10, leading=17, text=f"""<font name="TimesNewRomanItalicBold" size="12"
    color={Color.Blue}>Линии в матрице
    </font>
    <font name="TimesNewRomanItalic" size="12"
    color={Color.Brown}>(сочетание энергий формируют характерные черты личности и
        врождённый потенциал)
    </font>
    """)

    create_text(elements, alignment=0, space_before=10, space_after=10, left_indent=20, leading=17,
                text=f"""
                <font name="TimesNewRoman" size="15"> • </font>
                <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}
                >Программа эгоцентризма</font>
                <font name="TimesNewRoman" size="12">
                («Я хочу, чтобы все думали и делали только так, как я хочу»)</font>
                """)

    create_text(elements, alignment=0, space_before=30, space_after=30, left_indent=20, leading=17,
                text=f"""
                <font name="TimesNewRoman" size="15"> • </font>
                <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}
                >Знания перетекают в опыт</font>
                <font name="TimesNewRoman" size="12">
                (4-8, где 4 – знания, 8 – опыт/практика/труд</font>
                """)

    create_text(elements, alignment=0, space_before=30, space_after=30, left_indent=20, leading=20,
                text=f"""
                <font name="TimesNewRoman" size="15"> • </font>
                <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}
                >Быстрое восстановление</font>
                <font name="TimesNewRoman" size="12">
                (перезагрузка) (где 6 – комфорт/отдых, 8 –
                труд/безмятежность. Человек способен быстро восстанавливать свои силы</font>
                """)

    create_text(elements, alignment=0, space_before=30, space_after=30, left_indent=20, leading=17,
                text=f"""
                <font name="TimesNewRoman" size="15"> • </font>
                <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}
                >Линия конечного результата</font>
                <font name="TimesNewRoman" size="12">
                (способность видеть конечный результат дела ещё до его
                начала, умение завершать дела)</font>
                """)

    create_text(elements, alignment=0, space_after=15, text=f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>В Вашей матрице заложены следующие энергии:</font>""")
    create_matrix_energy(elements, est_energy)

    create_text(elements, alignment=0, space_after=15, space_before=20,
                text=f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>В Вашей матрице отсутствуют следующие энергии:</font>""")
    create_matrix_energy(elements, net_energy)

    create_text(elements, alignment=0, space_after=15, space_before=20,
                text=f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Рекомендации по наработке отсутствующих энергий:</font>""")

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

    create_orange_rect(elements, doc.width, 30, f"""
    <font name="TimesNewRomanItalicBold" size="16" color="white">Ваш личный год {datetime.now().year} г. - {lichniy_god}</font><br/>
    """)

    text = f"""
    <font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>{lichniy_god_description}</font><br/><br/>
    """
    if lichniy_god_sub_description is not None:
        text += f"""
            <font name="TimesNewRomanItalic" size="12" color={Color.Brown}>{lichniy_god_sub_description}</font>
        """

    create_text(elements, alignment=0, space_after=15, space_before=15, leading=15, text=text)

    # Формируем содержимое ячеек
    positive_text = f"""<font name="TimesNewRoman" size="12">{positive_aspect_by_lichny_god}</font>"""
    negative_text = f"""<font name="TimesNewRoman" size="12">{negative_aspect_by_lichny_god}</font>"""

    # Создаем данные для таблицы
    data = [
        [Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>В позитивном аспекте (+)</font>', ParagraphStyle(name='', alignment=1)),
         Paragraph(f'<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>В негативном аспекте (-)</font>', ParagraphStyle(name='', alignment=1))],
        [Paragraph(positive_text, styles['TimesNewRomanNormal']),
         Paragraph(negative_text, styles['TimesNewRomanNormal'])]
    ]
    create_2x2_table(elements, doc.width, data)

    text = f"""<font name="TimesNewRomanItalicBold" size="12" color={Color.Blue}>Рекомендации на этот год:</font>
    <font name="TimesNewRoman" size="12" color={Color.Brown}>{recomendations_na_god}</font>"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=18, text=text)

    text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Red}>{name}, я от всей души желаю Вам успеха!</font>"""
    create_text(elements, alignment=1, space_after=10, text=text)

    text = f"""<font name="TimesNewRomanBold" size="12" color={Color.Red}>С Уважением,</font>"""
    create_text(elements, alignment=1, text=text)

    # Создание PDF
    doc.build(elements)
    pdf_buffer.seek(0)
    file_path: str = f'{name}_{date_of_birth_str}.pdf'

    return pdf_buffer.read(), file_path


load_font()
