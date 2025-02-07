import streamlit as st
셎=Exception
𣾝=str
𤽡=True
㓸=enumerate
䝊=False
ﳛ=st.warning
ﺭ=st.spinner
𐰋=st.radio
𦅊=st.slider
ࡁ=st.selectbox
𐳭=st.text_area
쏆=st.expander
𠟏=st.subheader
ﱽ=st.session_state
𢒒=st.button
𥄻=st.columns
뭁=st.container
鴴=st.markdown
𘢈=st.set_page_config
ⷖ=st.secrets
import google.generativeai as genai
import textwrap
𣠤=ⷖ["API_KEYS"]
𘢈(page_title="🍽️ Smart Cooking App 😎",page_icon="🍳",layout="wide",initial_sidebar_state="expanded",)
def ךּ(鈱):
 for ﷱ in 𣠤:
  try:
   genai.configure(api_key=ﷱ)
   ﬡ=genai.GenerativeModel("gemini-2.0-flash-lite-preview-02-05")
   𐤏=ﬡ.generate_content(鈱)
   return 𐤏.text.strip()
  except 셎 as e:
   ﻄ=𣾝(e)
   if "insufficient_quota" in ﻄ or "Quota exceeded" in ﻄ:
    continue
   else:
    return f"❌ เกิดข้อผิดพลาด: {error_message}"
 return "⚠️ API ทั้งหมดหมดโควต้าแล้ว กรุณาตรวจสอบบัญชีของคุณ"
def 𫫒(response_text):
 מּ=[]
 𝞬=["🍽️ เมนูที่","\n- ","\n• ","\n— ","- ","• "]
 for 稯 in 𝞬:
  if 稯 in response_text:
   מּ=response_text.split(稯)
   break
 else:
  return[response_text.strip()]
 מּ=[menu.strip()for menu in מּ if menu.strip()]
 return מּ
