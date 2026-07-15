import streamlit as st
import urllib.request
import urllib.parse
import json
import re

# การตั้งค่าหน้าเว็บของ riendee
st.set_page_config(
    page_title="riendee - smart ai study partner",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ตกแต่งสไตล์ CSS ให้สวยงามน่ารักสไตล์แบรนด์ riendee
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    .stButton>button {
        width: 100%;
        border-radius: 14px;
        height: 3.5em;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        color: white;
        font-weight: bold;
        border: none;
        transition: 0.3s;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #4f46e5 0%, #4338ca 100%);
        box-shadow: 0 4px 20px rgba(79, 70, 229, 0.4);
        transform: translateY(-1px);
    }
    .brand-title {
        font-size: 42px;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1 0%, #4f46e5 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 5px;
    }
    .form-section {
        background-color: #f1f5f9;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin-bottom: 15px;
    }
    .quiz-card {
        padding: 20px;
        border-radius: 16px;
        background-color: white;
        border-left: 5px solid #6366f1;
        box-shadow: 0 4px 12px rgba(0,0,0,0.03);
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# ฟังก์ชันเชื่อมต่อกับ Pollinations AI
def generate_pollinations_ai(prompt_text):
    url = "https://text.pollinations.ai/"
    
    system_content = (
        "You are 'riendee' (เรียนดี) an expert Thai academic assistant. "
        "Your task is to translate and solve the user's questions. "
        "Please provide the output in a clear format. You can use markdown or JSON."
    )
    
    payload = {
        "messages": [
            {"role": "system", "content": system_content},
            {"role": "user", "content": prompt_text}
        ],
        "model": "openai",
        "jsonMode": False
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            url, 
            data=data, 
            headers={
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            res_body = response.read().decode('utf-8')
            return res_body
    except Exception as e:
        return f"เกิดข้อผิดพลาดในการเชื่อมต่อ: {str(e)}"

# ฟังก์ชันดึงเนื้อหาหน้าเว็บ
def extract_text_pure_python(url_string):
    try:
        req = urllib.request.Request(
            url_string, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            clean_text = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', html)
            lines = [line.strip() for line in clean_text.splitlines() if line.strip()]
            return " ".join(lines)[:12000]
    except Exception as e:
        return f"Error_Scraping: {str(e)}"

# แถบด้านซ้ายมือ (Sidebar)
with st.sidebar:
    st.markdown("<h1 style='text-align: center; font-size: 70px; margin-top: 0; margin-bottom: 10px;'>🎓</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='color: #f1f5f9; font-weight: 800; text-align: center;'>riendee settings</h2>", unsafe_allow_html=True)
    st.markdown("🎉 **เวอร์ชันแก้บั๊ก SyntaxError สำเร็จแล้ว!** ระบบการ์ดแยกข้อกลับมาทำงานได้สมบูรณ์")
    
    st.divider()
    st.markdown("### 🛠 โหมดทำงานของ riendee")
    mode = st.radio("เลือกหน้าที่ต้องการให้ AI ทำงาน:", 
                    ["แปลภาษาและเฉลยโจทย์", "สรุปใจความสำคัญจากเนื้อหา", "วิเคราะห์เชิงลึกและอธิบาย", "✨ คลังสร้างข้อสอบทดสอบตัวเอง"])

# แผงต้อนรับหลักบนหน้าจอกลาง
st.markdown('<h1 class="brand-title">🎓 riendee</h1>', unsafe_allow_html=True)
st.subheader("เพื่อนคู่คิดอัจฉริยะ ช่วยแปลภาษา ดึงข้อมูลจากเว็บ และวิเคราะห์คำตอบที่ดีที่สุด")
st.write("---")

# แถบรับข้อมูลนำเข้า
input_method = st.radio(
    "เลือกวิธีการใช้งานระบบ:", 
    ["📝 พิมพ์/วางข้อความเอง", "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)", "🌐 ใส่ลิงก์เว็บไซต์ (URL)", "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ"]
)

user_input = ""
web_url = ""

if input_method == "📝 พิมพ์/วางข้อความเอง":
    user_input = st.text_area("✍️ พิมพ์หรือวางโจทย์วิชาการ/บทความที่นี่:", height=250, 
                             placeholder="วางโจทย์หรือข้อความหลายๆ ข้อที่นี่...")

elif input_method == "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)":
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### ✏️ กรอกรายละเอียดโจทย์ในฟอร์มด้านล่าง")
    form_subject = st.selectbox("📚 เลือกกลุ่มวิชา:", ["วิทยาศาสตร์ (Science)", "คณิตศาสตร์ (Mathematics)", "ภาษาและวรรณกรรม (Language)", "คอมพิวเตอร์และเทคโนโลยี (IT)", "อื่นๆ (Others)"])
    form_question = st.text_area("❓ ตัวโจทย์/คำถามภาษาอังกฤษ (Question):", placeholder="พิมพ์คำถามของคุณตรงนี้")
    
    has_choices = st.checkbox("➕ โจทย์นี้มีตัวเลือก (Multiple Choice)")
    choice_a, choice_b, choice_c, choice_d = "", "", "", ""
    if has_choices:
        col_a, col_b = st.columns(2)
        with col_a:
            choice_a = st.text_input("ตัวเลือก A:", placeholder="ชอยส์ข้อ A")
            choice_c = st.text_input("ตัวเลือก C:", placeholder="ชอยส์ข้อ C")
        with col_b:
            choice_b = st.text_input("ตัวเลือก B:", placeholder="ชอยส์ข้อ B")
            choice_d = st.text_input("ตัวเลือก D:", placeholder="ชอยส์ข้อ D")
    form_instruction = st.text_input("🎯 คำสั่งพิเศษเพิ่มเติม (ถ้ามี):", placeholder="เช่น ขอสูตรอย่างละเอียด")
    st.markdown('</div>', unsafe_allow_html=True)

elif input_method == "🌐 ใส่ลิงก์เว็บไซต์ (URL)":
    web_url = st.text_input("🌐 ใส่ลิงก์หน้าเว็บที่คุณต้องการดึงข้อมูล:", placeholder="ใส่ลิงก์ที่นี่...")

elif input_method == "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ":
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown("### 🎲 สั่งให้ riendee ออกข้อสอบจำลอง")
    quiz_topic = st.text_input("📝 พิมพ์หัวข้อเรื่องหรือบทเรียนที่ต้องการทำข้อสอบ:", placeholder="เช่น English vocabulary")
    quiz_count = st.slider("📊 จำนวนข้อที่ต้องการให้น้องออกสอบ:", min_value=1, max_value=5, value=3)
    quiz_level = st.select_slider("🔥 ระดับความยาก:", options=["ง่าย (Easy)", "ปานกลาง (Medium)", "ยาก (Hard)"])
    st.markdown('</div>', unsafe_allow_html=True)

# เมื่อกดปุ่มรันโปรแกรม
if st.button("🚀 เริ่มการทำงานด้วย riendee AI"):
    is_valid = True

    if input_method == "🌐 ใส่ลิงก์เว็บไซต์ (URL)":
        if not web_url.strip():
            st.error("❌ กรุณาระบุลิงก์เว็บไซต์ก่อนกดปุ่ม")
            is_valid = False
        else:
            with st.spinner('riendee กำลังเข้าไปคัดลอกข้อความจากหน้าเว็บ...'):
                scraped_content = extract_text_pure_python(web_url)
            if "Error_Scraping" in scraped_content:
                st.error(f"❌ ดึงข้อมูลล้มเหลว: {scraped_content}")
                is_valid = False
            else:
                user_input = scraped_content
                st.success("✅ คัดลอกเนื้อหาเรียบร้อยแล้ว!")

    elif input_method == "📋 ฟอร์มสร้างโจทย์สำเร็จรูป (Form Builder)":
        if not form_question.strip():
            st.error("❌ กรุณากรอกหัวข้อคำถามในฟอร์มด้วยครับ")
            is_valid = False
        else:
            temp_input = f"[วิชา: {form_subject}] โจทย์: {form_question}\n"
            if has_choices:
                temp_input += f"ชอยส์: A){choice_a} B){choice_b} C){choice_c} D){choice_d}\n"
            if form_instruction.strip():
                temp_input += f"เพิ่มเติม: {form_instruction}\n"
            user_input = temp_input

    elif input_method == "🎯 ให้ AI ออกข้อสอบ 4 ตัวเลือกให้ฉันฝึกทำ":
        if not quiz_topic.strip():
            st.error("❌ กรุณาระบุหัวข้อหลักก่อนส่งออกข้อสอบ")
            is_valid = False
        else:
            user_input = f"สร้างชุดข้อสอบปรนัยหัวข้อเกี่ยวกับ: '{quiz_topic}' จำนวน {quiz_count} ข้อ ระดับความยาก {quiz_level}"

    # ส่งคำสั่งประมวลผล
    if is_valid and user_input.strip():
        try:
            with st.spinner('riendee AI กำลังวิเคราะห์ข้อความและจัดทำคำเฉลย...'):
                
                prompt = (
                    f"จงประมวลผลข้อมูลในโหมด '{mode}' จากข้อความที่ให้ด้านล่างนี้แยกทีละข้อให้ชัดเจน "
                    f"โดยแต่ละข้อต้องประกอบด้วยหัวข้อเหล่านี้ให้ครบถ้วนและห้ามปล่อยว่างเด็ดขาด:\n"
                    f"ข้อที่: [เลขข้อ]\n"
                    f"คำแปลภาษาไทย: [คำแปลตัวโจทย์ภาษาไทย]\n"
                    f"เฉลยข้อที่ถูกต้องที่สุด: [คำเฉลยหรือคำตอบที่ถูกต้องที่สุด]\n"
                    f"หลักการคิดวิเคราะห์: [การวิเคราะห์หลักคิดและเหตุผลอธิบายแบบกระชับเข้าใจง่าย]\n\n"
                    f"นี่คือข้อความที่ต้องนำมาประมวลผล:\n{user_input}"
                )
                
                raw_response = generate_pollinations_ai(prompt)
                
                # แยกบล็อกข้อมูลรายข้อด้วย Regex Split
                blocks = re.split(r'ข้อที่[:\s\d]+|🎯\s*ข้อที่[:\s\d]+', raw_response)
                valid_blocks = [b.strip() for b in blocks if b.strip() and ("แปล" in b or "เฉลย" in b or "คิด" in b)]
                
                if len(valid_blocks) > 0:
                    st.success(f"🎉 แปลและวิเคราะห์สำเร็จทั้งหมด {len(valid_blocks)} ข้อ!")
                    for idx, block in enumerate(valid_blocks, 1):
                        trans_match = re.search(r'คำแปลภาษาไทย\s*:\s*(.*?)(?=เฉลยข้อที่ถูกต้องที่สุด|หลักการคิดวิเคราะห์|$)', block, re.DOTALL)
                        ans_match = re.search(r'เฉลยข้อที่ถูกต้องที่สุด\s*:\s*(.*?)(?=หลักการคิดวิเคราะห์|$)', block, re.DOTALL)
                        explain_match = re.search(r'หลักการคิดวิเคราะห์\s*:\s*(.*)', block, re.DOTALL)
                        
                        txt_trans = trans_match.group(1).strip() if trans_match else "สามารถดูเนื้อหารวมได้ในส่วนวิเคราะห์ด้านล่าง"
                        txt_ans = ans_match.group(1).strip() if ans_match else "วิเคราะห์คำตอบสำเร็จแล้ว"
                        txt_explain = explain_match.group(1).strip() if explain_match else block
                        
                        # แสดงผลในกล่องแบบสลับข้อสวยงาม (ซ่อม syntax บรรทัด st.markdown ที่ขาดหาย)
                        st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                        st.markdown(f"### 🎯 ข้อที่ {idx}")
                        
                        st.markdown("**📝 คำแปลภาษาไทย:**")
                        st.write(txt_trans)
                        
                        st.markdown("**💡 เฉลยข้อที่ถูกต้องที่สุด:**")
                        st.info(txt_ans)
                        
                        st.markdown("**🔬 หลักการคิดวิเคราะห์:**")
                        st.write(txt_explain)
                        st.markdown('</div>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.success("🎉 แปลและวิเคราะห์เนื้อหาเรียบร้อยแล้ว!")
                    st.markdown('<div class="quiz-card">', unsafe_allow_html=True)
                    st.markdown(raw_response)
                    st.markdown('</div>', unsafe_allow_html=True)
                    st.balloons()

        except Exception as e:
            st.error(f"เกิดข้อผิดพลาดในการรันประมวลผล: {str(e)}")
            
    elif input_method == "📝 พิมพ์/วางข้อความเอง" and not user_input.strip():
        st.error("❌ กรุณาป้อนเนื้อหาโจทย์ก่อนกดปุ่มรันระบบ")

# ส่วนท้ายหน้าเว็บของโครงงาน
st.markdown("<br><br><hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #94a3b8; font-size: 13px;'>riendee project - intelligent smart study & translation platform © 2026</p>", unsafe_allow_html=True)