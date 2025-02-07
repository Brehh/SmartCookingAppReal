import streamlit as st
import google.generativeai as genai
import textwrap

# --- API Key Setup (From Streamlit Secrets) ---
API_KEYS = st.secrets["API_KEYS"]


# --- Page Configuration ---
st.set_page_config(
    page_title="🍽️ Smart Cooking App 😎",
    page_icon="🍳",  # Changed page icon to a frying pan
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Helper Functions ---
def call_gemini_api(prompt):
    for api_key in API_KEYS:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
            response = model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            error_message = str(e)
            if "insufficient_quota" in error_message or "Quota exceeded" in error_message:
                continue
            else:
                return f"❌ เกิดข้อผิดพลาด: {error_message}"
    return "⚠️ API ทั้งหมดหมดโควต้าแล้ว กรุณาตรวจสอบบัญชีของคุณ"

def process_menus(response_text):
    menu_list = []
    separators = ["🍽️ เมนูที่", "\n- ", "\n• ", "\n— ", "- ", "• "]
    for sep in separators:
        if sep in response_text:
            menu_list = response_text.split(sep)
            break
    else:
        return [response_text.strip()]

    menu_list = [menu.strip() for menu in menu_list if menu.strip()]
    return menu_list

# --- Custom CSS ---
st.markdown("""
<style>
/* Global Styles */
body {
    font-family: 'Kanit', sans-serif;
}

.stApp {
    /* Default Streamlit background */
}

/* Main Container Styles */
.main-container {
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    padding: 30px;
    margin-bottom: 20px;
    border: 2px solid #e0e0e0;
}

/* Header */
.title {
    color: #343a40;
    text-align: center;
    padding: 1rem 0;
    font-size: 3rem;
    font-weight: 700;
    margin-bottom: 1rem;
}

/* Mode Selection Buttons - Using st.buttons */
.mode-buttons {
    display: flex;
    justify-content: center;
    gap: 20px; /* Spacing between buttons */
    margin-bottom: 30px;
}

.mode-button {
    background-color: #007bff; /* Blue */
    color: white;
    border: none;
    border-radius: 8px; /* Rounded */
    padding: 15px 30px; /* Larger padding */
    font-size: 1.4rem;  /* Larger font */
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}

.mode-button:hover {
    background-color: #0056b3; /* Darker blue on hover */
    transform: translateY(-2px);
}

.mode-button-selected {
    background-color: #28a745; /* Green - for the selected mode */
    color: white;
    border: none;
    border-radius: 8px;
    padding: 15px 30px;
    font-size: 1.4rem;
    font-weight: bold;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 2px 5px rgba(0,0,0,0.2);
}
.mode-button-selected:hover {
    background-color: #1e7e34;
    transform: translateY(-2px);
}
/* Subheaders */
.st-expanderHeader {
    font-size: 1.6rem; /* Even larger */
    font-weight: 700;
    margin-bottom: 0.5rem;
}

/* Input Sections */
.input-section {
    margin-bottom: 1rem;
}

/* Input Fields */
.stTextInput, .stSelectbox, .stSlider, .stRadio, .stNumberInput {
    margin-bottom: 0.8rem;
}

/* Text Area */
.stTextArea>div>div>textarea{
    border-color:#3498db;
    border-radius: 8px;
}

/* Buttons */
.stButton>button {
    background-color: #28a745;
    color: white;
    border: none;
    border-radius: 25px;
    padding: 12px 28px;
    font-size: 1.2rem;
    transition: all 0.3s ease;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
    width: 100%;
}

.stButton>button:hover {
    background-color: #218838;
    transform: translateY(-3px);
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.stButton>button:active {
    transform: translateY(0);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

/* Menu Columns */
.menu-column {
    border-radius: 12px;
    padding: 25px;
    margin-bottom: 15px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
    border: 1px solid #dee2e6;
}

.menu-column:hover {
    transform: scale(1.02);
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);
}

.menu-column h3 {
    color: #28a745;
    margin-bottom: 12px;
    font-size: 1.5rem;
    font-weight: 600;
}

.menu-item {
    font-size: 1.05rem;
    line-height: 1.7;
}

/* About Section */
.about-section {
    border-radius: 12px;
    padding: 25px;
    margin-top: 30px;
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
    border: 1px solid #dee2e6;
}
.about-section ul {
    list-style: none;
    padding: 0;
}

.about-section li {
    margin-bottom: 0.6rem;
}

/* Spinners */
.st-cf {
    color: #28a745 !important;
}

/* Larger and Bolder Expander Text */
.st-expander button[data-baseweb="button"] {
    font-size: 1.4rem !important; /* Larger font */
    font-weight: bold !important;   /* Bold text */
}

/* Change expander icons */
.st-expander svg {
    color: #007bff; /* Blue expander icon */
}

</style>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown("<h1 class='title'>🍽️ Smart Cooking App 😎</h1>", unsafe_allow_html=True)

with st.container(border=True):
    # --- Mode Selection (Using Buttons) ---
    col1, col2 = st.columns(2)  # Use columns for side-by-side buttons
    with col1:
        if st.button("📝 สร้างเมนูทำกินเอง 👨‍🍳", key="create_mode", type='primary' if 'mode' not in st.session_state or st.session_state.mode == "create" else 'secondary'):
            st.session_state.mode = "create"  # Store the selected mode
    with col2:
        if st.button("🔍 ค้นหาเมนูที่จะซื้อกิน 😎", key="search_mode",  type='primary' if 'mode' in st.session_state and st.session_state.mode == "search" else 'secondary'):
            st.session_state.mode = "search"

    # --- Conditional Display based on Selected Mode ---
    if 'mode' not in st.session_state or st.session_state.mode == "create":
        st.subheader("✨ สร้างเมนูแบบกำหนดเอง")

        with st.expander("📝 กรอกวัตถุดิบหลัก", expanded=True):
            ingredients = st.text_area("วัตถุดิบหลัก (คั่นด้วยจุลภาค):",
                                       placeholder="เช่น ไข่, หมูสับ, ผักกาด...",
                                       height=120, label_visibility="collapsed")

        with st.expander("⚙️ ปรับแต่งเมนู", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("ประเภทอาหาร",st.secrets['foodtype1'])
                calories = st.slider("แคลอรี่ที่ต้องการ (kcal)", 100, 1500, 500, step=50)

            with col2:
                difficulty = st.radio("ระดับความยาก", ["ง่าย", "ปานกลาง", "ยาก", 'ยากมาก', 'นรก'], horizontal=True)
                cook_time = st.slider("เวลาทำอาหาร (นาที)", 5, 180, 30, step=5)

        if st.button("🍳 สร้างเมนู", use_container_width=True):
            if ingredients:
                prompt = (f"ฉันมี: {ingredients} เป็นวัตถุดิบหลัก "
                          f"แนะนำเมนู {category} เวลาทำไม่เกิน {cook_time} นาที "
                          f"ประมาณ {calories} kcal ระดับความยาก ระดับ{difficulty} "
                          f"พร้อมวิธีทำอย่างละเอียด เสนอ 3 ตัวเลือก คั่นด้วย '🍽️ เมนูที่' ไม่ต้องเกริ่นนำ")
                with st.spinner("กำลังสร้างสรรค์ไอเดียอร่อยๆ... 3 เมนู"):
                    menu_list = process_menus(call_gemini_api(prompt))

                if menu_list:
                    st.subheader("🧑‍🍳 เมนูแนะนำ 3 เมนู:")
                    cols = st.columns(3)
                    for i, menu in enumerate(menu_list[:3]):
                        with cols[i]:
                            st.markdown(
                                f"<div class='menu-column'><h3>🍽️ เมนูที่ {i + 1}</h3><p class='menu-item'>{menu}</p></div>",
                                unsafe_allow_html=True)
                else:
                    st.warning("⚠️ ไม่พบเมนูที่ตรงกับเกณฑ์ของคุณ โปรดลองปรับการตั้งค่า")
            else:
                st.warning("⚠️ กรุณากรอกวัตถุดิบของคุณ")

    elif st.session_state.mode == "search":
        st.subheader("✨ ค้นหาเมนูที่ใช่สำหรับคุณ 3 เมนู")

        with st.expander("⚙️ ตั้งค่าการค้นหา", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox('ประเทศที่คุณอยู่ในตอนนี้', st.secrets['country1'])
                category = st.selectbox("ประเภทอาหาร",st.secrets['foodtype2'])
            with col2:
                taste = st.radio("รสชาติ", ["เผ็ด", "หวาน", "เค็ม", "เปรี้ยว", "ขม", "อูมามิ", "มัน", "ฝาด", "จืด", 'รสจัด',
                                            'กลมกล่อม', 'กลางๆ'], horizontal=True)
                budget = st.radio("งบประมาณ", ['ต่ำกว่า 100 บาท', '100 - 300 บาท', '300 - 1,000 บาท', 'ไม่จำกัดงบ (มีงบระดับ Mr Beast)'], horizontal=True)

        if st.button("🔎 ค้นหาเมนู", use_container_width=True):
            prompt = (f"ฉันต้องการซื้ออาหาร {category} รสชาติ {taste} งบประมาณ {budget} ใน {country} "
                      f"แนะนำ 3 ตัวเลือกเมนู {category} ที่มีขายใน {country} คั่นด้วย '🍽️ เมนูที่' ไม่ต้องเกริ่นนำ และบอกราคาของอาหารนั้นๆด้วย")

            with st.spinner("กำลังค้นหาตัวเลือกที่ดีที่สุด... 3 เมนู"):
                menu_list = process_menus(call_gemini_api(prompt))

            if menu_list:
                st.subheader("🧑‍🍳 เมนูแนะนำ 3 เมนู:")
                cols = st.columns(3)
                for i, menu in enumerate(menu_list[:3]):
                    with cols[i]:
                        st.markdown(
                            f"<div class='menu-column'><h3>🍽️ เมนูที่ {i + 1}</h3><p class='menu-item'>{menu}</p></div>",
                            unsafe_allow_html=True)
            else:
                st.warning("⚠️ ไม่พบเมนู โปรดลองอีกครั้ง")

# --- About Section ---
st.markdown("---")
if st.button("📜 เกี่ยวกับผู้พัฒนา", use_container_width=True):
    with st.expander("🤝 พบกับทีมงาน", expanded=False):
        st.markdown("""
        <div class='about-section'>
        <ul style='list-style: none; padding: 0; display: flex; flex-direction: column; align-items: center;'>

        <li style='font-size: 1.6rem; font-weight: bold; margin-top: 10px;'>นาย กัลปพฤกษ์ วิเชียรรัตน์ (คนแบกอิๆๆ😎)</li>
        <li style='font-size: 1.3rem;'><em>ชั้น 6/13 เลขที่ 3</em></li>
        <img src='https://media.istockphoto.com/id/176799603/photo/3-4-profile-portrait.jpg?s=612x612&w=0&k=20&c=ArfYQTh-m4PGKwNyWypZWl6Q918m71g6aj5y8s4k1bA=' width='250px' style='border-radius: 50%; margin-bottom: 20px;'>

        <li style='font-size: 1.6rem; font-weight: bold; margin-top: 10px;'>นาย ธีราธร มุกดาเพชรรัตน์</li>
        <li style='font-size: 1.3rem;'><em>ชั้น 6/13 เลขที่ 13</em></li>
        <img src='https://media.istockphoto.com/id/176799603/photo/3-4-profile-portrait.jpg?s=612x612&w=0&k=20&c=ArfYQTh-m4PGKwNyWypZWl6Q918m71g6aj5y8s4k1bA=' width='250px' style='border-radius: 50%; margin-bottom: 20px;'>

        <li style='font-size: 1.6rem; font-weight: bold; margin-top: 10px;'>นาย อภิวิชญ์ อดุลธรรมวิทย์</li>
        <li style='font-size: 1.3rem;'><em>ชั้น 6/13 เลขที่ 28</em></li>
        <img src='https://media.istockphoto.com/id/176799603/photo/3-4-profile-portrait.jpg?s=612x612&w=0&k=20&c=ArfYQTh-m4PGKwNyWypZWl6Q918m71g6aj5y8s4k1bA=' width='250px' style='border-radius: 50%; margin-bottom: 20px;'>

        <li style='font-size: 1.6rem; font-weight: bold; margin-top: 10px;'>นาย ปัณณวิชญ์ หลีกภัย</li>
        <li style='font-size: 1.3rem;'><em>ชั้น 6/13 เลขที่ 29</em></li>
        <img src='https://media.istockphoto.com/id/176799603/photo/3-4-profile-portrait.jpg?s=612x612&w=0&k=20&c=ArfYQTh-m4PGKwNyWypZWl6Q918m71g6aj5y8s4k1bA=' width='250px' style='border-radius: 50%;'>
        </ul>
        </div>
        """, unsafe_allow_html=True)
