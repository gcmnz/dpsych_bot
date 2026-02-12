from reportlab.platypus import Paragraph, Flowable, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle

from color import Color
from getters_text import get_narabotat_competencie_array_by_competencie_num

MAIN_SIZE = 22

week_days: dict[str: str] = {
    'Monday': 'Понедельник',
    'Tuesday': 'Вторник',
    'Wednesday': 'Среда',
    'Thursday': 'Четверг',
    'Friday': 'Пятница',
    'Saturday': 'Суббота',
    'Sunday': 'Воскресенье'
}

char_to_digit: dict[str: int] = {'A': 1,
                                 'B': 2,
                                 'C': 3,
                                 'D': 4,
                                 'E': 5,
                                 'F': 8,
                                 'G': 3,
                                 'H': 5,
                                 'I': 1,
                                 'J': 1,
                                 'K': 2,
                                 'L': 3,
                                 'M': 4,
                                 'N': 5,
                                 'O': 7,
                                 'P': 8,
                                 'Q': 1,
                                 'R': 2,
                                 'S': 3,
                                 'T': 4,
                                 'U': 6,
                                 'V': 6,
                                 'W': 6,
                                 'X': 5,
                                 'Y': 1,
                                 'Z': 7}

height_: int = 150
cross_size: int = 30  # Size of the cross
equal_size: int = 30  # Size of the equal sign
arrow_size: int = 30  # Size of the right arrow


# Функция для преобразования списка в форматированный текст
def format_list(items: list[str]) -> str:
    formatted_items: list[str] = []
    for item in items:
        formatted_items.append(f'<font name="OpenSans" size="22" color={Color.Main}> • </font>'
                               f'<font name="OpenSans" size="22" color={Color.Main}>{item}</font>')
    return "<br/><br/>".join(formatted_items)


def create_text(elements: list[Flowable], text: str, alignment, space_after: int = 0, space_before: int = 0, leading: int = 12, left_indent: int = 0, right_indent: int = 0) -> None:
    elements.append(Paragraph(text, style=ParagraphStyle(name='', alignment=alignment, spaceAfter=space_after, leading=leading, spaceBefore=space_before, rightIndent=right_indent, leftIndent=left_indent)))


def create_orange_rect(elements, w, h, text):
    style = ParagraphStyle(
        name='',
        alignment=1,
        leading=32  # Межстрочный интервал
    )

    # Создание таблицы для прямоугольника
    data = [[Paragraph(text, style)]]
    table = Table(data, colWidths=[w], rowHeights=h)  # Ширина прямоугольника равна ширине страницы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), Color.TableBackground),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),  # Вертикальное центрирование текста
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Горизонтальное центрирование текста
    ]))

    elements.append(KeepTogether([
        table,
    ]))


def create_2x2_table(elements, w, data):
    table = Table(data, colWidths=[w / 2] * 2, rowHeights=None)  # Ширина ячеек равна половине ширины страницы
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), Color.TableBackground),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('GRID', (0, 0), (-1, -1), 1, Color.Highlighted),
        ('LEFTPADDING', (0, 0), (-1, -1), 25),
        ('RIGHTPADDING', (0, 0), (-1, -1), 25),
        ('TOPPADDING', (0, 0), (-1, -1), 20),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 40)
    ]))

    elements.append(KeepTogether([
        table,
    ]))


def create_matrix_energy(elements, array):
    for i in array:
        t = f"""<font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> • {i}</font>"""
        create_text(elements, left_indent=20, space_after=5, space_before=5, alignment=0, leading=32, right_indent=40, text=t)


def create_recomendations(elements, array):
    for i in array:
        t = f"""
                <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> • {i}</font>
                """
        create_text(elements, left_indent=20, space_after=10, space_before=10, alignment=0, leading=32, text=t)


def create_build_competencies(elements, competencie_num: int):
    competencie_array: list[str] = get_narabotat_competencie_array_by_competencie_num(competencie_num)

    t = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">Как наработать качества/компетенции «{competencie_num}»:</font>"""
    create_text(elements, left_indent=10, space_before=15, space_after=15, alignment=0, leading=28, text=t)

    for competencie in competencie_array:
        t = f"""
             <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> • {competencie}</font>"""
        create_text(elements, left_indent=20, space_after=5, space_before=5, alignment=0, leading=28, text=t)

    elements.append(Spacer(1, 10))


def draw_rectangles(elements, data):
    table = Table(data, colWidths=[None])
    table.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(KeepTogether([
        table,
    ]))


def get_create_zadacha_ot_tvortsa_func(nomer_zadachi_ot_tvortsa: int):
    d = {1: zadacha_by_1,
         2: zadacha_by_2,
         3: zadacha_by_3,
         4: zadacha_by_4,
         5: zadacha_by_5,
         6: zadacha_by_6,
         7: zadacha_by_7,
         8: zadacha_by_8,
         9: zadacha_by_9}

    return d[nomer_zadachi_ot_tvortsa]


