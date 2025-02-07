lllllllllllllll, llllllllllllllI, lllllllllllllIl, lllllllllllllII = str, Exception, enumerate, bool

from streamlit import number_input as IlllllIIIIIIll, container as IIllIIllIIIlII, secrets as lllIlIIIIlIIll, button as IIIlIlIIIIIllI, warning as lIllIIllIlIllI, slider as llllIllIlIlIlI, radio as lIIIIIIllIlIll, spinner as IlllIlIIllllII, subheader as lIIlIllIllIllI, selectbox as IlIIlIllIlIIll, expander as lIIIIlllIlIIll, markdown as lIIllIIIIlIIII, text_area as IIIIllIIllllll, columns as lllIlIIlIllIlI
from google.generativeai import configure as lIllIlIIIIlllI, GenerativeModel as IIIIlIIlllIlIl
IIIlIlIllIIIIlllll = lllIlIIIIlIIll['API_KEYS']

def lllllllIlIIIIIlIll(lIIIlIIIllIlIlIllI):
    for IllllIlIlIllIIlIIl in IIIlIlIllIIIIlllll:
        try:
            lIllIlIIIIlllI(api_key=IllllIlIlIllIIlIIl)
            IllllllIIllIllIlII = IIIIlIIlllIlIl('gemini-pro')
            lIlIllIllIlIIIIIlI = IllllllIIllIllIlII.generate_content(lIIIlIIIllIlIlIllI)
            return lIlIllIllIlIIIIIlI.text.strip()
        except llllllllllllllI as IlllIlIIIllllIIIII:
            lIlIIIlIIlIlIlIlII = lllllllllllllll(IlllIlIIIllllIIIII)
            if 'insufficient_quota' in lIlIIIlIIlIlIlIlII or 'Quota exceeded' in lIlIIIlIIlIlIlIlII:
                continue
            else:
                return f'❌ เกิดข้อผิดพลาด: {lIlIIIlIIlIlIlIlII}'
    return '⚠️ API ทั้งหมดหมดโควต้าแล้ว กรุณาตรวจสอบบัญชีของคุณ'

def lIlIIIIIIIlIIlIllI(IlIIIIIIIlIIIIlIII):
    lIIIllIlIllIIIIlll = IlIIIIIIIlIIIIlIII.split('🍽️ เมนูที่')
    lIIIllIlIllIIIIlll = [lIIIIIlIIIlIlllIIl.strip() for lIIIIIlIIIlIlllIIl in lIIIllIlIllIIIIlll if lIIIIIlIIIlIlllIIl.strip()]
    if not lIIIllIlIllIIIIlll:
        lIIIllIlIllIIIIlll = IlIIIIIIIlIIIIlIII.split('\n- ')
        lIIIllIlIllIIIIlll = [lIIIIIlIIIlIlllIIl.strip() for lIIIIIlIIIlIlllIIl in lIIIllIlIllIIIIlll if lIIIIIlIIIlIlllIIl.strip()]
    if not lIIIllIlIllIIIIlll:
        lIIIllIlIllIIIIlll = IlIIIIIIIlIIIIlIII.split('\n• ')
        lIIIllIlIllIIIIlll = [lIIIIIlIIIlIlllIIl.strip() for lIIIIIlIIIlIlllIIl in lIIIllIlIllIIIIlll if lIIIIIlIIIlIlllIIl.strip()]
    return lIIIllIlIllIIIIlll
