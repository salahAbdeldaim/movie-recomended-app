import flet
from flet import *
import sqlite3
import random

# تعريف الألوان
RED = Colors.RED
PURE_RED = "#F9FFE1"
GRAY = Colors.GREY_500
GRAY2 = "#E6E6E6"
BLACK = Colors.BLACK
ACCENT_COLOR = "#FF6F61"

# تهيئة قاعدة البيانات
def initialize_database(content_type):
    try:
        conn = sqlite3.connect(f'{content_type}.db')
        cursor = conn.cursor()
        cursor.execute(f'''CREATE TABLE IF NOT EXISTS {content_type} (
            title TEXT, genres TEXT, averageRating REAL, releaseYear INTEGER
        )''')
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_genres ON {content_type} (genres)")
        cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_title ON {content_type} (title)")
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        return str(e)
    return None

# جلب البيانات من قاعدة البيانات
def get_data(page: Page, content_type: str, genre: str = None, search_query: str = None, for_suggestions: bool = False):
    try:
        conn = sqlite3.connect(f'{content_type}.db')
        cursor = conn.cursor()
        if for_suggestions:
            query = f"SELECT title FROM {content_type}"
        else:
            query = f"SELECT title, genres, averageRating, releaseYear FROM {content_type}"
        params = []
        conditions = []
        if genre and genre != "All":
            conditions.append("genres LIKE ?")
            params.append(f'%{genre}%')
        if search_query:
            conditions.append("title LIKE ?")
            params.append(f'%{search_query}%')  # البحث في أي مكان داخل العنوان
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        cursor.execute(query, params)
        data = cursor.fetchall()
        count = len(data)
        conn.close()
        if for_suggestions:
            return [row[0] for row in data], count  # إرجاع الأسماء فقط
        return data, count
    except sqlite3.Error as e:
        page.snack_bar = SnackBar(
            content=Row(
                controls=[
                    Icon(Icons.WARNING, color=Colors.WHITE, size=20),
                    Text(f"خطأ في قاعدة البيانات: {e}", size=16, color=Colors.WHITE),
                ],
                alignment=MainAxisAlignment.CENTER,
            ),
            bgcolor=Colors.RED_700,
            duration=4000,
            show_close_icon=True,
            close_icon_color=Colors.WHITE,
        )
        page.snack_bar.open = True
        page.update()
        return [], 0

# اختيار عنصر عشوائي
def get_random_item(data):
    return random.choice(data) if data else None

# تحديث نصوص الأزرار
def update_button_labels(content_type: str, b1: ElevatedButton, b2: ElevatedButton):
    b1.content.value = "فيلم جديد" if content_type == "movies" else "مسلسل جديد"
    b2.content.value = "فيلم عشوائي" if content_type == "movies" else "مسلسل عشوائي"