def get_draw_formula_zadachi_tvortsa_func(nomer_zadachi_ot_tvortsa: int):
    d = {1: draw_formula_tvortsa_by_1,
         2: draw_formula_tvortsa_by_2,
         3: draw_formula_tvortsa_by_3,
         4: draw_formula_tvortsa_by_4,
         5: draw_formula_tvortsa_by_5,
         6: draw_formula_tvortsa_by_6,
         7: draw_formula_tvortsa_by_7,
         8: draw_formula_tvortsa_by_8,
         9: draw_formula_tvortsa_by_9}

    return d[nomer_zadachi_ot_tvortsa]


def zadacha_by_1(elements):
    text = """
        «Стать лидером (руководителем), самостоятельно принимать решения, взять ответственность за
        собственную жизнь на себя. Достичь финансового благополучия и передавать полученный опыт
        другим людям»
    """
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")


def zadacha_by_2(elements):
    text = """
        «Научиться слушать и слышать людей любого уровня. Меньше анализировать, а больше действовать.
        Стать наставником в своей сфере деятельности»
    """
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text_list = ["стать номером 2 в отношениях", "научиться понимать другого человека (разговаривать с ним с позиции «снизу», задавать вопросы, уйти от монолога)",
                 "давать людям только те знания, которые им нужны", "прийти к пониманию (без понимания сложно добиться финансового успеха)."]

    for t in text_list:
        create_text(elements, alignment=0, space_before=5, space_after=5, left_indent=20, leading=28, text=f"""
        <font name="OpenSans" size="15"> • </font>
        <font name="OpenSans" size="{MAIN_SIZE}">{t}</font>
    """)

    text = "Только через понимание людей Вы сможете действовать и добиться материального успеха."
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_3(elements):
    text = """
        «Ваша задача - не источать в мир энергию неудовлетворенности, разрушения и отчуждения. Только
        через расчет и выстраивание правильных последовательных действий Вы достигнете финансового
        успеха»
    """
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")


def zadacha_by_4(elements):
    text = """«Определить цель, не тратить время и энергию на пустые разговоры, а начать действовать. В
процессе действия появится вдохновение, которое приведет Вас к финансовому успеху»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text = """Как только Вы начинаете действовать, а не думать и анализировать, к Вам приходит ощущение всесилия."""
    create_text(elements, alignment=0, space_before=10, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_5(elements):
    text = """«Развивать интеллект, развивать коммуникативные и ораторские навыки. Расширение интеллекта
приведет Вас к гениальности, финансовому успеху и благополучию во всех сферах жизни»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")


def zadacha_by_6(elements):
    text = """«Заниматься физической активностью и телесно-ориентированными практиками: йогой, тантрой,
медитацией. Вам необходимо высвободить сексуальную энергию. Голова станет ясной и появится
желание трудиться, а труд приведет к финансовому успеху»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text = """Как только Вы поднимете энергию в голову, у Вас появятся творческие идеи и неуёмное желание их
претворять в жизнь (реальность)."""
    create_text(elements, alignment=0, space_before=10, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_7(elements):
    text = """«Научиться управлять материальным миром, а не разрешать ему управлять собой. Посвящать время
