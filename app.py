import streamlit as st
import pandas as pd
import json

# 128 суждений Лири
QUESTIONS = [
    "Другие думают о нем благосклонно", "Производит впечатление на окружающих", "Умеет распоряжаться, приказывать", "Умеет настоять на своем",
    "Обладает чувством достоинства", "Независимый", "Способен сам позаботиться о себе", "Может проявлять безразличие",
    "Способен быть суровым", "Строгий, но справедливый", "Может быть искренним", "Критичен к другим",
    "Любит поплакаться", "Часто печален", "Способен проявлять недоверие", "Часто разочаровывается",
    "Способен быть критичным к себе", "Способен признать свою неправоту", "Охотно подчиняется", "Уступчивый",
    "Благодарный", "Восхищающийся, склонный к подражанию", "Уважительный", "Ищущий одобрения",
    "Способный к сотрудничеству, взаимопомощи", "Стремится ужиться с другими", "Дружелюбный, доброжелательный", "Внимательный, ласковый",
    "Деликатный", "Ободряющий", "Отзывчивый на призывы о помощи", "Бескорыстный",
    "Способен вызывать восхищение", "Пользуется у других уважением", "Обладает талантом руководителя", "Любит ответственность",
    "Уверен в себе", "Самоуверен, напорист", "Деловитый, практичный", "Любит соревноваться",
    "Стойкий и упорный, где надо", "Неумолимый, но беспристрастный", "Раздражительный", "Открытый, прямолинейный",
    "Не терпит, чтобы им командовали", "Скептичен", "На него трудно произвести впечатление", "Обидчивый, щепетильный",
    "Легко смущается", "Неуверенный в себе", "Уступчивый", "Скромный",
    "Часто прибегает к помощи других", "Очень почитает авторитеты", "Охотно принимает советы", "Доверчив и стремится радовать других",
    "Всегда любезен в обхождении", "Дорожит мнением окружающих", "Общительный, уживчивый", "Добросердечный",
    "Добрый, вселяющий уверенность", "Нежный, мягкосердечный", "Любит заботиться о других", "Бескорыстный, щедрый",
    "Любит давать советы", "Производит впечатление значительного человека", "Начальственно повелительный", "Властный",
    "Хвастливый", "Надменный и самодовольный", "Думает только о себе", "Хитрый, расчетливый",
    "Нетерпим к ошибкам других", "Корыстный", "Откровенный", "Часто недружелюбен",
    "Озлобленный", "Жалобщик", "Ревнивый", "Долго помнит свои обиды",
    "Самобичующийся", "Застенчивый", "Безынициативный", "Кроткий",
    "Зависимый, несамостоятельный", "Любит подчиняться", "Предоставляет другим принимать решения", "Легко попадает впросак",
    "Легко поддается влиянию друзей", "Готов довериться любому", "Благорасположен ко всем без разбора", "Всем симпатизирует",
    "Прощает все", "Переполнен чрезмерным сочувствием", "Великодушен, терпим к недостаткам", "Стремится покровительствовать",
    "Стремится к успеху", "Ожидает восхищения от каждого", "Распоряжается другими", "Деспотичный",
    "Сноб, судит о людях лишь по рангу и достатку", "Тщеславный", "Эгоистичный", "Холодный, черствый",
    "Язвительный, насмешливый", "Злой, жестокий", "Часто гневлив", "Бесчувственный, равнодушный",
    "Злопамятный", "Проникнут духом противоречия", "Упрямый", "Недоверчивый, подозрительный",
    "Робкий", "Стыдливый", "Отличается чрезмерной готовностью подчиняться", "Мягкотелый",
    "Почти никогда никому не возражает", "Навязчивый", "Любит, чтобы его опекали", "Чрезмерно доверчив",
    "Стремится сыскать расположение каждого", "Со всеми соглашается", "Всегда дружелюбен", "Любит всех",
    "Слишком снисходителен к окружающим", "Старается утешить каждого", "Заботится о других в ущерб себе", "Портит людей чрезмерной добротой"
]

