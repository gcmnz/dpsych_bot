from reportlab.platypus import Paragraph, Flowable, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import ParagraphStyle

from .color import Color
from .getters_text import get_narabotat_competencie_array_by_competencie_num

MAIN_SIZE = 22
MAIN_FONT = 'OpenSans'
MAIN_LEADING = 31
MAIN_SPACE = 20

NAME_SIZE = 24
NAME_LEADING = 35

HEADER_SIZE = 34
HEADER_FONT = "Cremona"
HEADER_LEADING = 34
HEADER_COLOR = Color.White
HEADER_SPACE = 20

SUBHEADER_SIZE = 20
SUBHEADER_FONT = "OpenSans"
SUBHEADER_LEADING = 20
SUBHEADER_COLOR = Color.White

TABLE_HEADER_SIZE = 22
TABLE_HEADER_FONT = "OpenSansBold"
TABLE_HEADER_LEADING = 31
TABLE_HEADER_COLOR = Color.White

TABLE_MAIN_SIZE = 22
TABLE_MAIN_FONT = "OpenSans"
TABLE_MAIN_LEADING = 31
TABLE_MAIN_COLOR = Color.Main

MATRIX_FONT = "Cremona"
MATRIX_SIZE = 40
MATRIX_LEADING = 40
MATRIX_COLOR = Color.Highlighted

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

height_: int = 250
cross_size: int = 40  # Size of the cross
equal_size: int = 40  # Size of the equal sign
arrow_size: int = 40  # Size of the right arrow


# Функция для преобразования списка в форматированный текст
def format_list(items: list[str]) -> str:
    formatted_items: list[str] = []
    for item in items:
        formatted_items.append(f'<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}> •  </font>'
                               f'<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{item}</font>')
    return f'<font name="{MAIN_FONT}" size="22" color={Color.Main}><br></br></font>'.join(formatted_items)


# Функция для преобразования списка в форматированный текст
def format_triggers_list(items: list[str]) -> str:
    formatted_items: list[str] = []
    for item in items:
        formatted_items.append(f'<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}> • </font>'
                               f'<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{item}</font>')
    return "<br/><br/>".join(formatted_items)


def create_text(
        elements: list[Flowable],
        text: str,
        alignment,
        space_after: int = 0,
        space_before: int = 0,
        leading: int = MAIN_LEADING,
        left_indent: int = 0,
        right_indent: int = 0,
        font_size: int = MAIN_SIZE,
) -> None:
    style = ParagraphStyle(
        name='custom',
        alignment=alignment,
        fontSize=font_size,
        spaceAfter=space_after,
        spaceBefore=space_before,
        leading=leading,
        leftIndent=left_indent,
        rightIndent=right_indent,
        bulletIndent=left_indent,  # ключевой момент
    )

    elements.append(KeepTogether(
        Paragraph(
            text,
            style=style,
        ))
    )


def create_matrix_energy(elements, array):
    for i in array:
        t = f"""<font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">• {i}</font>"""
        create_text(elements, left_indent=10, space_after=5, space_before=5, alignment=0, right_indent=40, text=t)


def create_recomendations(elements, array):
    for i in array:
        t = f"""
                <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}">• {i}</font>
                """
        create_text(elements, left_indent=10, space_after=10, space_before=10, alignment=0, text=t)


def create_build_competencies(elements, competencie_num: int):
    competencie_array: list[str] = get_narabotat_competencie_array_by_competencie_num(competencie_num)

    t = f"""<font name="OpenSansBold" size="{MAIN_SIZE}" color="{Color.Highlighted}">Как наработать качества/компетенции «{competencie_num}»:</font>"""
    create_text(elements, space_before=15, space_after=15, alignment=0, text=t)

    for competencie in competencie_array:
        t = f"""
             <font name="OpenSans" size="{MAIN_SIZE}" color="{Color.Main}"> • {competencie}</font>"""
        create_text(elements, left_indent=20, space_after=5, space_before=5, alignment=0, text=t)

    elements.append(Spacer(1, 10))


