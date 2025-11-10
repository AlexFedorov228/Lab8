import re
from enum import Enum, auto

# --- Рівень 1: Регулярні вирази ---
# [cite: 4]

def task_level_1(filename="level1_input.txt"):
    """
    Виконує завдання першого рівня:
    1. Описує регулярний вираз[cite: 7].
    2. Знаходить у файлі слова, що відповідають виразу[cite: 8].
    """
    print("--- Рівень 1 ---")
    
    # Варіант 15 (Таблиця 8.1):
    # Слово починається з '[', далі '+' або '-',
    # потім послідовність '0-9' АБО 'A-Z',
    # і закінчується ']'. [cite: 45]
    
    # ^ - початок рядка
    # \[ - символ '['
    # (\+|-) - один символ: '+' або '-'
    # ([0-9]+|[A-Z]+) - одна або більше цифр АБО одна або більше великих літер
    # \] - символ ']'
    # $ - кінець рядка
    regex_l1 = r"^\[(\+|-)([0-9]+|[A-Z]+)\]$"
    
    print(f"Регулярний вираз: {regex_l1}\n")
    print(f"Результати перевірки файлу '{filename}':")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                word = line.strip() # Прибираємо зайві пробіли і \n
                if not word:
                    continue
                    
                if re.match(regex_l1, word):
                    print(f"  '{word}' -> Знайдено відповідність")
                else:
                    print(f"  '{word}' -> НЕ відповідає")
                    
    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
    print("-" * 20 + "\n")


# --- Рівень 2 і 3: Скінченний автомат ---

# Варіант 15 (Таблиця 8.2):
# Регулярний вираз: \$([A-F]+||d)*\W+ [cite: 47]
#
# *АНАЛІЗ*: Вираз [cite: 47] '||d' виглядає як помилка друку.
# Найбільш імовірна інтерпретація: \$([A-F]+|\d)*\W+
#
# Опис:
# \$ - Починається з символу '$'
# ( ... )* - Група, що може повторюватись 0 або більше разів
# [A-F]+ - Послідовність (1+) літер від A до F
# | - АБО
# \d - Одна цифра
# \W+ - Послідовність (1+) "не-літерно-цифрових" символів (наприклад, %, _, ., $ і т.д.)

# Набір станів скінченного автомату (згідно рекомендацій) [cite: 26]
class State(Enum):
    S0 = auto() # Початковий стан
    S1 = auto() # Стан після '$' (очікуємо A-F, \d або \W)
    S2 = auto() # Стан всередині послідовності [A-F]+
    S3 = auto() # Фінальний стан (всередині \W+)
    SF = auto() # Стан помилки (Fail)

# --- Рівень 2: Реалізація через 'switch' (if/elif) ---
# [cite: 10]

def parse_level_2(text: str) -> bool:
    """
    Описує синтаксичний аналізатор на основі скінченного автомата,
    реалізованого за допомогою 'switch' (if/elif/else в Python). [cite: 12]
    """
    
    # Граф скінченного автомату (для звіту)[cite: 11]:
    # 
    # (S0) --'$'--> (S1)
    #
    # (S1) --'\d'--> (S1)
    # (S1) --'[A-F]'--> (S2)
    # (S1) --'\W'--> [S3] (де \W не '$')
    # (S1) --'$'--> [S3]
    #
    # (S2) --'[A-F]'--> (S2)
    # (S2) --'\d'--> (S1)
    # (S2) --'\W'--> [S3] (де \W не '$')
    # (S2) --'$'--> [S3]
    #
    # [S3] --'\W'--> [S3]
    #
    # Будь-який інший символ з будь-якого стану веде в (SF).
    # [S3] - фінальний стан.
    
    current_state = State.S0
    
    for char in text:
        # Емуляція 'switch' по поточному стану
        if current_state == State.S0:
            if char == '$':
                current_state = State.S1
            else:
                current_state = State.SF # Не '$' на початку - помилка
        
        elif current_state == State.S1:
            if char.isdigit():
                current_state = State.S1
            elif 'A' <= char <= 'F':
                current_state = State.S2
            elif not char.isalnum(): # \W (будь-який не-alpha-numeric)
                current_state = State.S3
            else:
                current_state = State.SF # Інші символи (a-z, G-Z і т.д.)
        
        elif current_state == State.S2:
            if 'A' <= char <= 'F':
                current_state = State.S2
            elif char.isdigit():
                current_state = State.S1
            elif not char.isalnum(): # \W
                current_state = State.S3
            else:
                current_state = State.SF

        elif current_state == State.S3:
            if not char.isalnum(): # \W
                current_state = State.S3
            else:
                current_state = State.SF # Почався буквенно-цифровий символ
        
        elif current_state == State.SF:
            break # Якщо ми в стані помилки, далі перевіряти немає сенсу
            
    # Слово правильне, ТІЛЬКИ ЯКЩО автомат завершив роботу
    # у фінальному стані (S3).
    return current_state == State.S3

