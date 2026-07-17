import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DILI Search", page_icon="🩺")
st.title("🩺 DILI Search from LiverTox")
st.markdown("ค้นหาข้อมูล Drug-Induced Liver Injury อ้างอิงจาก **LiverTox (NCBI)**")

# ระบบจัดการ API Key อัตโนมัติ (ไม่ให้แอปพัง)
api_key = ""
try:
    # พยายามดึงรหัสจากระบบหลังบ้านก่อน
    api_key = st.secrets["GEMINI_API_KEY"]
except:
    # ถ้าดึงไม่ได้ หรือตั้งค่าผิด จะแสดงช่องให้ใส่หน้าเว็บแทน
    api_key = st.text_input("ใส่ Gemini API Key (เฉพาะคนที่มีลิงก์):", type="password")

# ช่องค้นหาชื่อยา
drug_name = st.text_input("พิมพ์ชื่อยา (เช่น Amoxicillin):")

if st.button("ค้นหาข้อมูล", type="primary"):
    if not api_key:
        st.warning("⚠️ ไม่พบ API Key กรุณาใส่รหัสในช่องด้านบนครับ")
    elif not drug_name:
        st.warning("⚠️ กรุณาพิมพ์ชื่อยาครับ")
    else:
        with st.spinner(f'กำลังค้นหาข้อมูล "{drug_name}" จาก LiverTox...'):
            try:
                # ตั้งค่ารหัส API
                genai.configure(api_key=api_key)
                
                prompt = f"""
                You are a medical assistant extracting DILI data strictly from the LiverTox database (NCBI) (https://www.ncbi.nlm.nih.gov/books/NBK547852/). 
                Search for the drug: {drug_name}
                Return the summary in THAI language with exactly these 6 numbers/bullets. Do not add intro/outro text:
                1. Liver injury pattern: (Hepatocellular, Cholestatic, Mixed, or most common. If none, put N/A)
                2. Specific liver function: (Specific lab abnormalities. If none, put N/A)
                3. Onset: (Time to onset. If none, put N/A)
                4. Recovery time: (Time to recovery. If none, put N/A)
                5. Likelihood ratio: (LiverTox score e.g. Score A)
                6. Link: (Exact NCBI LiverTox URL for {drug_name})
                Do NOT use external sources. Do NOT hallucinate data.
                """
                
                # ระบบสลับโมเดลอัตโนมัติ (กัน Error รุ่นเก่า/ใหม่)
                try:
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    response = model.generate_content(prompt)
                except:
                    model = genai.GenerativeModel('gemini-pro')
                    response = model.generate_content(prompt)
                
                # แสดงผลลัพธ์
                st.success("✅ ค้นหาสำเร็จ!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"❌ เกิดข้อผิดพลาดในการดึงข้อมูล โปรดตรวจสอบ API Key หรือชื่อยาอีกครั้ง (Error: {e})")