OCTANTS = {
    "I. Авторитарный": [1, 2, 3, 4, 33, 34, 35, 36, 65, 66, 67, 68, 97, 98, 99, 100],
    "II. Эгоистичный": [5, 6, 7, 8, 37, 38, 39, 40, 69, 70, 71, 72, 101, 102, 103, 104],
    "III. Агрессивный": [9, 10, 11, 12, 41, 42, 43, 44, 73, 74, 75, 76, 105, 106, 107, 108],
    "IV. Подозрительный": [13, 14, 15, 16, 45, 46, 47, 48, 77, 78, 79, 80, 109, 110, 111, 112],
    "V. Подчиняемый": [17, 18, 19, 20, 49, 50, 51, 52, 81, 82, 83, 84, 113, 114, 115, 116],
    "VI. Зависимый": [21, 22, 23, 24, 53, 54, 55, 56, 85, 86, 87, 88, 117, 118, 119, 120],
    "VII. Дружелюбный": [25, 26, 27, 28, 57, 58, 59, 60, 89, 90, 91, 92, 121, 122, 123, 124],
    "VIII. Альтруистичный": [29, 30, 31, 32, 61, 62, 63, 64, 93, 94, 95, 96, 125, 126, 127, 128]
}

# Настраиваем конфигурацию страницы: открываем боковое меню сразу
st.set_page_config(
    page_title="Тест Лири (ДМО) — Онлайн", 
    page_icon="🧠", 
    layout="centered",
    initial_sidebar_state="expanded"
)

# Инициализация сессии
if "started" not in st.session_state:
    st.session_state.started = False
if "names" not in st.session_state:
    st.session_state.names = []
if "q_index" not in st.session_state:
    st.session_state.q_index = 0
if "p_index" not in st.session_state:
    st.session_state.p_index = 0
if "sub_mode" not in st.session_state:
    st.session_state.sub_mode = "real"
if "answers" not in st.session_state:
    st.session_state.answers = {}

# Вспомогательная функция для формирования файла бекапа
def get_backup_json():
    data = {
        "names": st.session_state.names,
        "q_index": st.session_state.q_index,
        "p_index": st.session_state.p_index,
        "sub_mode": st.session_state.sub_mode,
        "answers": st.session_state.answers
    }
    return json.dumps(data, ensure_ascii=False, indent=4)

# --- БОКОВАЯ ПАНЕЛЬ (SIDEBAR) ---
with st.sidebar:
    st.header("⚙️ Меню и бекап")
    if st.session_state.started:
        st.success("🟢 Тестирование идет")
        st.write(f"Участников: {len(st.session_state.names)}")
        st.markdown("---")
        st.subheader("💾 Быстрое сохранение")
        st.download_button(
            label="💾 Скачать бекап (.json)",
            data=get_backup_json(),
            file_name="leary_backup.json",
            mime="application/json",
            use_container_width=True
        )
    else:
        st.info("⚪ Тест не начат")

    st.markdown("---")
    st.caption("Разработано для группового тестирования по методике ДМО Т. Лири.")

# --- ОСНОВНОЙ ИНТЕРФЕЙС ---
st.title("🧠 ДМО Т. Лири (Реальный / Идеальный образ)")

if not st.session_state.started:
    # Используем удобные вкладки на главном экране
    tab_new, tab_restore = st.tabs(["🆕 Начать новый тест", "📂 Загрузить сохранение (.json)"])

    with tab_new:
        st.markdown("Введите список участников (каждое имя на новой строке):")
        default_text = "Я (Самооценка)\nИван\nМария"
        names_input = st.text_area("Список участников", value=default_text, height=150)
        
        if st.button("Начать тестирование ▶", type="primary", use_container_width=True):
            lines = [n.strip() for n in names_input.split("\n") if n.strip()]
            if lines:
                st.session_state.names = lines
                st.session_state.answers = {
                    name: {
                        "real": [False] * len(QUESTIONS),
                        "ideal": [False] * len(QUESTIONS)
                    } for name in lines
                }
                st.session_state.q_index = 0
                st.session_state.p_index = 0
                st.session_state.sub_mode = "real"
                st.session_state.started = True
                st.rerun()
            else:
                st.warning("Введите хотя бы одно имя!")

    with tab_restore:
        st.markdown("Если вы ранее сохраняли прогресс теста, загрузите файл **`leary_backup.json`**:")
        uploaded_backup = st.file_uploader("Выберите файл бекапа", type=["json"], key="start_page_uploader")
        if uploaded_backup is not None:
            try:
                b_data = json.load(uploaded_backup)
                st.session_state.names = b_data["names"]
                st.session_state.q_index = b_data["q_index"]
                st.session_state.p_index = b_data["p_index"]
                st.session_state.sub_mode = b_data["sub_mode"]
                st.session_state.answers = b_data["answers"]
                st.session_state.started = True
                st.success("Прогресс успешно восстановлен!")
                st.rerun()
            except Exception as e:
                st.error(f"Ошибка чтения файла: {e}")