def draw_rectangles(elements, data):
    table = Table(
        data,
        hAlign='CENTER'
    )

    table.setStyle(TableStyle([
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))

    elements.append(KeepTogether([table]))


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
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")


def zadacha_by_2(elements):
    text = """
        «Научиться слушать и слышать людей любого уровня. Меньше анализировать, а больше действовать.
        Стать наставником в своей сфере деятельности»
    """
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text_list = ["стать номером 2 в отношениях", "научиться понимать другого человека (разговаривать с ним с позиции «снизу», задавать вопросы, уйти от монолога)",
                 "давать людям только те знания, которые им нужны", "прийти к пониманию (без понимания сложно добиться финансового успеха)."]

    t_list = []
    for t in text_list:
        t_list.append(
            f"""
            <font name="{MAIN_FONT}" size="{MAIN_SIZE}"> • </font>
            <font name="{MAIN_FONT}" size="{MAIN_SIZE}">{t}</font>
            """
        )
    create_text(elements, alignment=0, space_before=5, space_after=5, left_indent=20, text="<br/>".join(t_list))
    text = "Только через понимание людей Вы сможете действовать и добиться материального успеха."
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_3(elements):
    text = """
        «Ваша задача - не источать в мир энергию неудовлетворенности, разрушения и отчуждения. Только
        через расчет и выстраивание правильных последовательных действий Вы достигнете финансового
        успеха»
    """
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")


def zadacha_by_4(elements):
    text = """«Определить цель, не тратить время и энергию на пустые разговоры, а начать действовать. В
процессе действия появится вдохновение, которое приведет Вас к финансовому успеху»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text = """Как только Вы начинаете действовать, а не думать и анализировать, к Вам приходит ощущение всесилия."""
    create_text(elements, alignment=0, space_before=10, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_5(elements):
    text = """«Развивать интеллект, развивать коммуникативные и ораторские навыки. Расширение интеллекта
приведет Вас к гениальности, финансовому успеху и благополучию во всех сферах жизни»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")


def zadacha_by_6(elements):
    text = """«Заниматься физической активностью и телесно-ориентированными практиками: йогой, тантрой,
медитацией. Вам необходимо высвободить сексуальную энергию. Голова станет ясной и появится
желание трудиться, а труд приведет к финансовому успеху»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text = """Как только Вы поднимете энергию в голову, у Вас появятся творческие идеи и неуёмное желание их
претворять в жизнь (реальность)."""
    create_text(elements, alignment=0, space_before=10, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_7(elements):
    text = """«Научиться управлять материальным миром, а не разрешать ему управлять собой. Посвящать время
собственному духовному развитию. Уйти от тотального контроля. Научиться доверять и
сотрудничать с людьми»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text = """Как только Вы начинаете разговаривать с людьми по душам и доверять им, у Вас сразу возникают
дружественные отношения и желание помочь им."""
    create_text(elements, alignment=0, space_before=10, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_8(elements):
    text = """«Найти идею. Работать над ней индивидуально. Разработать стратегию и взять ответственность
на себя»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text = """Как только Вы начинаете трудиться на себя, то сразу чувствуете самодостаточность. У Вас появляются
деньги и независимость, становитесь автономным."""
    create_text(elements, alignment=0, space_before=10, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def zadacha_by_9(elements):
    text = """«Научиться светить, а не затмевать других людей, стать причиной их успеха. А также
контролировать свой финансовый поток»"""
    create_text(elements, alignment=0, space_before=15, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}" color={Color.Main}>{text}</font>""")

    text = """Как только проявите намерение привести другого человека к успеху – к Вам придут идеи, как это сделать.
Необходимо создавать возможности для личностного, профессионального и духовного роста других людей."""
    create_text(elements, alignment=0, space_before=10, space_after=15, text=f"""<font name="{MAIN_FONT}" size="{MAIN_SIZE}">{text}</font>""")


def draw_formula_tvortsa_by_1(elements):
    data = [
        [RectangleWithText(height=height_, text=f"""исполнительность<br/>
                                                              желание понять другого человека или ситуацию"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(height=height_, text=f"""разработка стратегии<br/>
                                                              принятие решений<br/>
                                                              ответственность на себя"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(height=height_, text=f"""расширение собственных возможностей<br/>
                                                              богатство (власть, деньги)<br/>
                                                              гармоничные отношения"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_2(elements):
    data = [
        [RectangleWithText(width=250, height=height_, text=f"""видение<br/>
                                                    целеустремлённость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=250, height=height_, text=f"""действия через анализ"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=250, height=height_, text=f"достижение целей, деньги, изобилие и гармония в отношениях"),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_3(elements):
    data = [
        [RectangleWithText(width=250, height=height_, text=f"""видение<br/>
                                                    целеустремлённость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=250, height=height_, text=f"""действия через анализ"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=250, height=height_, text=f"достижение целей, деньги, изобилие и гармония в отношениях"),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_4(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""интеллект (логика)"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""цель<br/>
                                                              действия"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=180, height=height_, text=f"""вдохновление (созидание)"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=180, height=height_, text=f"""в Вашу жизнь придут деньги и изобилие"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_5(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""мудрость (понимание жизни)<br/>
                                                              сексуальная энергия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""глубокие знания"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=180, height=height_, text=f"""гениальность"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=180, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_6(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""интуиция<br/>
                                                              харизма<br/>
                                                              сексуальная энергия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""йога<br/>
                                                              тантра<br/>
                                                              спорт (энергия поднимается в голову)"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=180, height=height_, text=f"""ясность в голове и желание трудиться"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=180, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_7(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""труд<br/>
                                                              мудрость"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""отказ от контроля<br/>
                                                              душевность и доверие к людям"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=180, height=height_, text=f"""внутренний покой и свобода сознания"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=180, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_8(elements):
    data = [
        [RectangleWithText(width=180, height=height_, text=f"""стремление к победе<br/>
                                                              динамика<br/>
                                                              действия"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=180, height=height_, text=f"""индивидуальность<br/>
                                                              автономность<br/>
                                                              ответственность"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=180, height=height_, text=f"""стратегия достижения целей"""),
         RightArrow(width=arrow_size, height=arrow_size),
         RectangleWithText(width=180, height=height_, text=f"""в Вашу жизнь придут деньги, изобилие и счастье в личной жизни"""),
         ],
    ]

    draw_rectangles(elements, data)


def draw_formula_tvortsa_by_9(elements):
    data = [
        [RectangleWithText(width=250, height=height_, text=f"""лидерство (руководство)<br/>
                                                    мотиватор (вдохновитель)<br/>
                                                    стратегическое мышление<br/>"""),
         Cross(width=cross_size, height=cross_size),
         RectangleWithText(width=250, height=height_, text=f"""выстраивание равноправных партнёрских отношений с людьми<br/>
                                                               контроль финансовых потоков"""),
         EqualSign(width=equal_size, height=equal_size),
         RectangleWithText(width=250, height=height_, text=f"в Вашу жизнь придут деньги, изобилие и гармоничные отношения"),
         ],
    ]

    draw_rectangles(elements, data)


class RoundedMatrix(Flowable):
    def __init__(self, table, size=260):
        super().__init__()
        self.table = table
        self.size = size
        self.radius = 12
        self.margin_bottom = 20

    def wrap(self, availWidth, availHeight):
        self.width = self.size
        self.height = self.size + self.margin_bottom
        return self.width, self.height

    def draw(self):
        c = self.canv

        # Рисуем рамку ОТНОСИТЕЛЬНО (0,0)
        c.setStrokeColor(Color.Highlighted)
        c.setLineWidth(2)

        c.roundRect(
            0,
            self.margin_bottom,
            self.size,
            self.size,
            self.radius,
            stroke=1,
            fill=0
        )

        # Таблица внутри (без смещения по X!)
        self.table.wrapOn(c, self.size, self.size)
        self.table.drawOn(c, 0, self.margin_bottom)


class RectangleWithText(Flowable):
    def __init__(self, text, width=250, height=80, radius=5):
        super().__init__()
        self.width = width
        self.height = height
        self.radius = radius
        self.text = text

        self.style = ParagraphStyle(
            name="",
            fontName="OpenSans",
            fontSize=20,
            leading=28,
            alignment=1,  # центр
            textColor=Color.Main
        )

    def wrap(self, availWidth, availHeight):
        return self.width + 12, self.height  # + margin-right

    def draw(self):
        c = self.canv

        # Рамка
        c.setStrokeColor(Color.Table)
        c.setLineWidth(2)
        c.roundRect(0, 0, self.width, self.height, self.radius, stroke=1, fill=0)

        # Текст
        p = Paragraph(self.text, self.style)
        w, h = p.wrap(self.width - 10, self.height - 10)
        p.drawOn(c, 5, (self.height - h) / 2)


class Cross(Flowable):
    def __init__(self, width=40, height=40):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width + 12, self.height

    def draw(self):
        c = self.canv
        x_offset = 6

        c.setStrokeColor(Color.Table)
        c.setLineWidth(8)

        c.line(x_offset, self.height / 2,
               self.width + x_offset, self.height / 2)

        c.line(self.width / 2 + x_offset, 0,
               self.width / 2 + x_offset, self.height)


class EqualSign(Flowable):
    def __init__(self, width=40, height=26):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width + 12, self.height

    def draw(self):
        c = self.canv
        x_offset = 6

        c.setStrokeColor(Color.Table)
        c.setLineWidth(7)

        c.line(x_offset, self.height * 0.65,
               self.width + x_offset, self.height * 0.65)

        c.line(x_offset, self.height * 0.35,
               self.width + x_offset, self.height * 0.35)


class RightArrow(Flowable):
    def __init__(self, width=40, height=26):
        super().__init__()
        self.width = width
        self.height = height

    def wrap(self, availWidth, availHeight):
        return self.width + 12, self.height

    def draw(self):
        c = self.canv
        x_offset = 6

        c.setStrokeColor(Color.Table)
        c.setLineWidth(6)

        c.line(x_offset,
               self.height / 2,
               self.width - 8 + x_offset,
               self.height / 2)

        c.line(self.width - 8 + 4,
               self.height / 2,
               self.width - 20 + 4,
               self.height - 5)

        c.line(self.width - 8 + 4,
               self.height / 2,
               self.width - 20 + 4,
               5)
