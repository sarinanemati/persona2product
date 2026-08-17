import pandas as pd
import os

def load_data():
    # مسیر فایل جدید
    file_path = 'persona2product/data/digikala_digital_products.xlsx'
    
    # لود کردن دیتا
    df = pd.read_excel(file_path)
    
    # پاکسازی اولیه (اگر ستون خالی یا نال دارد)
    df = df.dropna(subset=['product_name', 'price_proxy', 'recommender'])
    
    return df

# برای تست سریع
if __name__ == "__main__":
    df = load_data()
    print(f"دیتا با موفقیت لود شد. تعداد سطرها: {len(df)}")
    print(df.head())
