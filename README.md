🎬 Movie & Series Randomizer | مقترح الأفلام والمسلسلات

A modern desktop application built with Python and Flet that helps you decide what to watch next! It features a sleek UI to browse, search, and randomly select movies and TV series based on genres.

تطبيق سطح مكتب عصري مبني باستخدام بايثون ومكتبة Flet، يساعدك في اختيار ما ستشاهده تالياً! يتميز بواجهة مستخدم أنيقة لتصفح، بحث، واختيار أفلام ومسلسلات عشوائية بناءً على التصنيف.

✨ Features | المميزات

🎲 Random Pick: Get a random movie or series suggestion with a single click.

اختيار عشوائي: احصل على اقتراح عشوائي لفيلم أو مسلسل بضغطة زر.

🔍 Search & Suggestions: Real-time search with auto-complete suggestions.

بحث واقتراحات: بحث فوري مع قائمة اقتراحات تلقائية.

📂 Genre Filtering: Filter content by specific genres (Action, Drama, Comedy, etc.).

تصفية حسب النوع: فلترة المحتوى بناءً على التصنيف (أكشن، دراما، كوميديا، إلخ).

🌗 Modern UI: A responsive interface with a custom dark/red theme.

واجهة عصرية: واجهة متجاوبة مع ثيم مخصص بالألوان الداكنة والأحمر.

💾 Database Integration: Uses SQLite for efficient local data storage.

قاعدة بيانات: يعتمد على SQLite لتخزين البيانات محلياً بكفاءة.

🚀 Installation | التثبيت والتشغيل

Clone the repository | انسخ المستودع

git clone [https://github.com/YourUsername/movie-randomizer.git](https://github.com/YourUsername/movie-randomizer.git)
cd movie-randomizer


Install dependencies | ثبت المكتبات المطلوبة

pip install flet


Run the App | شغل التطبيق

python main.py


🗄️ Database Note | ملاحظة بخصوص قاعدة البيانات

The application automatically creates movies.db and series.db files upon the first run. However, they will be empty initially. You need to populate them with data or use existing database files matching the schema below:

يقوم التطبيق بإنشاء ملفات قواعد البيانات movies.db و series.db تلقائياً عند التشغيل لأول مرة، لكنها ستكون فارغة. تحتاج إلى ملئها بالبيانات لكي يعمل التطبيق بشكل صحيح، مع الالتزام بالبنية التالية:

CREATE TABLE content (
    title TEXT,
    genres TEXT,
    averageRating REAL,
    releaseYear INTEGER
);


🛠️ Built With | تم البناء بواسطة

Python - Programming Language.

Flet - The framework for building the UI.

SQLite3 - Database engine.

🤝 Contributing | المساهمة

Contributions are welcome! Feel free to open issues or submit pull requests.
المساهمات مرحب بها! لا تتردد في فتح Issues أو إرسال Pull Requests.

Developed with ❤️ by Salah Abdeldaim
