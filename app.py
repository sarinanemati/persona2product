import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import json

st.set_page_config(
    page_title="Persona2Product",
    page_icon="",
    layout="wide"
)


st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Vazirmatn', 'Segoe UI', Tahoma, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #F5F0E8 0%,#FFFFFF 50%, #EDE5D8 100%);
        backgrounf-size: 400% 400%;
        animation: gradientShift 8s ease infinite;
    }
    @keyframes gradientShift {
        0% {
            background-position: 0% 50%;
        }
        50% {
            background-position: 100% 50%;
        }
        100% {
            background-position: 0% 50%;
        }
    }
    
    .main > div {
        backdrop-filter: blur(12px);
        padding: 2rem;
        border-radius: 28px;
        box-shadow: 0 12px 48px rgba(0,0,0,0.06);
        border: 1px solid rgba(255, 255, 255, 0.5);
    }
    
    h1 {
        font-size: 2.8rem;
        background: linear-gradient(135deg, #3D2C1E, #8B6B4D);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        display: inline-block;
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #8B6B4D, #5A3E2B);
        color: white;
        border: none;
        border-radius: 40px;
        padding: 0.7rem 2.2rem;
        font-weight: 500;
        font-family: 'Vazirmatn', sans-serif;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(212, 165, 116, 0.3);
        width: 100%;
    }

    
    .stButton > button:hover {
        transform: translateY(-2px) scale(1.02);
        box-shadow: 0 8px 28px rgba(212, 165, 116, 0.4);
        background: linear-gradient(135deg, #C4956A, #B8895C);
    }
    
.stSelectbox > div > div {
    background: #F5EDE4;  
    border: none;  
    border-radius: 12px;
    font-family: 'Vazirmatn', sans-serif;
    padding: 0.5rem 1rem;
    color: #3D2C1E;  
    transition: all 0.3s ease;
}

.stSelectbox > div > div:hover {
    background: #D4A574
    border-color: #5A3E2B;  
    box-shadow: 0 0 0 4px rgba(139, 107, 77, 0.2);  
}

/* رنگ متن داخل باکس */
.stSelectbox > div > div > div {
    color: #3D2C1E !important;
}

    .product-card {
        background: rgba(255, 253, 249, 0.7);
        backdrop-filter: blur(8px);
        padding: 1.5rem 1.8rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.04);
        transition: all 0.4s cubic-bezier(0.25, 0.46, 0.45, 0.94);
        position: relative;
        overflow: hidden;
        height: 100%;
    }
    
    .product-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, #D4A574, #E8DDD0, #D4A574);
        opacity: 0;
        transition: opacity 0.4s ease;
    }
    
    .product-card:hover {
        transform: translateY(-6px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.08);
        border-color: rgba(212, 165, 116, 0.3);
    }
    
    .product-card:hover::before {
        opacity: 1;
    }
    
    .product-title {
        font-size: 1.15rem;
        font-weight: 700;
        color: #3D2C1E;
        font-family: 'Vazirmatn', sans-serif;
        margin-bottom: 0.3rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .product-title .badge {
        font-size: 0.6rem;
        background: linear-gradient(135deg, #D4A574, #C4956A);
        color: white;
        padding: 0.15rem 0.8rem;
        border-radius: 40px;
        font-weight: 500;
    }
    
    .product-body {
        color: #5A4A3A;
        font-size: 0.92rem;
        line-height: 1.8;
        font-family: 'Vazirmatn', sans-serif;
        margin: 0.5rem 0 0.8rem 0;
        opacity: 0.85;
    }
    
    .product-meta {
        display: flex;
        flex-wrap: wrap;
        gap: 0.8rem 1.5rem;
        color: #8B6B4D;
        font-size: 0.82rem;
        font-family: 'Vazirmatn', sans-serif;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(232, 221, 208, 0.4);
    }
    
    .product-meta span {
        display: flex;
        align-items: center;
        gap: 0.3rem;
    }
    
    .footer {
        text-align: center;
        color: #B5A690;
        font-size: 0.8rem;
        margin-top: 3rem;
        padding: 1.5rem;
        border-top: 1px solid rgba(232, 221, 208, 0.4);
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .stAlert {
        border-radius: 16px;
        backdrop-filter: blur(8px);
        border: 1px solid rgba(255, 255, 255, 0.3);
    }
    
    .stForm {
        background: transparent !important;
        padding: 0 !important;
    }
    
    .stForm > div {
        gap: 0.5rem !important;
    }
</style>
""", unsafe_allow_html=True)


PERSONAS = {
    "برندگرا": {
        "price": 2,
        "rate": 4.5,
        "likes": 30,
        "desc": "به دنبال برندهای معروف و باکیفیت"
    },
    "نظرخوان": {
        "price": 1,
        "rate": 4.0,
        "likes": 40,
        "desc": "به نظرات دیگران و محبوبیت اهمیت می‌دهد"
    },
    "اقتصادی": {
        "price": 0,
        "rate": 3.5,
        "likes": 20,
        "desc": "به دنبال بهترین قیمت و ارزش خرید"
    },
    "عملکردگرا": {
        "price": 1,
        "rate": 4.8,
        "likes": 35,
        "desc": "به قدرت و عملکرد سخت‌افزاری اهمیت می‌دهد"
    },
    "متوسط": {
        "price": 1,
        "rate": 4.0,
        "likes": 30,
        "desc": "ترکیبی از موارد مختلف"
    }
}

def load_user_history():
    history_file = Path(__file__).parent / 'user_history.json'
    if history_file.exists():
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"liked_products": [], "persona_history": []}
    return {"liked_products": [], "persona_history": []}

def save_user_history(history):
    history_file = Path(__file__).parent / 'user_history.json'
    with open(history_file, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def update_weights_based_on_likes(df, history):
    liked_ids = history.get("liked_products", [])
    if not liked_ids:
        return None
    liked_df = df[df['id'].isin(liked_ids)]
    if len(liked_df) == 0:
        return None
    avg_rate = liked_df['rate'].mean()
    avg_likes = liked_df['likes'].mean()
    avg_price = liked_df['price_encoded'].mean() if 'price_encoded' in liked_df.columns else 1
    return {
        'rate_weight': 0.6 + (avg_rate / 10),
        'likes_weight': 0.3 + (avg_likes / 100),
        'price_weight': 0.1 + (1 - avg_price / 3)
    }

def apply_rl_to_recommendations(df, cluster_id, history, top_n=4):
    if 'cluster' not in df.columns:
        return df.head(top_n)
    cluster_df = df[df['cluster'] == cluster_id].copy()
    if len(cluster_df) == 0:
        return df.head(top_n)
    weights = update_weights_based_on_likes(df, history)
    if weights:
        max_likes = cluster_df['likes'].max() + 1
        cluster_df['score'] = (
            cluster_df['rate'] * weights['rate_weight'] +
            (cluster_df['likes'] / max_likes) * weights['likes_weight'] +
            (1 - cluster_df['price_encoded'] / 3) * weights['price_weight']
        )
    else:
        max_likes = cluster_df['likes'].max() + 1
        cluster_df['score'] = cluster_df['rate'] * 0.6 + (cluster_df['likes'] / max_likes) * 0.4
    return cluster_df.nlargest(top_n, 'score')

@st.cache_data
def load_data():
    base = Path(__file__).parent
    data_path = base / 'data' / 'digikala_digital_products.xlsx'
    if not data_path.exists():
        st.error(" فایل داده پیدا نشد")
        return None
    df = pd.read_excel(data_path)
    price_map = {'Low': 0, 'Medium': 1, 'High': 2}
    df['price_encoded'] = df['price_proxy'].map(price_map).fillna(1)
    if 'cluster' not in df.columns:
        df['cluster'] = np.random.randint(0, 4, len(df))
    return df

def find_best_cluster(persona_key, df):
    if 'cluster' not in df.columns:
        return 0
    target = PERSONAS[persona_key]
    price_map = {'Low': 0, 'Medium': 1, 'High': 2}
    df['price_code'] = df['price_proxy'].map(price_map).fillna(1)
    best_cluster = 0
    best_dist = float('inf')
    for c in df['cluster'].unique():
        cluster_data = df[df['cluster'] == c]
        avg_price = cluster_data['price_code'].mean()
        avg_rate = cluster_data['rate'].mean()
        avg_likes = cluster_data['likes'].mean()
        dist = (
            (avg_price - target['price'])**2 +
            (avg_rate - target['rate'])**2 +
            (avg_likes - target['likes'])**2
        )
        if dist < best_dist:
            best_dist = dist
            best_cluster = c
    return int(best_cluster)


df = load_data()
if df is None:
    st.stop()

if 'history' not in st.session_state:
    st.session_state.history = load_user_history()

st.markdown("<h1> Persona2Product</h1>", unsafe_allow_html=True)
st.markdown("find your digital product base on your persona")
st.markdown("---")

total_products = len(df)
avg_rate = round(df['rate'].mean(), 2)
avg_likes = round(df['likes'].mean(), 1)
total_categories = df['category'].nunique()

st.markdown(f"""
<div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 1rem; margin: 1rem 0;">
    <div style="background: rgba(253,251,247,0.6); padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(232,221,208,0.4); text-align: center;">
        <div style="color: #8B6B4D; font-size: 0.85rem; font-family: Vazirmatn;"> تعداد محصولات</div>
        <div style="font-size: 3.2rem; font-weight: 800; color: #3D2C1E; font-family: Vazirmatn; line-height: 1.2;">{total_products}</div>
    </div>
    <div style="background: rgba(253,251,247,0.6); padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(232,221,208,0.4); text-align: center;">
        <div style="color: #8B6B4D; font-size: 0.85rem; font-family: Vazirmatn;"> میانگین امتیاز</div>
        <div style="font-size: 3.2rem; font-weight: 800; color: #3D2C1E; font-family: Vazirmatn; line-height: 1.2;">{avg_rate}</div>
    </div>
    <div style="background: rgba(253,251,247,0.6); padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(232,221,208,0.4); text-align: center;">
        <div style="color: #8B6B4D; font-size: 0.85rem; font-family: Vazirmatn;"> میانگین لایک</div>
        <div style="font-size: 3.2rem; font-weight: 800; color: #3D2C1E; font-family: Vazirmatn; line-height: 1.2;">{avg_likes}</div>
    </div>
    <div style="background: rgba(253,251,247,0.6); padding: 1.2rem; border-radius: 16px; border: 1px solid rgba(232,221,208,0.4); text-align: center;">
        <div style="color: #8B6B4D; font-size: 0.85rem; font-family: Vazirmatn;"> دسته‌ها</div>
        <div style="font-size: 3.2rem; font-weight: 800; color: #3D2C1E; font-family: Vazirmatn; line-height: 1.2;">{total_categories}</div>
    </div>
</div>
""", unsafe_allow_html=True)


liked_count = len(st.session_state.history.get("liked_products", []))
if liked_count > 0:
    print("")
st.markdown("---")


st.subheader("pick your persona")

with st.form(key="persona_form"):
    col_left, col_right = st.columns([3, 1])
    
    with col_left:
        persona = st.selectbox(
            "شخصیت خود را انتخاب کنید:",
            list(PERSONAS.keys()),
            format_func=lambda x: f"{x} - {PERSONAS[x]['desc']}",
            label_visibility="collapsed"
        )
    
    with col_right:
        st.write("")
        st.write("")
        submit_button = st.form_submit_button(
            " دریافت پیشنهادات"
        )

if submit_button:
    with st.spinner("در حال پردازش..."):
        try:
            best_cluster = find_best_cluster(persona, df)
            recommendations = apply_rl_to_recommendations(
                df, best_cluster, st.session_state.history
            )
            
            st.session_state['best_cluster'] = best_cluster
            st.session_state['recommendations'] = recommendations
            st.session_state['persona'] = persona
            
            st.success(f" بهترین خوشه: {best_cluster}")
            st.rerun()
        except Exception as e:
            st.error(f" خطا: {e}")


if 'recommendations' in st.session_state:
    st.markdown("---")
    st.subheader(f"پیشنهاداتی برای تو")
    
    recs = st.session_state['recommendations']
    
    if len(recs) > 0:
        cols = st.columns(2)
        
        for idx, (_, row) in enumerate(recs.iterrows()):
            product_id = int(row['id'])
            is_liked = product_id in st.session_state.history.get("liked_products", [])
            
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="product-card">
                    <div class="product-title">
                         {row['product_name']}
                        <span class="badge">{row['category']}</span>
                    </div>
                    <div class="product-body">{row['body'][:130]}...</div>
                    <div class="product-meta">
                        <span>⭐ {row['rate']}</span>
                        <span>👍 {row['likes']}</span>
                        <span>👎 {row['dislikes']}</span>
                        <span>💰 {row['price_proxy']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # دکمه قلب
                heart_emoji = "❤️" if is_liked else "🤍"
                
                if st.button(
                    heart_emoji,
                    key=f"like_{product_id}_{idx}",
                    help="برای یادگیری سیستم کلیک کنید",
                    use_container_width=True
                ):
                    if product_id in st.session_state.history.get("liked_products", []):
                        st.session_state.history["liked_products"].remove(product_id)
                    else:
                        st.session_state.history["liked_products"].append(product_id)
                    
                    save_user_history(st.session_state.history)
                    weights = update_weights_based_on_likes(df, st.session_state.history)
                    if weights:
                        st.session_state.rl_weights = weights
                    
                    st.rerun()
    else:
        st.info("محصولی برای این شخصیت پیدا نشد.")


if 'rl_weights' in st.session_state:
    with st.expander("prediction system updates", expanded=False):
        st.write("وزن‌های فعلی بر اساس بازخورد شما:")
        st.json(st.session_state.rl_weights)
        
        liked_ids = st.session_state.history.get("liked_products", [])
        if liked_ids:
            liked_products = df[df['id'].isin(liked_ids)]
            st.write("محصولات لایک‌شده:")
            st.dataframe(liked_products[['product_name', 'rate', 'likes', 'price_proxy']])

with st.expander("About Data", expanded=False):
    st.subheader("overview")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("تعداد کل محصولات", len(df))
    with col2:
        st.metric("میانگین امتیاز", f"{df['rate'].mean():.2f}")
    with col3:
        st.metric("بیشترین لایک", df['likes'].max())
    with col4:
        st.metric("دسته‌ها", df['category'].nunique())
    
    try:
        fig = px.bar(
            df['category'].value_counts().reset_index(),
            x='category', y='count',
            title="تعداد محصولات به تفکیک دسته",
            color_discrete_sequence=['#D4A574']
        )
        fig.update_layout(font_family="Vazirmatn", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    except:
        pass
    
    try:
        category_colors = {
            'Smartphone': '#D4A574',   
            'Tablet': '#8B6B4D',       
            'Laptop': '#5A3E2B'       
        }
        fig = px.scatter(
            df, x='rate', y='likes',
            color='category',
            title="ارتباط امتیاز و لایک"
        )
        fig.update_layout(font_family="Vazirmatn", plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
    except:
        pass
    
    try:
        text = ' '.join(df['body'].dropna().tolist()[:100])
        if len(text) > 50:
            wordcloud = WordCloud(
                width=800, height=400,
                background_color="#CCB791",
                colormap='OrRd',
                contour_width=1,
                contour_color='#D4A574'
            ).generate(text)
            fig, ax = plt.subplots(figsize=(10, 5))
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')
            st.pyplot(fig)
    except:
        pass

st.markdown("""
<div class="footer">
made with love | data from Digikala    <br>
    <span style="opacity:0.5; font-size:0.7rem;">ساخته شده توسط سارینا</span>
</div>
""", unsafe_allow_html=True)