собственному духовному развитию. Уйти от тотального контроля. Научиться доверять и
сотрудничать с людьми»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text = """Как только Вы начинаете разговаривать с людьми по душам и доверять им, у Вас сразу возникают
дружественные отношения и желание помочь им."""
    create_text(elements, alignment=0, space_before=10, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_8(elements):
    text = """«Найти идею. Работать над ней индивидуально. Разработать стратегию и взять ответственность
на себя»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text = """Как только Вы начинаете трудиться на себя, то сразу чувствуете самодостаточность. У Вас появляются
деньги и независимость, становитесь автономным."""
    create_text(elements, alignment=0, space_before=10, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_9(elements):
    text = """«Научиться светить, а не затмевать других людей, стать причиной их успеха. А также
контролировать свой финансовый поток»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, leading=28, text=f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color={Color.Highlighted}>{text}</font>""")

    text = """Как только проявите намерение привести другого человека к успеху – к Вам придут идеи, как это сделать.
Необходимо создавать возможности для личностного, профессионального и духовного роста других людей."""
    create_text(elements, alignment=0, space_before=10, space_after=15, leading=28, text=f"""<font name="OpenSans" size="{MAIN_SIZE}">{text}</font>""")


def draw_formula_tvortsa_by_1(elements):
    data = [
        [RectangleWithText(width=200, height=height_, text=f"""• исполнительность<br/>
                                                              • желание понять другого человека или ситуацию"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=200, height=height_, text=f"""• разработка стратегии<br/>
                                                              • принятие решений<br/>
                                                              • ответственность на себя"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=220, height=height_, text=f"""• расширение собственных возможностей<br/>
                                                              • богатство (власть, деньги)<br/>
                                                              • гармоничные отношения"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_2(elements):
    data = [
        [RectangleWithText(width=200, height=height_, text=f"""• видение<br/>
                                                    • целеустремлённость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""• действия через анализ"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=200, height=height_, text=f"достижение целей, деньги, изобилие и гармония в отношениях"),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_3(elements):
    data = [
        [RectangleWithText(width=200, height=height_, text=f"""• видение<br/>
                                                    • целеустремлённость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=190, height=height_, text=f"""• действия через анализ"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=200, height=height_, text=f"достижение целей, деньги, изобилие и гармония в отношениях"),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_4(elements):
    data = [
        [RectangleWithText(width=140, height=height_, text=f"""• интеллект (логика)"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=160, height=height_, text=f"""• цель<br/>
                                                              • действия"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=140, height=height_, text=f"""вдохновление (созидание)"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=140, height=height_, text=f"""в Вашу жизнь придут деньги и изобилие"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_5(elements):
    data = [
        [RectangleWithText(width=140, height=height_, text=f"""• мудрость (понимание жизни)<br/>
                                                              • сексуальная энергия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=140, height=height_, text=f"""• глубокие знания"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=140, height=height_, text=f"""гениальность"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=140, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_6(elements):
    data = [
        [RectangleWithText(width=140, height=height_, text=f"""• интуиция<br/>
                                                              • харизма<br/>
                                                              • сексуальная энергия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=140, height=height_, text=f"""• йога<br/>
                                                              • тантра<br/>
                                                              • спорт (энергия поднимается в голову)"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=140, height=height_, text=f"""ясность в голове и желание трудиться"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=140, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_7(elements):
    data = [
        [RectangleWithText(width=140, height=height_, text=f"""• труд<br/>
                                                              • мудрость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=150, height=height_, text=f"""• отказ от контроля<br/>
                                                              • душевность и доверие к людям"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=140, height=height_, text=f"""внутренний покой и свобода сознания"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=150, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_8(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""• стремление к победе<br/>
                                                              • динамика<br/>
                                                              • действия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""• индивидуальность<br/>
                                                              • автономность<br/>
                                                              • ответственность"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=120, height=height_, text=f"""стратегия достижения целей"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=120, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_9(elements):
    data = [
        [RectangleWithText(width=200, height=height_, text=f"""• лидерство (руководство)<br/>
                                                    • мотиватор (вдохновитель)<br/>
                                                    • стратегическое мышление<br/>"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=200, height=height_, text=f"""• выстраивание равноправных партнёрских отношений с людьми<br/>
                                                               • контроль финансовых потоков"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=160, height=height_, text=f"в Вашу жизнь придут деньги, изобилие и гармоничные отношения"),
         ],
    ]

    draw_rectangles(elements, data)


class RectangleWithText(Flowable):
    def __init__(self, width, height, text):
        Flowable.__init__(self)
        self.width = width
        self.height = height
        self.style = ParagraphStyle(
            name='OpenSansCenter',
            fontName='OpenSans',
            fontSize=16,
            alignment=1,
            leading=18,  # Межстрочный интервал
            textColor=Color.Main
        )
        self.text = text

    def draw(self):
        self.canv.setStrokeColor(Color.Highlighted)
        self.canv.setFillColor(Color.White)
        self.canv.rect(0, 0, self.width, self.height, stroke=1, fill=1)
        self.canv.setFillColor(Color.Black)

        p = Paragraph(self.text, self.style)

        # Вычисляем ширину и высоту Paragraph
        w, h = p.wrap(self.width, self.height)

        # Вычисляем позицию для центрирования текста
        text_x = (self.width - w) / 2
        text_y = (self.height - h) / 2

        # Рисуем Paragraph
        p.drawOn(self.canv, text_x, text_y)


class Cross(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        # Добавляем обводку
        self.canv.setStrokeColor(Color.Cross)
        self.canv.setLineWidth(8)
        self.canv.line(0, self.height / 2, self.width, self.height / 2)
        self.canv.line(self.width / 2, 0, self.width / 2, self.height)


class EqualSign(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        self.canv.setStrokeColor(Color.Cross)
        self.canv.setLineWidth(8)
        self.canv.line(0, self.height / 2 + 6, self.width, self.height / 2 + 6)
        self.canv.line(0, self.height / 2 - 6, self.width, self.height / 2 - 6)


class RightArrow(Flowable):
    def __init__(self, width, height):
        Flowable.__init__(self)
        self.width = width
        self.height = height

    def draw(self):
        # Устанавливаем цвет и толщину линии
        self.canv.setStrokeColor(Color.Cross)
        self.canv.setLineWidth(8)

        # Вычисляем центр по вертикали
        center_x = self.width / 2
        center_y = self.height / 2

        # Рисуем основную линию
        self.canv.line(0, center_y, center_x + 5, center_y)

        self.canv.setLineWidth(4)
        self.canv.line(center_x + 7, center_y, center_x - 3, center_y - 11)
        self.canv.line(center_x + 7, center_y, center_x - 3, center_y + 11)

        self.canv.setLineWidth(3)
        self.canv.line(center_x + 3, center_y + 5, center_x + 9, center_y - 1)