def task_level_2():
    """
    Виконує завдання другого рівня:
    1. Вводить рядок з клавіатури[cite: 13].
    2. Визначає його правильність[cite: 14].
    """
    print("--- Рівень 2 ---")
    print(f"Перевірка автомату (реалізація 'switch'). Введіть рядок:")
    text = input("Ваш рядок: ")
    
    if parse_level_2(text):
        print("Результат: Рядок ПРАВИЛЬНИЙ (відповідає автомату).")
    else:
        print("Результат: Рядок НЕПРАВИЛЬНИЙ.")
    print("-" * 20 + "\n")


# --- Рівень 3: Реалізація через таблицю переходів ---
# [cite: 15]

# Категорії символів для таблиці
class CharCategory(Enum):
    DOLLAR = auto()
    DIGIT = auto()
    HEX_AF = auto()
    NON_ALNUM = auto() # \W
    OTHER = auto()

def get_char_category(char: str) -> CharCategory:
    """Визначає категорію символу для таблиці переходів."""
    if char == '$':
        return CharCategory.DOLLAR
    if char.isdigit():
        return CharCategory.DIGIT
    if 'A' <= char <= 'F':
        return CharCategory.HEX_AF
    if not char.isalnum():
        return CharCategory.NON_ALNUM
    return CharCategory.OTHER # Все інше (a-z, G-Z і т.д.)

# Таблиця переходів скінченного автомату [cite: 18, 27]
# Структура: { Поточний_Стан: { Категорія_Символу: Наступний_Стан, ... }, ... }
transition_table = {
    State.S0: {
        CharCategory.DOLLAR: State.S1,
        # Все інше веде в SF (стан помилки)
    },
    State.S1: {
        CharCategory.DIGIT: State.S1,
        CharCategory.HEX_AF: State.S2,
        CharCategory.DOLLAR: State.S3, # $ - це \W
        CharCategory.NON_ALNUM: State.S3,
    },
    State.S2: {
        CharCategory.HEX_AF: State.S2,
        CharCategory.DIGIT: State.S1,
        CharCategory.DOLLAR: State.S3, # $ - це \W
        CharCategory.NON_ALNUM: State.S3,
    },
    State.S3: {
        CharCategory.DOLLAR: State.S3, # $ - це \W
        CharCategory.NON_ALNUM: State.S3,
    }
}

def parse_level_3(text: str) -> bool:
    """
    Описує синтаксичний аналізатор на основі скінченного автомата,
    реалізованого через таблицю переходів. [cite: 19]
    """
    current_state = State.S0
    
    # Використовуємо цикл for, як вимагає завдання [cite: 19]
    for char in text:
        category = get_char_category(char)
        
        # Шукаємо наступний стан у таблиці.
        # .get(category, State.SF) означає:
        # "спробуй взяти ключ 'category', а якщо його немає, поверни State.SF"
        current_state = transition_table.get(current_state, {}).get(category, State.SF)

        if current_state == State.SF:
            break
            
    # Слово правильне, тільки якщо ми у фінальному стані S3
    return current_state == State.S3
    

def task_level_3(filename="level3_input.txt"):
    """
    Виконує завдання третього рівня:
    1. Читає текст з файлу[cite: 20].
    2. Розділяє його на слова за допомогою регулярного виразу[cite: 20].
    3. Визначає правильність слів аналізатором на основі таблиці[cite: 21].
    """
    print("--- Рівень 3 ---")
    
    # Варіант 15 (Таблиця 8.3):
    # Роздільники: « » (пробіл), «,», «.» [cite: 50]
    # Регулярний вираз для розділення: шукаємо 1 або більше роздільників
    delimiters_regex = r"[ ,.]+"
    
    print(f"Регулярний вираз для роздільників: {delimiters_regex}")
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        print(f"\nВміст файлу '{filename}':\n{content}")
        
        # Розділяємо текст на слова
        words = re.split(delimiters_regex, content)
        
        print("Результати перевірки слів (реалізація через таблицю):")
        
        for word in words:
            if not word: # re.split може дати пусті рядки
                continue
                
            if parse_level_3(word):
                print(f"  '{word}' -> ПРАВИЛЬНО")
            else:
                print(f"  '{word}' -> НЕПРАВИЛЬНО")

    except FileNotFoundError:
        print(f"Помилка: Файл '{filename}' не знайдено.")
    print("-" * 20 + "\n")


# --- Головна функція для запуску ---

if __name__ == "__main__":
    print("=== Лабораторна робота 2.2 (Варіант 15) ===\n")
    
    # Запуск Рівня 1
    task_level_1()
    
    # Запуск Рівня 3
    task_level_3()
    
    # Запуск Рівня 2 (інтерактивний)
    task_level_2()
    
    print("=== Роботу завершено ===\n")