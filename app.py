import streamlit as st
import google.generativeai as genai
import textwrap  # For wrapping long text

# --- API Key Setup (Replace with your actual keys) ---
API_KEYS = st.secrets["API_KEYS"]
# --- Helper Functions ---
def call_gemini_api(prompt):
    for api_key in API_KEYS:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-pro")
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
    menu_list = response_text.split("🍽️ เมนูที่")
    menu_list = [menu.strip() for menu in menu_list if menu.strip()]
    if not menu_list:
        menu_list = response_text.split("\n- ")
        menu_list = [menu.strip() for menu in menu_list if menu.strip()]
    if not menu_list:
        menu_list = response_text.split("\n• ")
        menu_list = [menu.strip() for menu in menu_list if menu.strip()]
    return menu_list

# --- Custom CSS ---
st.markdown("""
<style>
/* Global Styles */
body {
    font-family: 'Kanit', sans-serif; /* Modern Thai font */
}

.stApp {
    background-color: #f0f2f6;  /* Light gray background */
    background-image: url("https://www.transparenttextures.com/patterns/subtle-white-feathers.png"); /*Subtle Background Pattern*/

}

/* Header */
.title {
    color: #2c3e50;
    text-align: center;
    padding: 1rem 0;
    font-size: 2.5rem; /* Larger title */
    font-weight: 600;  /* Semi-bold */
}

/* Mode Selection */
.mode-selection {
    margin-bottom: 2rem;
    border-radius: 10px;
    padding: 10px;
    background-color: white;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

/* Input Sections */
.input-section {
    background-color: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
}

/* Input Fields */
.stTextInput, .stSelectbox, .stSlider, .stRadio, .stNumberInput {
    margin-bottom: 10px;
}
.stTextArea>div>div>textarea{
    border-color:#3498db;
}

/* Buttons */
.stButton>button {
    background-color: #3498db; /* Blue */
    color: white;
    border: none;
    border-radius: 20px; /* Rounded buttons */
    padding: 10px 24px;
    font-size: 1.1rem;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow */
    width: 100%; /* Make buttons full width */
}

.stButton>button:hover {
    background-color: #2980b9; /* Darker blue on hover */
    transform: translateY(-2px); /* Slight lift on hover */
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.stButton>button:active {
    transform: translateY(0); /* Reset position on click */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Menu Columns */
.menu-column {
    background-color: white;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease; /* Smooth transition */
    border: 2px solid transparent; /* Add a border */
}

.menu-column:hover {
    transform: scale(1.03); /* Slightly enlarge on hover */
    border-color: #3498db;
}

.menu-column h3 {
    color: #3498db; /* Blue heading */
    margin-bottom: 10px;
    font-size: 1.4rem;
}

.menu-item {
    font-size: 1rem;
    line-height: 1.6;
    color: #4a4a4a; /* Dark gray text */
}

/* Expander */
.st-expanderHeader {
    font-size: 1.2rem;
    font-weight: 500; /* Slightly bolder expander header */
}

/* About Section */
.about-section {
    background-color: #e0e0e0;
    border-radius: 10px;
    padding: 20px;
    margin-top: 20px;
}
.about-section ul {
    list-style: none; /* Remove bullet points */
    padding: 0;

}

.about-section li {
    margin-bottom: .5rem;
}

/* Spinners */
.st-cf {
    color: #3498db !important; /* Make spinners blue */
}

</style>
""", unsafe_allow_html=True)

# --- App UI ---
st.markdown("<h1 class='title'>🍽️ Smart Cooking App 😎</h1>", unsafe_allow_html=True)

with st.container(border=True):
    option = st.radio("🔹 เลือกโหมด:", ["สร้างเมนูจากวัตถุดิบ", "ค้นหาเมนูสำหรับซื้อ"],
                    horizontal=True, key="mode_select")

