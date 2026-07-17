import streamlit as st
import google.generativeai as genai

# ตั้งค่าหน้าเว็บ
st.set_page_config(page_title="DILI LiverTox Search", page_icon="🩺")
st.title("🩺 DILI Search from LiverTox")
st.markdown("ค้นหาข้อมูล Drug-Induced Liver Injury (DILI) อ้างอิงจาก **LiverTox (NCBI)**")

# ดึง API Key จากระบบหลังบ้านแบบลับ (Streamlit Secrets)
try:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
except KeyError:
    st.error("ยังไม่ได้ตั้งค่า API Key ในระบบหลังบ้าน กรุณาตั้งค่าใน Streamlit Settings")
    st.stop()

# ช่องค้นหาชื่อยา (เหลือแค่ช่องนี้ช่องเดียว)
drug_name = st.text_input("พิมพ์ชื่อยา (เช่น Amoxicillin-clavulanate):")

if st.button("ค้นหาข้อมูล", type="primary"):
    if not drug_name:
        st.warning("กรุณาพิมพ์ชื่อยาครับ")
    else:
        with st.spinner(f'กำลังดึงข้อมูล "{drug_name}" จาก LiverTox...'):
            try:
                # ใช้โมเดลมาตรฐานที่เสถียร
                model = genai.GenerativeModel('gemini-pro')
                
                # คำสั่งที่บังคับให้ AI ดึงเฉพาะ 6 ข้อ จาก Livertox
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
                
                # เรียกใช้ AI และแสดงผล
                response = model.generate_content(prompt)
                st.success("ค้นหาสำเร็จ!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"เกิดข้อผิดพลาด: {e}")