# إنشاء محتوى الصندوق
def create_content_page(page: Page, content_type: str, genre: str = None, search_query: str = None, dropdown: Dropdown = None):
    data, count = get_data(page, content_type, genre, search_query)
    random_item = get_random_item(data)
    content_name = "مسلسلات" if content_type == "series" else "أفلام"

    if random_item:
        content = Column(
            controls=[
                Text(
                    random_item[0],
                    size=20,
                    weight=FontWeight.BOLD,
                    color=ACCENT_COLOR,
                    text_align=TextAlign.CENTER,
                ),
                Row(
                    controls=[
                        Icon(Icons.CALENDAR_TODAY, size=16, color=ACCENT_COLOR),
                        Text(f"السنة: {random_item[3]}", size=16, color=BLACK),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Column(
                    controls=[
                        Row(
                            controls=[
                                Icon(Icons.LABEL, size=16, color=ACCENT_COLOR),
                                Text("الأنواع:", size=16, color=BLACK),
                            ],
                            alignment=MainAxisAlignment.CENTER,
                        ),
                        Text(
                            random_item[1],
                            size=16,
                            color=BLACK,
                            text_align=TextAlign.CENTER,
                            width=280,
                            max_lines=2,
                            overflow=TextOverflow.ELLIPSIS,
                        ),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                    spacing=5,
                ),
                Row(
                    controls=[
                        Icon(Icons.STAR, size=16, color=ACCENT_COLOR),
                        Text(f"التقييم: {random_item[2]}", size=16, color=BLACK),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                Divider(height=10, color=Colors.TRANSPARENT),
                Text(
                    f"عدد {content_name} في هذا البحث: {count}",
                    size=14,
                    color=BLACK,
                    text_align=TextAlign.CENTER,
                    weight=FontWeight.W_500,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10,
        )
    else:
        content = Column(
            controls=[
                Text(f"لا توجد {content_name} تحتوي على '{search_query}' لهذا النوع!" if search_query else f"لا توجد {content_name} متاحة لهذا النوع!", size=16, color=BLACK),
                ElevatedButton(
                    content=Text("جرب بحثًا آخر", size=14, color=Colors.WHITE),
                    style=ButtonStyle(
                        bgcolor=ACCENT_COLOR,
                        color=Colors.WHITE,
                        padding=10,
                        shape=RoundedRectangleBorder(radius=8),
                    ),
                    on_click=lambda e: (dropdown.__setattr__('value', None), dropdown.update()) if dropdown else None,
                ),
            ],
            alignment=MainAxisAlignment.CENTER,
            horizontal_alignment=CrossAxisAlignment.CENTER,
            spacing=10,
        )

    return Container(
        height=300,
        width=320,
        border_radius=16,
        bgcolor=GRAY2,
        padding=20,
        shadow=BoxShadow(
            spread_radius=2,
            blur_radius=10,
            color=Colors.with_opacity(0.2, Colors.BLACK),
            offset=Offset(0, 4),
        ),
        gradient=LinearGradient(
            begin=alignment.top_center,
            end=alignment.bottom_center,
            colors=[GRAY2, Colors.with_opacity(0.9, GRAY2)],
        ),
        content=content,
        alignment=alignment.center,
    )

def main(page: Page):
    page.title = "فيلم - مسلسل عشوائي"
    page.window.top = 50
    page.window.left = 1100
    page.window.width = 360
    page.window.height = 800
    page.bgcolor = RED
    page.scroll = ScrollMode.AUTO
    page.rtl = True
    page.padding = 20
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.theme = Theme(
        font_family="Roboto",
        text_theme=TextTheme(
            body_medium=TextStyle(size=16, color=BLACK, weight=FontWeight.W_500),
            headline_medium=TextStyle(size=20, color=BLACK, weight=FontWeight.BOLD),
        ),
    )

    # تهيئة قواعد البيانات
    for content_type in ["movies", "series"]:
        error = initialize_database(content_type)
        if error:
            page.snack_bar = SnackBar(
                content=Text(f"خطأ في تهيئة قاعدة بيانات {content_type}: {error}", color=Colors.WHITE),
                bgcolor=Colors.RED_700,
                duration=4000,
                show_close_icon=True,
                close_icon_color=Colors.WHITE,
            )
            page.snack_bar.open = True
            page.update()
            return

    # AppBar
    page.appbar = AppBar(
        bgcolor=PURE_RED,
        title=Text("فيلم - مسلسل عشوائي", color=BLACK, weight=FontWeight.BOLD, size=20),
        center_title=True,
        leading=Icon(Icons.HOME, color=ACCENT_COLOR),
        leading_width=40,
        elevation=2,
        shadow_color=Colors.with_opacity(0.3, Colors.BLACK),
        actions=[
            PopupMenuButton(
                icon=Icons.SETTINGS,
                icon_color=ACCENT_COLOR,
                items=[
                    PopupMenuItem(text="الإعدادات"),
                    PopupMenuItem(),
                    PopupMenuItem(text="حول التطبيق"),
                    PopupMenuItem(),
                    PopupMenuItem(text="من نحن"),
                ],
            )
        ],
    )

    # القائمة المنسدلة للأنواع
    options = [
        {"key": "All", "text": "All - الكل"},
        {"key": "Action", "text": "Action - أكشن"},
        {"key": "Adventure", "text": "Adventure - مغامرة"},
        {"key": "Animation", "text": "Animation - رسوم متحركة"},
        {"key": "Biography", "text": "Biography - سيرة ذاتية"},
        {"key": "Comedy", "text": "Comedy - كوميدي"},
        {"key": "Crime", "text": "Crime - جريمة"},
        {"key": "Documentary", "text": "Documentary - وثائقي"},
        {"key": "Drama", "text": "Drama - دراما"},
        {"key": "Family", "text": "Family - عائلي"},
        {"key": "Fantasy", "text": "Fantasy - فانتازيا"},
        {"key": "Game-Show", "text": "Game-Show - برنامج مسابقات"},
        {"key": "History", "text": "History - تاريخي"},
        {"key": "Horror", "text": "Horror - رعب"},
        {"key": "Music", "text": "Music - موسيقي"},
        {"key": "Musical", "text": "Musical - موسيقي درامي"},
        {"key": "Mystery", "text": "Mystery - غموض"},
        {"key": "News", "text": "News - أخبار"},
        {"key": "Reality-TV", "text": "Reality-TV - تلفزيون الواقع"},
        {"key": "Romance", "text": "Romance - رومانسي"},
        {"key": "Sci-Fi", "text": "Sci-Fi - خيال علمي"},
        {"key": "Short", "text": "Short - قصير"},
        {"key": "Sport", "text": "Sport - رياضي"},
        {"key": "Talk-Show", "text": "Talk-Show - برنامج حواري"},
        {"key": "Thriller", "text": "Thriller - إثارة"},
        {"key": "War", "text": "War - حرب"},
        {"key": "Western", "text": "Western - غربي"},
    ]
    selected_genre = Ref[str]()
    search_query = Ref[str]()

    # خانة البحث
    search_field = TextField(
        width=250,
        border_radius=12,
        color=BLACK,
        bgcolor="#FF6F6F",
        hint_text="اسم الفيلم أو المسلسل",
        text_size=16,
        content_padding=padding.only(left=10, right=30),
        border_color=GRAY,
        on_change=lambda e: update_suggestions(e),
        suffix=IconButton(
            icon=Icons.CLEAR,
            icon_color=ACCENT_COLOR,
            on_click=lambda e: clear_search(),
        ),
    )

    # قائمة منسدلة للاقتراحات
    suggestion_dropdown = Dropdown(
        width=155,
        border_radius=12,
        color=BLACK,
        bgcolor="#FF6F6F",
        hint_text="اختر فيلم!",
        text_size=16,
        content_padding=padding.only(left=10, right=10),
        visible=False,  # مخفية افتراضيًا
        on_change=lambda e: select_suggestion(e),
    )

    def update_suggestions(e):
        search_query.current = e.control.value if e.control.value else None
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        titles, _ = get_data(page, content_type, selected_genre.current, search_query.current, for_suggestions=True)
        suggestion_dropdown.options = [flet.dropdown.Option(title) for title in titles[:10]]  # الحد الأقصى 10 اقتراحات
        show_suggestions = bool(search_query.current and titles)
        suggestion_dropdown.visible = show_suggestions
        suggestion_container.visible = show_suggestions  # تحديث رؤية الحاوية
        suggestion_dropdown.update()
        suggestion_container.update()
        main_content.content = create_content_page(page, content_type, selected_genre.current, search_query.current, dropdown)
        page.update()

    def select_suggestion(e):
        search_query.current = e.control.value
        search_field.value = e.control.value
        suggestion_dropdown.visible = False
        suggestion_container.visible = False  # إخفاء الحاوية
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        main_content.content = create_content_page(page, content_type, selected_genre.current, search_query.current, dropdown)
        search_field.update()
        suggestion_dropdown.update()
        page.update()

    def clear_search():
        search_field.value = ""
        search_query.current = None
        suggestion_dropdown.visible = False
        suggestion_container.visible = False  # إخفاء الحاوية
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        main_content.content = create_content_page(page, content_type, selected_genre.current, None, dropdown)
        search_field.update()
        suggestion_dropdown.update()
        suggestion_container.update()
        page.update()

    search_container = Container(
        bgcolor=GRAY2,
        border_radius=12,
        padding=10,
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=Colors.with_opacity(0.2, Colors.BLACK),
            offset=Offset(0, 2),
        ),
        content=search_field,
    )

    suggestion_container = Container(
        bgcolor=GRAY2,
        width=155,  # تصحيح العرض ليتناسب مع suggestion_dropdown
        border_radius=12,
        padding=5,
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=Colors.with_opacity(0.2, Colors.BLACK),
            offset=Offset(0, 2),
        ),
        content=suggestion_dropdown,
        visible=False,  # مخفية افتراضيًا
    )

    dropdown = Dropdown(
        width=200,
        border_radius=12,
        color=BLACK,
        bgcolor="#FF6F6F",
        hint_text="اختر فئة!",
        options=[flet.dropdown.Option(key=opt["key"], text=opt["text"]) for opt in options],
        text_size=16,
        content_padding=padding.only(left=10, right=10),
        value=None,
    )

    def update_content_by_genre(e):
        selected_genre.current = e.control.value if e else None
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        main_content.content = create_content_page(page, content_type, selected_genre.current, search_query.current, dropdown)
        update_button_labels(content_type, b1, b2)
        # تحديث الاقتراحات بناءً على النوع الجديد
        titles, _ = get_data(page, content_type, selected_genre.current, search_query.current, for_suggestions=True)
        suggestion_dropdown.options = [flet.dropdown.Option(title) for title in titles[:10]]
        show_suggestions = bool(search_query.current and titles)
        suggestion_dropdown.visible = show_suggestions
        suggestion_container.visible = show_suggestions  # تحديث رؤية الحاوية
        suggestion_dropdown.update()
        suggestion_container.update()
        page.update()

    dropdown.on_change = update_content_by_genre

    drop_down = Container(
        bgcolor=GRAY2,
        border_radius=12,
        padding=5,
        width=155,
        shadow=BoxShadow(
            spread_radius=1,
            blur_radius=8,
            color=Colors.with_opacity(0.2, Colors.BLACK),
            offset=Offset(0, 2),
        ),
        content=dropdown,
    )

    # الحاوية الرئيسية
    main_content = Container(
        height=300,
        width=320,
        border_radius=16,
        content=create_content_page(page, "movies", dropdown=dropdown),
        alignment=alignment.center,
    )

    # تحديث المحتوى بناءً على شريط التنقل
    def update_content(e):
        content_type = "movies" if e.control.selected_index == 0 else "series"
        main_content.content = create_content_page(page, content_type, selected_genre.current, search_query.current, dropdown)
        update_button_labels(content_type, b1, b2)
        # تحديث الاقتراحات بناءً على النوع الجديد
        titles, _ = get_data(page, content_type, selected_genre.current, search_query.current, for_suggestions=True)
        suggestion_dropdown.options = [flet.dropdown.Option(title) for title in titles[:10]]
        show_suggestions = bool(search_query.current and titles)
        suggestion_dropdown.visible = show_suggestions
        suggestion_container.visible = show_suggestions  # تحديث رؤية الحاوية
        suggestion_dropdown.update()
        suggestion_container.update()
        page.update()

    # Navigation Bar
    nav_bar = CupertinoNavigationBar(
        bgcolor=PURE_RED,
        inactive_color=GRAY,
        active_color=ACCENT_COLOR,
        height=60,
        destinations=[
            NavigationBarDestination(icon=Icons.MOVIE, label="الأفلام"),
            NavigationBarDestination(icon=Icons.TV, label="المسلسلات"),
        ],
        on_change=update_content,
        border=Border(bottom=BorderSide(color=Colors.with_opacity(0.2, Colors.BLACK), width=1)),
    )
    page.navigation_bar = nav_bar

    # زر تحديث العنصر العشوائي
    def refresh_random_item(e):
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        if selected_genre.current or search_query.current:
            main_content.content = create_content_page(page, content_type, selected_genre.current, search_query.current, dropdown)
            page.update()
        else:
            page.snack_bar = SnackBar(
                content=Row(
                    controls=[
                        Icon(Icons.WARNING, color=Colors.WHITE, size=20),
                        Text("يرجى اختيار فئة أو إدخال اسم للبحث!", size=16, color=Colors.WHITE),
                    ],
                    alignment=MainAxisAlignment.CENTER,
                ),
                bgcolor=Colors.RED_700,
                duration=4000,
                show_close_icon=True,
                close_icon_color=Colors.WHITE,
            )
            page.snack_bar.open = True
            page.update()

    b1 = ElevatedButton(
        content=Text("فيلم جديد", size=16, weight=FontWeight.BOLD, color=Colors.WHITE),
        width=150,
        style=ButtonStyle(
            bgcolor=ACCENT_COLOR,
            color=Colors.WHITE,
            padding=15,
            shape=RoundedRectangleBorder(radius=12),
            elevation={"pressed": 2, "": 5},
            animation_duration=300,
        ),
        on_click=refresh_random_item,
    )

    # زر جلب عنصر عشوائي مع إعادة القائمة المنسدلة إلى "الكل" ومسح البحث
    def fetch_random_item(e):
        selected_genre.current = None
        search_query.current = None
        dropdown.value = "All"
        search_field.value = ""
        suggestion_dropdown.visible = False
        suggestion_container.visible = False  # إخفاء الحاوية
        content_type = "movies" if nav_bar.selected_index == 0 else "series"
        main_content.content = create_content_page(page, content_type, dropdown=dropdown)
        update_button_labels(content_type, b1, b2)
        dropdown.update()
        search_field.update()
        suggestion_dropdown.update()
        suggestion_container.update()
        page.update()

    b2 = ElevatedButton(
        content=Text("فيلم عشوائي", size=16, weight=FontWeight.BOLD, color=Colors.WHITE),
        width=150,
        style=ButtonStyle(
            bgcolor=ACCENT_COLOR,
            color=Colors.WHITE,
            padding=15,
            shape=RoundedRectangleBorder(radius=12),
            elevation={"pressed": 2, "": 5},
            animation_duration=300,
        ),
        on_click=fetch_random_item,
    )

    page.add(
        Column(
            [
                Divider(height=5, color=Colors.TRANSPARENT),
                search_container,
                Divider(height=5, color=Colors.TRANSPARENT),
                Row([suggestion_container, drop_down], alignment=MainAxisAlignment.CENTER, spacing=10),
                Divider(height=5, color=Colors.TRANSPARENT),
                main_content,
                Divider(height=5, color=Colors.TRANSPARENT),
                Row([b1, b2], alignment=MainAxisAlignment.CENTER, spacing=10),
            ],
            horizontal_alignment=CrossAxisAlignment.CENTER,
            alignment=MainAxisAlignment.CENTER,
            spacing=10,
        )
    )

app(main)