鴴("""
<style>
/*Global Styles */
body {font-family: 'Kanit', sans-serif;}
.stApp {/* Default Streamlit background */}
/* Main Container Styles */
.main-container {border-radius: 15px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); padding: 30px; margin-bottom: 20px; border: 2px solid #e0e0e0;}
/* Header */
.title {color: #343a40; text-align: center; padding: 1rem 0; font-size: 3rem; font-weight: 700; margin-bottom: 1rem;}
/* Mode Selection Buttons - Using st.buttons */
.mode-buttons {display: flex; justify-content: center; gap: 20px; /* Spacing between buttons */ margin-bottom: 30px;}
.mode-button {background-color: #007bff; /* Blue */ color: white; border: none; border-radius: 8px; /* Rounded */ padding: 15px 30px; /* Larger padding */ font-size: 1.4rem; /* Larger font */ font-weight: bold; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 2px 5px rgba(0,0,0,0.2);}
.mode-button:hover {background-color: #0056b3; /* Darker blue on hover */ transform: translateY(-2px);}
.mode-button-selected {background-color: #28a745; /* Green - for the selected mode */ color: white; border: none; border-radius: 8px; padding: 15px 30px; font-size: 1.4rem; font-weight: bold; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 2px 5px rgba(0,0,0,0.2);}
.mode-button-selected:hover {background-color: #1e7e34; transform: translateY(-2px);}
/* Subheaders */
.st-expanderHeader {font-size: 1.6rem; /* Even larger */ font-weight: 700; margin-bottom: 0.5rem;}
/* Input Sections */
.input-section {margin-bottom: 1rem;}
/* Input Fields */
.stTextInput, .stSelectbox, .stSlider, .stRadio, .stNumberInput {margin-bottom: 0.8rem;}
/* Text Area */
.stTextArea>div>div>textarea{border-color:#3498db; border-radius: 8px;}
/* Buttons */
.stButton>button {background-color: #28a745; color: white; border: none; border-radius: 25px; padding: 12px 28px; font-size: 1.2rem; transition: all 0.3s ease; box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15); width: 100%;}
.stButton>button:hover {background-color: #218838; transform: translateY(-3px); box-shadow: 0 5px 10px rgba(0, 0, 0, 0.2);}
.stButton>button:active {transform: translateY(0); box-shadow: 0 3px 6px rgba(0, 0, 0, 0.15);}
/* Menu Columns */
.menu-column {border-radius: 12px; padding: 25px; margin-bottom: 15px; box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1); transition: transform 0.25s ease, box-shadow 0.25s ease; border: 1px solid #dee2e6;}
.menu-column:hover {transform: scale(1.02); box-shadow: 0 5px 15px rgba(0, 0, 0, 0.15);}
.menu-column h3 {color: #28a745; margin-bottom: 12px; font-size: 1.5rem; font-weight: 600;}
.menu-item {font-size: 1.05rem; line-height: 1.7;}
/* About Section */
.about-section {border-radius: 12px; padding: 25px; margin-top: 30px; box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1); border: 1px solid #dee2e6;}
.about-section ul {list-style: none; padding: 0;}
.about-section li {margin-bottom: 0.6rem;}
/* Spinners */
.st-cf {color: #28a745 !important;}
/* Larger and Bolder Expander Text */
.st-expander button[data-baseweb="button"] {font-size: 1.4rem !important; /* Larger font */ font-weight: bold !important; /* Bold text */}
/* Change expander icons */
.st-expander svg {color: #007bff; /* Blue expander icon */}
</style>
""", unsafe_allow_html=𤽡)
鴴("<h1 class='title'>🍽️ Smart Cooking App 😎</h1>",unsafe_allow_html=𤽡)
with 뭁(border=𤽡):
 𞠽,ว=𥄻(2) 
 with 𞠽:
  if 𢒒("📝 สร้างเมนูทำกินเอง 👨‍🍳",key="create_mode",type='primary' if 'mode' not in ﱽ or ﱽ.mode=="create" else 'secondary'):
   ﱽ.mode="create" 
 with ว:
  if 𢒒("🔍 ค้นหาเมนูที่จะซื้อกิน 😎",key="search_mode",type='primary' if 'mode' in ﱽ and ﱽ.mode=="search" else 'secondary'):
   ﱽ.mode="search"
 if 'mode' not in ﱽ or ﱽ.mode=="create":
  𠟏("✨ สร้างเมนูแบบกำหนดเอง")
  with 쏆("📝 กรอกวัตถุดิบหลัก",expanded=𤽡):
   𐼔=𐳭("วัตถุดิบหลัก (คั่นด้วยจุลภาค):",placeholder="เช่น ไข่, หมูสับ, ผักกาด...",height=120,label_visibility="collapsed")
  with 쏆("⚙️ ปรับแต่งเมนู",expanded=𤽡):
   𞠽,ว=𥄻(2)
   with 𞠽:
    𐤌=ࡁ("ประเภทอาหาร",ⷖ['foodtype1'])
    𒌋=𦅊("แคลอรี่ที่ต้องการ (kcal)",100,1500,500,step=50)
   with ว:
    ﳕ=𐰋("ระดับความยาก",["ง่าย","ปานกลาง","ยาก",'ยากมาก','นรก'],horizontal=𤽡)
    𞺥=𦅊("เวลาทำอาหาร (นาที)",5,180,30,step=5)
  if 𢒒("🍳 สร้างเมนู",use_container_width=𤽡):
   if 𐼔:
    鈱=(f"ฉันมี: {ingredients} เป็นวัตถุดิบหลัก " f"แนะนำเมนู {category} เวลาทำไม่เกิน {cook_time} นาที " f"ประมาณ {calories} kcal ระดับความยาก ระดับ{difficulty} " f"พร้อมวิธีทำอย่างละเอียด เสนอ 3 ตัวเลือก คั่นด้วย '🍽️ เมนูที่' ไม่ต้องเกริ่นนำ")
    with ﺭ("กำลังสร้างสรรค์ไอเดียอร่อยๆ... 3 เมนู"):
     מּ=𫫒(ךּ(鈱))
    if מּ:
     𠟏("🧑‍🍳 เมนูแนะนำ 3 เมนู:")
     흃=𥄻(3)
     for i,menu in 㓸(מּ[:3]):
      with 흃[i]:
       鴴(f"<div class='menu-column'><h3>🍽️ เมนูที่ {i + 1}</h3><p class='menu-item'>{menu}</p></div>",unsafe_allow_html=𤽡)
    else:
     ﳛ("⚠️ ไม่พบเมนูที่ตรงกับเกณฑ์ของคุณ โปรดลองปรับการตั้งค่า")
   else:
    ﳛ("⚠️ กรุณากรอกวัตถุดิบของคุณ")
 elif ﱽ.mode=="search":
  𠟏("✨ ค้นหาเมนูที่ใช่สำหรับคุณ 3 เมนู")
  with 쏆("⚙️ ตั้งค่าการค้นหา",expanded=𤽡):
   𞠽,ว=𥄻(2)
   with 𞠽:
    𐰑=ࡁ('ประเทศที่คุณอยู่ในตอนนี้',ⷖ['country1'])
    𐤌=ࡁ("ประเภทอาหาร",ⷖ['foodtype2'])
   with ว:
    𦷸=𐰋("รสชาติ",["เผ็ด","หวาน","เค็ม","เปรี้ยว","ขม","อูมามิ","มัน","ฝาด","จืด",'รสจัด','กลมกล่อม','กลางๆ'],horizontal=𤽡)
    ﺒ=𐰋("งบประมาณ",['ต่ำกว่า 100 บาท','100 - 300 บาท','300 - 1000 บาท','1000 - 10000 บาท','มากกว่า 10000 บาท(ไม่จำกัดงบ(ระดับ MrBeast))'],horizontal=𤽡)
  if 𢒒("🔎 ค้นหาเมนู",use_container_width=𤽡):
   鈱=(f"ฉันต้องการซื้ออาหาร {category} รสชาติ {taste} งบประมาณ {budget} ใน {country} " f"แนะนำ 3 ตัวเลือกเมนู {category} ที่มีขายใน {country} คั่นด้วย '🍽️ เมนูที่' ไม่ต้องเกริ่นนำ")
   with ﺭ("กำลังค้นหาตัวเลือกที่ดีที่สุด... 3 เมนู"):
    מּ=𫫒(ךּ(鈱))
   if מּ:
    𠟏("🧑‍🍳 เมนูแนะนำ 3 เมนู:")
    흃=𥄻(3)
    for i,menu in 㓸(מּ[:3]):
     with 흃[i]:
      鴴(f"<div class='menu-column'><h3>🍽️ เมนูที่ {i + 1}</h3><p class='menu-item'>{menu}</p></div>",unsafe_allow_html=𤽡)
   else:
    ﳛ("⚠️ ไม่พบเมนู โปรดลองอีกครั้ง")
鴴("---")
if 𢒒("📜 เกี่ยวกับผู้พัฒนา",use_container_width=𤽡):
 with 쏆("🤝 พบกับทีมงาน",expanded=䝊):
  鴴("""
      <divclass='about-section'>
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
        """  , unsafe_allow_html=𤽡)
