import streamlit as st
import pandas as pd
from datetime import datetime

# --- 页面配置 ---
st.set_page_config(page_title="爪爪星球 - 记录校园遇见", page_icon="🐾", layout="centered")

# --- 模拟数据库 (实际应用中应连接数据库) ---
if 'page' not in st.session_state:
    st.session_state.page = 'home'
if 'selected_animal' not in st.session_state:
    st.session_state.selected_animal = None

# 模拟动物数据
ANIMALS = [
    {"id": 1, "name": "大黄", "type": "橘猫", "tags": "亲人、贪吃", "status": "已绝育", "desc": "经常出现在图书馆草坪，喜欢晒太阳。", "img": "assets/database/animals/images/test1.jpg"},
    {"id": 2, "name": "点点", "type": "三花", "tags": "胆小、警觉", "status": "未绝育", "desc": "在学五食堂后门出没，对塑料袋声音敏感。", "img": "assets/database/animals/images/test2.jpg"},
]

# 模拟遇见记录
TIMELINE = [
    {"animal_id": 1, "time": "2023-10-24 14:00", "spot": "图书馆前草坪", "note": "它在打盹，超级可爱。"},
    {"animal_id": 1, "time": "2023-10-23 10:30", "spot": "教学楼A座", "note": "路过碰到了。"},
]

# --- 导航函数 ---
def navigate_to(page_name, animal=None):
    st.session_state.page = page_name
    st.session_state.selected_animal = animal
    st.rerun()

# --- 页面逻辑 ---

# 1. 主页 (Home)
if st.session_state.page == 'home':
    st.title("🐾 爪爪星球")
    st.subheader("记录校园里，被温柔遇见的瞬间")
    
    st.info("“记录一次（校园中的）遇见”")
    
    st.markdown("""
    这是一个匿名、公益性质的校园动物记录工具。  
    **我们不鼓励投喂，用手接触动物**，希望通过记录让它们成为校园生活中可被看见的一员。
    """)
    
    st.write("---")
    
    if st.button("🔍 【看看校园里的它们】", use_container_width=True):
        navigate_to('list')
        
    if st.button("📸 【我今天遇见了它】", use_container_width=True):
        navigate_to('submit')
        
    if st.button("❓ 【这个项目是做什么的】", use_container_width=True):
        navigate_to('faq')

    st.caption("""
    * 不需要注册，仅通过第三方登录即可浏览
    * 提交记录将匿名展示
    * 不记录精确位置，不引导喂食或聚集
    """)

# 2. 动物列表页 (List)
elif st.session_state.page == 'list':
    if st.button("← 返回主页"): navigate_to('home')
    st.header("校园萌友录")
    
    for animal in ANIMALS:
        with st.container(border=True):
            col1, col2 = st.columns([1, 2])
            with col1:
                st.image(animal['img'], use_container_width=True)
            with col2:
                st.subheader(animal['name'])
                st.write(f"标签：{animal['tags']}")
                if st.button(f"查看 {animal['name']} 的动态", key=f"btn_{animal['id']}"):
                    navigate_to('detail', animal)

# 3. 动物详情页 (Detail)
elif st.session_state.page == 'detail':
    animal = st.session_state.selected_animal
    if st.button("← 返回列表"): navigate_to('list')
    
    st.header(f"它是：{animal['name']}")
    st.image(animal['img'], caption=f"最近一次被拍到的 {animal['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"**基本信息：** {animal['type']}")
        st.write(f"**状态：** {animal['status']}")
    with col2:
        st.write(f"**性格说明：** {animal['tags']}")

    st.markdown(f"> {animal['desc']}")
    
    st.write("---")
    if st.button("✨ 我今天遇见了它", type="primary", use_container_width=True):
        navigate_to('submit', animal)
    
    st.subheader("🕰 遇见时间线")
    animal_records = [r for r in TIMELINE if r['animal_id'] == animal['id']]
    for record in animal_records:
        with st.chat_message("user", avatar="🐾"):
            st.write(f"**{record['time']}** 在 **{record['spot']}**")
            st.write(record['note'])
            
    st.write("---")
    if st.button("🚩 举报 / 反馈", use_container_width=True):
        navigate_to('report')

# 4. 提交遇见页 (Submit)
elif st.session_state.page == 'submit':
    st.header("记录一次遇见")
    
    with st.form("submit_form"):
        # 如果从详情页进入，默认选中该动物
        default_index = 0
        animal_names = [a['name'] for a in ANIMALS] + ["新面孔（去建档）"]
        if st.session_state.selected_animal:
            default_index = animal_names.index(st.session_state.selected_animal['name'])
            
        target = st.selectbox("你遇见了谁？", options=animal_names, index=default_index)
        spot = st.selectbox("在哪里遇见的？", options=["图书馆草坪", "学五食堂后", "操场看台", "宿舍区", "手动输入..."])
        
        note = st.text_area("想说点什么？(200字以内)", placeholder="例如：它在晒太阳，看起来心情不错。", max_chars=200)
        
        photo = st.file_uploader("上传照片 (如果是新面孔请务必上传)", type=['jpg', 'png', 'jpeg'])
        
        st.caption("🔒 你的提交将匿名展示。点击提交即代表同意合规说明。")
        
        submitted = st.form_submit_button("提交记录")
        if submitted:
            st.balloons() # 撒花庆祝
            st.success("提交成功！")
            # 可以在这里通过 session_state 自动跳回详情页或主页
            # st.session_state.page = 'detail'

    if st.button("取消并返回"): navigate_to('home')

# 5. 说明页 (FAQ)
elif st.session_state.page == 'faq':
    if st.button("← 返回主页"): navigate_to('home')
    st.header("关于爪爪星球")
    st.markdown("""
    ### 为什么要发起这个项目？
    我们希望通过非侵入性的方式，让校园里的流浪猫狗等动物被“看见”。
    
    ### 核心原则
    1. **不干扰原则**：记录而不打扰，远观而不投喂。
    2. **隐私保护**：所有记录匿名化，不公开精确坐标以防恶意伤害。
    3. **健康监测**：通过时间轴观察动物的状态（如是否绝育、是否受伤）。
    
    ### 如何贡献？
    看到它们时，随手拍一张照，选择对应的点位提交即可。
    """)

# 6. 举报/反馈页 (Report)
elif st.session_state.page == 'report':
    st.header("举报与反馈")
    st.write("如果你发现以下情况，请务必告诉我们：")
    
    with st.form("report_form"):
        report_type = st.selectbox("问题类型", ["动物受伤/生病", "未绝育提醒", "人类恶意接触", "内容不当", "其他"])
        detail = st.text_area("详细描述")
        
        if st.form_submit_button("提交反馈"):
            st.warning("反馈已收到，我们会尽快处理。")
            if st.button("返回详情页"): navigate_to('list')