lIIllIIIIlIIII('\n<style>\n/* Global Styles */\nbody {\n    font-family: \'Kanit\', sans-serif; /* Modern Thai font */\n}\n\n.stApp {\n    background-color: #f0f2f6;  /* Light gray background */\n    background-image: url("https://www.transparenttextures.com/patterns/subtle-white-feathers.png"); /*Subtle Background Pattern*/\n\n}\n\n/* Header */\n.title {\n    color: #2c3e50;\n    text-align: center;\n    padding: 1rem 0;\n    font-size: 2.5rem; /* Larger title */\n    font-weight: 600;  /* Semi-bold */\n}\n\n/* Mode Selection */\n.mode-selection {\n    margin-bottom: 2rem;\n    border-radius: 10px;\n    padding: 10px;\n    background-color: white;\n    box-shadow: 0 4px 8px rgba(0,0,0,0.1);\n}\n\n/* Input Sections */\n.input-section {\n    background-color: white;\n    padding: 20px;\n    border-radius: 10px;\n    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);\n    margin-bottom: 20px;\n}\n\n/* Input Fields */\n.stTextInput, .stSelectbox, .stSlider, .stRadio, .stNumberInput {\n    margin-bottom: 10px;\n}\n.stTextArea>div>div>textarea{\n    border-color:#3498db;\n}\n\n/* Buttons */\n.stButton>button {\n    background-color: #3498db; /* Blue */\n    color: white;\n    border: none;\n    border-radius: 20px; /* Rounded buttons */\n    padding: 10px 24px;\n    font-size: 1.1rem;\n    transition: all 0.3s ease;\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2); /* Subtle shadow */\n    width: 100%; /* Make buttons full width */\n}\n\n.stButton>button:hover {\n    background-color: #2980b9; /* Darker blue on hover */\n    transform: translateY(-2px); /* Slight lift on hover */\n    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);\n}\n\n.stButton>button:active {\n    transform: translateY(0); /* Reset position on click */\n    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);\n}\n\n/* Menu Columns */\n.menu-column {\n    background-color: white;\n    border-radius: 10px;\n    padding: 20px;\n    margin-bottom: 20px;\n    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);\n    transition: transform 0.2s ease; /* Smooth transition */\n    border: 2px solid transparent; /* Add a border */\n}\n\n.menu-column:hover {\n    transform: scale(1.03); /* Slightly enlarge on hover */\n    border-color: #3498db;\n}\n\n.menu-column h3 {\n    color: #3498db; /* Blue heading */\n    margin-bottom: 10px;\n    font-size: 1.4rem;\n}\n\n.menu-item {\n    font-size: 1rem;\n    line-height: 1.6;\n    color: #4a4a4a; /* Dark gray text */\n}\n\n/* Expander */\n.st-expanderHeader {\n    font-size: 1.2rem;\n    font-weight: 500; /* Slightly bolder expander header */\n}\n\n/* About Section */\n.about-section {\n    background-color: #e0e0e0;\n    border-radius: 10px;\n    padding: 20px;\n    margin-top: 20px;\n}\n.about-section ul {\n    list-style: none; /* Remove bullet points */\n    padding: 0;\n\n}\n\n.about-section li {\n    margin-bottom: .5rem;\n}\n\n/* Spinners */\n.st-cf {\n    color: #3498db !important; /* Make spinners blue */\n}\n\n</style>\n', unsafe_allow_html=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
lIIllIIIIlIIII("<h1 class='title'>🍽️ Smart Cooking App 😎 \n\n (กรุณาปิด Dark Mode ก่อนใช้งาน)</h1>", unsafe_allow_html=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
with IIllIIllIIIlII(border=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
    lIIIlIIIlllllllllI = lIIIIIIllIlIll('🔹 เลือกโหมด:', ['สร้างเมนูจากวัตถุดิบ', 'ค้นหาเมนูสำหรับซื้อ'], horizontal=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1), key='mode_select')
if lIIIlIIIlllllllllI == 'สร้างเมนูจากวัตถุดิบ':
    lIIlIllIllIllI('✨ สร้างเมนูแบบกำหนดเอง')
    with lIIIIlllIlIIll('📝 กรอกวัตถุดิบของคุณ', expanded=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
        IlIllIIlIlllIIllII = IIIIllIIllllll('วัตถุดิบ (คั่นด้วยจุลภาค):', placeholder='เช่น ไข่, หมูสับ, ผักกาด...', height=120)
    with lIIIIlllIlIIll('⚙️ ปรับแต่งเมนูของคุณ', expanded=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 0)):
        (IIlIllIlIlIIIIlIlI, IIlllllllIlIlllIll) = lllIlIIlIllIlI(2)
        with IIlIllIlIlIIIIlIlI:
            llIlIlIlIlllllIlll = IlllllIIIIIIll('จำนวนวัตถุดิบหลัก', min_value=1, max_value=20, value=3, step=1)
            IIllllllllIIIIIlII = IlIIlIllIlIIll('ประเภทอาหาร', ['อาหารทั่วไป', 'มังสวิรัติ', 'อาหารคลีน', 'อาหารไทย', 'อาหารญี่ปุ่น', 'อาหารตะวันตก'])
            llIlIllIlIlIIllIII = llllIllIlIlIlI('แคลอรี่ที่ต้องการ (kcal)', 100, 1500, 500, step=50)
        with IIlllllllIlIlllIll:
            llIIIIlIIIllIIlIll = lIIIIIIllIlIll('ระดับความยาก', ['ง่าย', 'ปานกลาง', 'ยาก'], horizontal=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            IIlIlIIlllllIllllI = llllIllIlIlIlI('เวลาทำอาหาร (นาที)', 5, 180, 30, step=5)
    if IIIlIlIIIIIllI('🍳 สร้างเมนู', use_container_width=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
        if IlIllIIlIlllIIllII:
            lIIIlIIIllIlIlIllI = f"ฉันมี: {IlIllIIlIlllIIllII} ({llIlIlIlIlllllIlll} วัตถุดิบหลัก) แนะนำเมนู {IIllllllllIIIIIlII} เวลาทำไม่เกิน {IIlIlIIlllllIllllI} นาที ประมาณ {llIlIllIlIlIIllIII} kcal ระดับความยาก {llIIIIlIIIllIIlIll} พร้อมวิธีทำอย่างละเอียด เสนอ 3 ตัวเลือก คั่นด้วย '🍽️ เมนูที่'"
            with IlllIlIIllllII('กำลังสร้างสรรค์ไอเดียอร่อยๆ...'):
                lIIIllIlIllIIIIlll = lIlIIIIIIIlIIlIllI(lllllllIlIIIIIlIll(lIIIlIIIllIlIlIllI))
            if lIIIllIlIllIIIIlll:
                lIIlIllIllIllI('🧑\u200d🍳 เมนูแนะนำ:')
                lIlIlllIIIIIIIIIlI = lllIlIIlIllIlI(3)
                for (IlIIlIIIlIlIIlIllI, lIIIIIlIIIlIlllIIl) in lllllllllllllIl(lIIIllIlIllIIIIlll[:3]):
                    with lIlIlllIIIIIIIIIlI[IlIIlIIIlIlIIlIllI]:
                        lIIllIIIIlIIII(f"<div class='menu-column'><h3>🍽️ เมนูที่ {IlIIlIIIlIlIIlIllI + 1}</h3><p class='menu-item'>{lIIIIIlIIIlIlllIIl}</p></div>", unsafe_allow_html=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            else:
                lIllIIllIlIllI('⚠️ ไม่พบเมนูที่ตรงกับเกณฑ์ของคุณ โปรดลองปรับการตั้งค่า')
        else:
            lIllIIllIlIllI('⚠️ กรุณากรอกวัตถุดิบของคุณ')
elif lIIIlIIIlllllllllI == 'ค้นหาเมนูสำหรับซื้อ':
    lIIlIllIllIllI('✨ ค้นหาเมนูที่ใช่สำหรับคุณ')
    with lIIIIlllIlIIll('⚙️ ตั้งค่าการค้นหา', expanded=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
        (IIlIllIlIlIIIIlIlI, IIlllllllIlIlllIll) = lllIlIIlIllIlI(2)
        with IIlIllIlIlIIIIlIlI:
            llIlIlllIIlIlIllIl = IlIIlIllIlIIll('ประเทศที่คุณอยู่ในตอนนี้', ['ไทย', 'ญี่ปุ่น', 'เกาหลีใต้', 'สหรัฐอเมริกา', 'อังกฤษ', 'ฝรั่งเศส', 'เยอรมนี'])
            IIllllllllIIIIIlII = IlIIlIllIlIIll('ประเภทอาหาร', ['อาหารไทย','อาหารท้องถิ่น', 'อาหารญี่ปุ่น', 'อาหารเกาหลี', 'ฟาสต์ฟู้ด', 'อาหารสุขภาพ'])
        with IIlllllllIlIlllIll:
            lIlllIllIIIIIIllll = lIIIIIIllIlIll('รสชาติ', ['เผ็ด', 'หวาน', 'เค็ม', 'เปรี้ยว','กลางๆ','รสจัด','กลมกล่อม'], horizontal=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
            IIlllllIIlIIIlIlll = lIIIIIIllIlIll('งบประมาณ', ['ต่ำกว่า 100 บาท', '100 - 300 บาท', 'มากกว่า 300 บาท','ไม่จำกัดงบ(ระดับ MrBeast)'], horizontal=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
    if IIIlIlIIIIIllI('🔎 ค้นหาเมนู', use_container_width=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
        lIIIlIIIllIlIlIllI = f"ฉันต้องการซื้ออาหาร {IIllllllllIIIIIlII} รสชาติ {lIlllIllIIIIIIllll} งบประมาณ {IIlllllIIlIIIlIlll} ใน {llIlIlllIIlIlIllIl} แนะนำ 3 ตัวเลือกเมนู {IIllllllllIIIIIlII} ที่มีขายใน {llIlIlllIIlIlIllIl} พร้อมบอกราคา คั่นด้วย '🍽️ เมนูที่'"
        with IlllIlIIllllII('กำลังค้นหาตัวเลือกที่ดีที่สุด...'):
            lIIIllIlIllIIIIlll = lIlIIIIIIIlIIlIllI(lllllllIlIIIIIlIll(lIIIlIIIllIlIlIllI))
        if lIIIllIlIllIIIIlll:
            lIIlIllIllIllI('🧑\u200d🍳 เมนูแนะนำ:')
            lIlIlllIIIIIIIIIlI = lllIlIIlIllIlI(3)
            for (IlIIlIIIlIlIIlIllI, lIIIIIlIIIlIlllIIl) in lllllllllllllIl(lIIIllIlIllIIIIlll[:3]):
                with lIlIlllIIIIIIIIIlI[IlIIlIIIlIlIIlIllI]:
                    lIIllIIIIlIIII(f"<div class='menu-column'><h3>🍽️ เมนูที่ {IlIIlIIIlIlIIlIllI + 1}</h3><p class='menu-item'>{lIIIIIlIIIlIlllIIl}</p></div>", unsafe_allow_html=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
        else:
            lIllIIllIlIllI('⚠️ ไม่พบเมนู โปรดลองอีกครั้ง')
lIIllIIIIlIIII('---')
if IIIlIlIIIIIllI('📜 เกี่ยวกับผู้พัฒนา', use_container_width=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1)):
    with lIIIIlllIlIIll('🤝 พบกับทีมงาน'):
        lIIllIIIIlIIII("\n        <div class='about-section'>\n        <ul>\n        <li><strong>1. นาย กัลปพฤกษ์ วิเชียรรัตน์</strong> - <em>ชั้น 6/13 เลขที่ 3 (คนแบกครับอิๆ😎)</em></li>\n        <li><strong>2. นาย ธีราธร มุกดาเพชรรัตน์</strong> - <em>ชั้น 6/13 เลขที่ 13</em></li>\n        <li><strong>3. นาย อภิวิชญ์ อดุลธรรมวิทย์</strong> - <em>ชั้น 6/13 เลขที่ 28</em></li>\n        <li><strong>4. นาย ปัณณวิชญ์ หลีกภัย </strong>  - <em> ชั้น 6/13 เลขที่ 29</em></li>\n        </ul>\n        </div>\n        ", unsafe_allow_html=lllllllllllllII(((1 & 0 ^ 0) & 0 ^ 1) & 0 ^ 1 ^ 1 ^ 0 | 1))
