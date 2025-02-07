import streamlit as st
import google.generativeai as genai
import textwrap  # For wrapping long text

# --- API Key Setup (From Streamlit Secrets) ---
API_KEYS = st.secrets["API_KEYS"]

# --- Page Configuration ---
st.set_page_config(
    page_title="🍽️ Smart Cooking App 😎",
    page_icon="🍽️",
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
    # More robust menu splitting, handles variations and edge cases
    menu_list = []
    separators = ["🍽️ เมนูที่", "\n- ", "\n• ", "\n— ", "- ", "• "]  # Added more separators
    for sep in separators:
        if sep in response_text:
            menu_list = response_text.split(sep)
            break  # Stop at the first successful split
    else:  # No separator found, treat the whole thing as one menu (fallback)
        return [response_text.strip()]

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
    background-color: #a3edf0; /* Very light gray */
    background-image: url("https://www.transparenttextures.com/patterns/brilliant.png"); /* Subtle metal texture */
}


/* Main Container Styles */
.main-container {
    background-color: white;
    border-radius: 15px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); /* More pronounced shadow */
    padding: 30px;
    margin-bottom: 20px;
    border: 2px solid #e0e0e0; /* Subtle border */

}


/* Header */
.title {
    color: #343a40; /* Darker gray */
    text-align: center;
    padding: 1rem 0;
    font-size: 3rem;  /* Even larger title */
    font-weight: 700;   /* Bold */
    margin-bottom: 1rem; /* Space below the title */
}

/* Mode Selection Radio Buttons*/
.mode-radio {
    margin-bottom: 1.5rem !important;
}
.mode-radio > div {
    display: flex;
    justify-content: center; /* Center the radio buttons */
    gap: 1rem;           /* Space between buttons */
}
.mode-radio label {
    background-color: #e9ecef; /* Light gray background */
    border: 1px solid #ced4da;
    border-radius: 20px; /* Rounded buttons */
    padding: 8px 18px;     /* Comfortable padding */
    margin: 0 5px;
    transition: all 0.2s ease;
}
.mode-radio input[type="radio"]:checked + label {
    background-color: #007bff; /* Blue when selected */
    color: white;
    border-color: #007bff;
}



/* Subheaders */
.st-expanderHeader {
    font-size: 1.3rem; /* Slightly smaller than before */
    font-weight: 600;  /* Semi-bold */
}

/* Input Sections */
.input-section {
    /* Removed background/shadow/padding to blend into main container */
    margin-bottom: 1rem; /* Reduced spacing */
}

/* Input Fields */
.stTextInput, .stSelectbox, .stSlider, .stRadio, .stNumberInput {
    margin-bottom: 0.8rem; /* Consistent spacing */
}

/* Text Area */
.stTextArea>div>div>textarea{
    border-color:#3498db;
    border-radius: 8px; /* Rounded corners */
}

/* Buttons */
.stButton>button {
    background-color: #28a745; /* Green */
    color: white;
    border: none;
    border-radius: 25px; /* More rounded buttons */
    padding: 12px 28px;  /* Larger padding */
    font-size: 1.2rem;    /* Slightly larger font */
    transition: all 0.3s ease;
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
    width: 100%;
}

.stButton>button:hover {
    background-color: #218838; /* Darker green on hover */
    transform: translateY(-3px);  /* More noticeable lift */
    box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);
}

.stButton>button:active {
    transform: translateY(0);
    box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);
}

/* Menu Columns */
.menu-column {
    background-color: #f8f9fa;
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
    color: #28a745; /* Green heading */
    margin-bottom: 12px;
    font-size: 1.5rem;
    font-weight: 600;
}

.menu-item {
    font-size: 1.05rem;
    line-height: 1.7;
    color: #495057; /* Slightly darker gray */
}


/* About Section */
.about-section {
    background-color: #f8f9fa; /* Light gray */
    border-radius: 12px;
    padding: 25px;
    margin-top: 30px; /* More space */
    box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1); /* Consistent shadow */
    border: 1px solid #dee2e6;
}
.about-section ul {
    list-style: none;
    padding: 0;
}

.about-section li {
    margin-bottom: 0.6rem; /* Slightly reduced spacing */
}

/* Spinners */
.st-cf {
    color: #28a745 !important; /* Green spinners */
}