else:
    total_q = len(QUESTIONS)
    total_p = len(st.session_state.names)
    q_idx = st.session_state.q_index
    p_idx = st.session_state.p_index
    mode = st.session_state.sub_mode

    if p_idx >= total_p:
        st.success("🎉 Тестирование успешно завершено!")
        
        results = []
        for name in st.session_state.names:
            for type_key, type_label in [("real", "Реальный"), ("ideal", "Идеальный")]:
                ans_list = st.session_state.answers[name][type_key]
                scores = {}
                for oct_name, q_indices in OCTANTS.items():
                    scores[oct_name] = sum(1 for q_num in q_indices if ans_list[q_num - 1])
                
                i = scores["I. Авторитарный"]
                ii = scores["II. Эгоистичный"]
                iii = scores["III. Агрессивный"]
                iv = scores["IV. Подозрительный"]
                v = scores["V. Подчиняемый"]
                vi = scores["VI. Зависимый"]
                vii = scores["VII. Дружелюбный"]
                viii = scores["VIII. Альтруистичный"]
                
                dom = (i - v) + 0.7 * (ii + viii - iv - vi)
                frd = (vii - iii) + 0.7 * (viii + vi - ii - iv)
                
                results.append({
                    "Имя": f"{name} ({type_label})",
                    **scores,
                    "Доминирование (V)": round(dom, 2),
                    "Дружелюбие (G)": round(frd, 2)
                })
        
        df = pd.DataFrame(results)
        st.dataframe(df)

        csv_data = df.to_csv(sep=";", index=False).encode("utf-8-sig")
        st.download_button(
            label="📥 Скачать результаты (CSV для Excel)",
            data=csv_data,
            file_name="leary_real_ideal_results.csv",
            mime="text/csv",
            type="primary",
            use_container_width=True
        )

        if st.button("Пройти заново", use_container_width=True):
            st.session_state.started = False
            st.rerun()
    else:
        current_question = QUESTIONS[q_idx]
        current_person = st.session_state.names[p_idx]

        if mode == "real":
            st.markdown("### 🟢 Оценка: РЕАЛЬНЫЙ ОБРАЗ (каков человек сейчас)")
        else:
            st.markdown("### 🔵 Оценка: ИДЕАЛЬНЫЙ ОБРАЗ (каким вы хотите его видеть)")

        st.progress((q_idx + 1) / total_q, text=f"Вопрос {q_idx + 1} из {total_q}")
        st.text(f"Участник: {p_idx + 1} из {total_p} ({current_person})")

        st.info(f"👉 **«{current_question}»**")

        col1, col2 = st.columns(2)
        
        def save_ans(val):
            st.session_state.answers[current_person][mode][q_idx] = val
            
            if mode == "real":
                st.session_state.sub_mode = "ideal"
            else:
                st.session_state.sub_mode = "real"
                st.session_state.q_index += 1
                if st.session_state.q_index >= total_q:
                    st.session_state.q_index = 0
                    st.session_state.p_index += 1
            st.rerun()

        with col1:
            if st.button("❌ НЕТ (-)", use_container_width=True):
                save_ans(False)
        with col2:
            if st.button("✅ ДА (+)", use_container_width=True, type="primary"):
                save_ans(True)

        # Яркий блок прямо на главном экране для быстрого сохранения
        st.markdown("---")
        with st.expander("💾 Нужна пауза? Сохранить текущий прогресс"):
            st.write("Нажмите кнопку ниже, чтобы скачать файл `leary_backup.json`. Позже вы сможете загрузить его на стартовом экране и продолжить с этого места.")
            st.download_button(
                label="💾 Скачать промежуточный прогресс (.json)",
                data=get_backup_json(),
                file_name="leary_backup.json",
                mime="application/json",
                use_container_width=True
            )