if option == "สร้างเมนูจากวัตถุดิบ":
    st.subheader("✨ สร้างเมนูแบบกำหนดเอง")

    with st.expander("📝 กรอกวัตถุดิบของคุณ", expanded=True):
        ingredients = st.text_area("วัตถุดิบ (คั่นด้วยจุลภาค):",
                                    placeholder="เช่น ไข่, หมูสับ, ผักกาด...",
                                    height=120)

    with st.expander("⚙️ ปรับแต่งเมนูของคุณ", expanded=False):
        col1, col2 = st.columns(2)
        with col1:
            num_ingredients = st.number_input("จำนวนวัตถุดิบหลัก", min_value=1, max_value=20, value=3, step=1)
            category = st.selectbox("ประเภทอาหาร",
                                    ["อาหารทั่วไป", "มังสวิรัติ", "อาหารคลีน", "อาหารไทย", "อาหารญี่ปุ่น", "อาหารตะวันตก"])
            calories = st.slider("แคลอรี่ที่ต้องการ (kcal)", 100, 1500, 500, step=50)

        with col2:
            difficulty = st.radio("ระดับความยาก", ["ง่าย", "ปานกลาง", "ยาก"], horizontal=True)
            cook_time = st.slider("เวลาทำอาหาร (นาที)", 5, 180, 30, step=5)

    if st.button("🍳 สร้างเมนู", use_container_width=True):
        if ingredients:
            prompt = (f"ฉันมี: {ingredients} ({num_ingredients} วัตถุดิบหลัก) "
                      f"แนะนำเมนู {category} เวลาทำไม่เกิน {cook_time} นาที "
                      f"ประมาณ {calories} kcal ระดับความยาก {difficulty} "
                      f"พร้อมวิธีทำอย่างละเอียด เสนอ 3 ตัวเลือก คั่นด้วย '🍽️ เมนูที่'")
            with st.spinner("กำลังสร้างสรรค์ไอเดียอร่อยๆ..."):
                menu_list = process_menus(call_gemini_api(prompt))

            if menu_list:
                st.subheader("🧑‍🍳 เมนูแนะนำ:")
                cols = st.columns(3)
                for i, menu in enumerate(menu_list[:3]):
                    with cols[i]:
                        st.markdown(f"<div class='menu-column'><h3>🍽️ เมนูที่ {i+1}</h3><p class='menu-item'>{menu}</p></div>", unsafe_allow_html=True)
            else:
                st.warning("⚠️ ไม่พบเมนูที่ตรงกับเกณฑ์ของคุณ โปรดลองปรับการตั้งค่า")
        else:
            st.warning("⚠️ กรุณากรอกวัตถุดิบของคุณ")

elif option == "ค้นหาเมนูสำหรับซื้อ":
    st.subheader("✨ ค้นหาเมนูที่ใช่สำหรับคุณ")

    with st.expander("⚙️ ตั้งค่าการค้นหา", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            country = st.selectbox("ประเทศ", ["ไทย", "ญี่ปุ่น", "เกาหลีใต้", "สหรัฐอเมริกา", "อังกฤษ", "ฝรั่งเศส", "เยอรมนี"])
            category = st.selectbox("ประเภทอาหาร", ["อาหารไทย", "อาหารญี่ปุ่น", "อาหารเกาหลี", "ฟาสต์ฟู้ด", "อาหารสุขภาพ"])
        with col2:
            taste = st.radio("รสชาติ", ["เผ็ด", "หวาน", "เค็ม", "เปรี้ยว"], horizontal=True)
            budget = st.radio("งบประมาณ", ["ต่ำกว่า 100 บาท", "100 - 300 บาท", "มากกว่า 300 บาท"], horizontal=True)

    if st.button("🔎 ค้นหาเมนู", use_container_width=True):
        prompt = (f"ฉันต้องการซื้ออาหาร {category} รสชาติ {taste} งบประมาณ {budget} ใน {country} "
                  f"แนะนำ 3 ตัวเลือกเมนู {category} ที่มีขายใน {country} คั่นด้วย '🍽️ เมนูที่'")

        with st.spinner("กำลังค้นหาตัวเลือกที่ดีที่สุด..."):
            menu_list = process_menus(call_gemini_api(prompt))

        if menu_list:
            st.subheader("🧑‍🍳 เมนูแนะนำ:")
            cols = st.columns(3)
            for i, menu in enumerate(menu_list[:3]):
                with cols[i]:
                     st.markdown(f"<div class='menu-column'><h3>🍽️ เมนูที่ {i+1}</h3><p class='menu-item'>{menu}</p></div>", unsafe_allow_html=True)
        else:
            st.warning("⚠️ ไม่พบเมนู โปรดลองอีกครั้ง")

# --- About Section ---
st.markdown("---")
if st.button("📜 เกี่ยวกับผู้พัฒนา", use_container_width=True):
    with st.expander("🤝 พบกับทีมงาน"):
        st.markdown("""
        <div class='about-section'>
        <ul>
        <li><strong>1. นาย กัลปพฤกษ์ วิเชียรรัตน์</strong> - <em>ชั้น 6/13 เลขที่ 3(คนแบกครับอิๆ)</em></li>
        <li><strong>2. นาย ธีราธร มุกดาเพชรรัตน์</strong> - <em>ชั้น 6/13 เลขที่ 13</em></li>
        <li><strong>3. นาย อภิวิชญ์ อดุลธรรมวิทย์</strong> - <em>ชั้น 6/13 เลขที่ 28</em></li>
        <li><strong>4. นาย ปัณณวิชญ์ หลีกภัย</strong> - <em>ชั้น 6/13 เลขที่ 29</em></li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