</style>
""", unsafe_allow_html=True)


# --- App UI ---
st.markdown("<h1 class='title'>🍽️ Smart Cooking App 😎</h1>", unsafe_allow_html=True)

with st.container(border=True):  # Main container for content

    option = st.radio("🔹 เลือกโหมด:", ["สร้างเมนูจากวัตถุดิบ", "ค้นหาเมนูสำหรับซื้อ"],
                      horizontal=True, key="mode_select", label_visibility="collapsed")  # Use CSS class

    if option == "สร้างเมนูจากวัตถุดิบ":
        st.subheader("✨ สร้างเมนูแบบกำหนดเอง")

        with st.expander("📝 กรอกวัตถุดิบหลัก", expanded=True):
            ingredients = st.text_area("วัตถุดิบหลัก (คั่นด้วยจุลภาค):",
                                       placeholder="เช่น ไข่, หมูสับ, ผักกาด...",
                                       height=120, label_visibility="collapsed")  # Hide label

        with st.expander("⚙️ ปรับแต่งเมนู", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                category = st.selectbox("ประเภทอาหาร",
                                        ["อาหารทั่วไป", "มังสวิรัติ", "อาหารคลีน", "อาหารไทย", "อาหารญี่ปุ่น",
                                         "อาหารตะวันตก", "อาหารจีน", "อาหารอินเดีย", "อาหารเวียดนาม", "อาหารเกาหลี",
                                         "อาหารเม็กซิกัน", "อาหารอิตาเลียน", "อาหารฟาสต์ฟู้ด", "อาหารทะเล",
                                         "อาหารมังสวิรัติ", "อาหารเจ", "อาหารอีสาน", "อาหารใต้", "อาหารเหนือ",
                                         "อาหารฟิวชั่น", "ขนม", "เครื่องดื่ม"])
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

    elif option == "ค้นหาเมนูสำหรับซื้อ":
        st.subheader("✨ ค้นหาเมนูที่ใช่สำหรับคุณ 3 เมนู")

        with st.expander("⚙️ ตั้งค่าการค้นหา", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                country = st.selectbox('ประเทศที่คุณอยู่ในตอนนี้',
                                       ["ไทย", "ญี่ปุ่น", "เกาหลีใต้", "สหรัฐอเมริกา", "อังกฤษ", "ฝรั่งเศส", "เยอรมนี",
                                        "จีน", "อินเดีย", "รัสเซีย", "แคนาดา", "บราซิล", "ออสเตรเลีย", "อาร์เจนตินา",
                                        "เม็กซิโก", "อิตาลี", "สเปน", "เนเธอร์แลนด์", "สวิตเซอร์แลนด์", "เบลเยียม",
                                        "สวีเดน", "นอร์เวย์", "เดนมาร์ก", "ฟินแลนด์", "โปรตุเกส", "ออสเตรีย", "ไอร์แลนด์",
                                        "กรีซ", "ตุรกี", "แอฟริกาใต้", "อียิปต์", "ไนจีเรีย", "เคนยา", "โมร็อกโก",
                                        "แอลจีเรีย", "ซาอุดีอาระเบีย", "สหรัฐอาหรับเอมิเรตส์", "กาตาร์", "โอมาน", "คูเวต",
                                        "อิหร่าน", "อิรัก", "ปากีสถาน", "บังกลาเทศ", "อินโดนีเซีย", "มาเลเซีย", "สิงคโปร์",
                                        "ฟิลิปปินส์", "เวียดนาม", "พม่า", "กัมพูชา", "ลาว", "มองโกเลีย", "เกาหลีเหนือ",
                                        "ไต้หวัน", "ฮ่องกง", "มาเก๊า", "นิวซีแลนด์", "ฟิจิ", "ปาปัวนิวกินี",
                                        "หมู่เกาะโซโลมอน", "วานูอาตู", "นาอูรู", "ตูวาลู", "คิริบาส", "ไมโครนีเซีย",
                                        "หมู่เกาะมาร์แชลล์", "ปาเลา", "ซามัว", "ตองกา", "นีวเวย์", "หมู่เกาะคุก",
                                        "เฟรนช์โปลินีเซีย", "นิวแคลิโดเนีย", "วาลลิสและฟูตูนา",
                                        "เฟรนช์เซาเทิร์นและแอนตาร์กติกแลนดส์", "เซนต์เฮเลนา", "อัสเซนชัน และตริสตันดากูนยา",
                                        "หมู่เกาะฟอล์กแลนด์", "เซาท์จอร์เจียและหมู่เกาะเซาท์แซนด์วิช", "หมู่เกาะพิตแคร์น",
                                        "บริติชอินเดียนโอเชียนเทร์ริทอรี", "หมู่เกาะบริติชเวอร์จิน", "หมู่เกาะเคย์แมน",
                                        "มอนต์เซอร์รัต", "อังGuilla", "อารูบา", "กูราเซา", "ซินต์มาร์เติน", "โบแนร์",
                                        "เซนต์เอิสตาเชียสและเซนต์มาร์เติน", "กรีนแลนด์", "หมู่เกาะแฟโร", "ยิบรอลตาร์",
                                        "อากรีอาและบาร์บูดา", "แอนติกาและบาร์บูดา", "บาร์เบโดส", "ดอมินิกา", "เกรนาดา",
                                        "เซนต์คิตส์และเนวิส", "เซนต์ลูเซีย", "เซนต์วินเซนต์และเกรนาดีนส์",
                                        "ตรินิแดดและโตเบโก", "แองโกลา", "เบนิน", "บอตสวานา", "บูร์กินาฟาโซ", "บุรุนดี",
                                        "กาบูเวร์ดี", "แคเมอรูน", "สาธารณรัฐแอฟริกากลาง", "ชาด", "สาธารณรัฐคองโก",
                                        "สาธารณรัฐประชาธิปไตยคองโก", "โกตดิวัวร์", "จิบูตี", "อียิปต์", "อิเควทอเรียลกินี",
                                        "เอริเทรีย", "เอสวาตินี", "เอธิโอเปีย", "กาบอง", "แกมเบีย", "กานา", "กินี",
                                        "กินี-บิสเซา", "เคนยา", "เลโซโท", "ไลบีเรีย", "ลิเบีย", "มาดากัสการ์", "มาลาวี",
                                        "มาลี", "มอริเตเนีย", "มอริเชียส", "โมร็อกโก", "โมซัมบิก", "นามิเบีย", "ไนเจอร์",
                                        "ไนจีเรีย", "รวันดา", "เซาตูเมและปรินซิปี", "เซเนกัล", "เซเชลส์", "เซียร์ราลีโอน",
                                        "โซมาเลีย", "แอฟริกาใต้", "ซูดานใต้", "ซูดาน", "แทนซาเนีย", "โตโก", "ตูนิเซีย",
                                        "ยูกันดา", "แซมเบีย", "ซิมบับเว"])
                category = st.selectbox("ประเภทอาหาร",
                                        ["อาหารไทย", "อาหารญี่ปุ่น", "อาหารเกาหลี", "ฟาสต์ฟู้ด", "อาหารสุขภาพ", "อาหารจีน",
                                         "อาหารอินเดีย", "อาหารเวียดนาม", "อาหารเม็กซิกัน", "อาหารอิตาเลียน", "อาหารทะเล",
                                     "อาหารมังสวิรัติ", "อาหารเจ", "อาหารอีสาน", "อาหารใต้", "อาหารเหนือ",
                                     "อาหารฟิวชั่น", "ขนม", "เครื่องดื่ม", "อาหารตะวันตก", "อาหารนานาชาติ"])
        with col2:
            taste = st.radio("รสชาติ", ["เผ็ด", "หวาน", "เค็ม", "เปรี้ยว", "ขม", "อูมามิ", "มัน", "ฝาด", "จืด", 'รสจัด',
                                        'กลมกล่อม', 'กลางๆ'], horizontal=True)
            budget = st.radio("งบประมาณ", ['ต่ำกว่า 100 บาท', '100 - 300 บาท', '300 - 1000 บาท', '1000 - 10000 บาท',
                                           ',มากกว่า 10000 บาท(ไม่จำกัดงบ(ระดับ MrBeast))'], horizontal=True)

    if st.button("🔎 ค้นหาเมนู", use_container_width=True):
        prompt = (f"ฉันต้องการซื้ออาหาร {category} รสชาติ {taste} งบประมาณ {budget} ใน {country} "
                  f"แนะนำ 3 ตัวเลือกเมนู {category} ที่มีขายใน {country} คั่นด้วย '🍽️ เมนูที่' ไม่ต้องเกริ่นนำ")

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
st.markdown("---")  # Separator line
if st.button("📜 เกี่ยวกับผู้พัฒนา", use_container_width=True): # Button for expander
    with st.expander("🤝 พบกับทีมงาน", expanded=False): # Start with it collapsed
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
