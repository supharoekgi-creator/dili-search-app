import streamlit as st

st.set_page_config(page_title="DILI Search Fast-Link", page_icon="🩺")
st.title("🩺 DILI Search from LiverTox")
st.markdown("ทางลัดสำหรับค้นหาข้อมูล DILI ในเว็บไซต์ **LiverTox (NCBI)** อย่างรวดเร็ว")

# ช่องค้นหาชื่อยา
drug_name = st.text_input("พิมพ์ชื่อยาที่ต้องการค้นหา (เช่น Amoxicillin):")

if st.button("สร้างลิงก์ค้นหา", type="primary"):
    if not drug_name:
        st.warning("⚠️ กรุณาพิมพ์ชื่อยาครับ")
    else:
        # สร้างลิงก์ค้นหาตรงไปที่หมวด LiverTox ของ NCBI
        search_url = f"https://www.ncbi.nlm.nih.gov/books/?term=livertox+[book]+AND+{drug_name}"
        
        st.success("สร้างลิงก์สำเร็จ!")
        st.markdown("---")
        st.markdown(f"### 👉 **[คลิกที่นี่เพื่อไปหน้าค้นหายา {drug_name.upper()} ใน LiverTox]({search_url})**")
        
        st.info("""
        **📌 ข้อมูลที่คุณหมอต้องการ (เพื่อนำไปสแกนหาในเว็บ):**
        1. Liver injury pattern (Hepatocellular, Cholestatic, Mixed)
        2. Specific liver function 
        3. Onset
        4. Recovery time
        5. Likelihood ratio (Score)
        """)
