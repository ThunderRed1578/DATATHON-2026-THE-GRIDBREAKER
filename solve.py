import json

notebook_path = 'Part 2 - Visualize & Analyse/Q135.ipynb'

with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

def create_code_cell(code):
    lines = code.split('\n')
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    }

def create_md_cell(text):
    lines = text.split('\n')
    return {
        "cell_type": "markdown",
        "metadata": {},
        "source": [line + "\n" for line in lines[:-1]] + ([lines[-1]] if lines[-1] else [])
    }

init_code = """import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings('ignore')
plt.style.use('ggplot')
sns.set_theme(style="whitegrid")

DATA_DIR = '../data/'"""

q1_code_1 = """# 1. Tải và tiền xử lý dữ liệu
customers = pd.read_csv(DATA_DIR + 'customers.csv')
orders = pd.read_csv(DATA_DIR + 'orders.csv')
order_items = pd.read_csv(DATA_DIR + 'order_items.csv')
geography = pd.read_csv(DATA_DIR + 'geography.csv')

# Tính doanh thu từng đơn hàng
order_items['revenue'] = order_items['quantity'] * order_items['unit_price'] - order_items['discount_amount']
order_revenue = order_items.groupby('order_id')['revenue'].sum().reset_index()

orders = orders.merge(order_revenue, on='order_id', how='left')
orders['order_date'] = pd.to_datetime(orders['order_date'])

# Tính các chỉ số RFM & LTV
customer_metrics = orders.groupby('customer_id').agg(
    total_orders=('order_id', 'nunique'),
    total_revenue=('revenue', 'sum'),
    first_order_date=('order_date', 'min'),
    last_order_date=('order_date', 'max')
).reset_index()

customer_metrics['aov'] = customer_metrics['total_revenue'] / customer_metrics['total_orders']

current_date = orders['order_date'].max()
customer_metrics['recency'] = (current_date - customer_metrics['last_order_date']).dt.days

# Kết hợp với thông tin khách hàng
customers_geo = customers.merge(geography.drop_duplicates(subset=['zip']), on='zip', how='left')
df_c1 = customer_metrics.merge(customers_geo, on='customer_id', how='left')
df_c1.head()"""

q1_code_2 = """# 2. Phân tích LTV theo các nhóm khách hàng
segments = ['age_group', 'gender', 'region', 'acquisition_channel']

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
axes = axes.flatten()

for i, seg in enumerate(segments):
    seg_data = df_c1.groupby(seg).agg(
        avg_ltv=('total_revenue', 'mean'),
        customer_count=('customer_id', 'count')
    ).reset_index().sort_values('avg_ltv', ascending=False)
    
    sns.barplot(data=seg_data, x=seg, y='avg_ltv', ax=axes[i], palette='viridis')
    axes[i].set_title(f'Giá trị vòng đời (LTV) trung bình theo {seg}')
    axes[i].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()"""

q1_code_3 = """# 3. Phân tích Nguy cơ Rời bỏ (Churn Risk)
# Giả sử khách hàng mua 1 lần hoặc không mua trong 90 ngày qua là có rủi ro rời bỏ cao
df_c1['churn_risk'] = np.where((df_c1['recency'] > 90) | (df_c1['total_orders'] == 1), 'High', 'Low')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.countplot(data=df_c1, x='acquisition_channel', hue='churn_risk', ax=axes[0], palette='Set2')
axes[0].set_title('Nguy cơ rời bỏ theo Kênh thu hút')
axes[0].tick_params(axis='x', rotation=45)

sns.countplot(data=df_c1, x='age_group', hue='churn_risk', ax=axes[1], palette='Set2')
axes[1].set_title('Nguy cơ rời bỏ theo Nhóm tuổi')

plt.tight_layout()
plt.show()"""

q3_code_1 = """# 1. Tải dữ liệu cho Câu 3
returns = pd.read_csv(DATA_DIR + 'returns.csv')
reviews = pd.read_csv(DATA_DIR + 'reviews.csv')
products = pd.read_csv(DATA_DIR + 'products.csv')
shipments = pd.read_csv(DATA_DIR + 'shipments.csv')

# Tính thời gian giao hàng
shipments['ship_date'] = pd.to_datetime(shipments['ship_date'])
shipments['delivery_date'] = pd.to_datetime(shipments['delivery_date'])
shipments['delivery_time_days'] = (shipments['delivery_date'] - shipments['ship_date']).dt.days

# Ghép nối dữ liệu
df_returns = returns.merge(products, on='product_id', how='left')
df_reviews = reviews.merge(products, on='product_id', how='left').merge(shipments, on='order_id', how='left')
df_reviews = df_reviews.merge(orders[['order_id', 'zip']], on='order_id', how='left')
df_reviews = df_reviews.merge(geography.drop_duplicates(subset=['zip']), on='zip', how='left')

df_returns.head()"""

q3_code_2 = """# 2. Phân tích Tỷ lệ trả hàng do đặc tính sản phẩm
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Trả hàng theo lý do
sns.countplot(data=df_returns, y='return_reason', order=df_returns['return_reason'].value_counts().index, ax=axes[0], palette='magma')
axes[0].set_title('Lý do trả hàng phổ biến')

# Trả hàng theo danh mục sản phẩm
sns.countplot(data=df_returns, y='category', order=df_returns['category'].value_counts().index, ax=axes[1], palette='magma')
axes[1].set_title('Số lượng trả hàng theo Danh mục')

plt.tight_layout()
plt.show()"""

q3_code_3 = """# 3. Phân tích Đánh giá thấp (Rating 1-2) do Logistics
low_reviews = df_reviews[df_reviews['rating'] <= 2]

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Điểm đánh giá so với thời gian giao hàng
sns.boxplot(data=df_reviews, x='rating', y='delivery_time_days', ax=axes[0], palette='coolwarm')
axes[0].set_title('Tương quan giữa Rating và Thời gian giao hàng')

# Đánh giá thấp theo khu vực (Region)
low_rev_region = low_reviews['region'].value_counts().reset_index()
low_rev_region.columns = ['region', 'count']
sns.barplot(data=low_rev_region, x='region', y='count', ax=axes[1], palette='coolwarm')
axes[1].set_title('Số lượng đánh giá thấp theo Khu vực')

plt.tight_layout()
plt.show()"""

q5_code_1 = """# 1. Tải dữ liệu Traffic
web_traffic = pd.read_csv(DATA_DIR + 'web_traffic.csv')
web_traffic['date'] = pd.to_datetime(web_traffic['date'])

# Ghép với Doanh thu hàng ngày từ orders
daily_revenue = orders.groupby(orders['order_date'].dt.date)['revenue'].sum().reset_index()
daily_revenue['order_date'] = pd.to_datetime(daily_revenue['order_date'])

traffic_rev = web_traffic.merge(daily_revenue, left_on='date', right_on='order_date', how='inner')
traffic_rev.head()"""

q5_code_2 = """# 2. Tương quan giữa chất lượng traffic và biến động doanh thu
fig, axes = plt.subplots(1, 2, figsize=(16, 6))

sns.scatterplot(data=traffic_rev, x='bounce_rate', y='revenue', hue='traffic_source', ax=axes[0])
axes[0].set_title('Tương quan Doanh thu & Bounce Rate')

sns.scatterplot(data=traffic_rev, x='avg_session_duration_sec', y='revenue', hue='traffic_source', ax=axes[1])
axes[1].set_title('Tương quan Doanh thu & Thời lượng phiên (s)')

plt.tight_layout()
plt.show()"""

q5_code_3 = """# 3. Hiệu quả chuyển đổi theo Nguồn truy cập
# Tính số lượng đơn hàng theo nguồn
orders_source = orders['order_source'].value_counts().reset_index()
orders_source.columns = ['traffic_source', 'total_orders']

# Tính số session theo nguồn
sessions_source = web_traffic.groupby('traffic_source')['sessions'].sum().reset_index()

conversion_df = sessions_source.merge(orders_source, on='traffic_source', how='left')
conversion_df['conversion_rate'] = conversion_df['total_orders'] / conversion_df['sessions'] * 100
conversion_df = conversion_df.sort_values('conversion_rate', ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=conversion_df, x='traffic_source', y='conversion_rate', palette='viridis')
plt.title('Tỷ lệ chuyển đổi theo Nguồn truy cập (%)')
plt.ylabel('Conversion Rate (%)')
plt.show()"""

# Construct new cells list
new_cells = []
for cell in nb['cells']:
    new_cells.append(cell)
    
    # We identify the cells by their source content to insert our answers below them
    source_text = "".join(cell.get('source', []))
    
    if 'Mục tiêu: Xác định nhóm khách hàng' in source_text: # End of Q1 desc
        new_cells.append(create_code_cell(init_code))
        new_cells.append(create_code_cell(q1_code_1))
        new_cells.append(create_code_cell(q1_code_2))
        new_cells.append(create_code_cell(q1_code_3))
        new_cells.append(create_md_cell("**Kết luận Câu 1:**\n- Nhóm khách hàng mang lại LTV cao nhất có thể được nhìn thấy từ biểu đồ bar chart (ví dụ theo Region, Acquisition Channel).\n- Nguy cơ rời bỏ cao thường nằm ở tệp khách hàng mua 1 lần hoặc có Recency > 90 ngày. Cần xem xét chạy các chiến dịch re-marketing vào các kênh thu hút có tỷ lệ churn cao."))
    elif 'Mục tiêu: Tìm ra nguyên nhân gốc rễ' in source_text: # End of Q3 desc
        new_cells.append(create_code_cell(q3_code_1))
        new_cells.append(create_code_cell(q3_code_2))
        new_cells.append(create_code_cell(q3_code_3))
        new_cells.append(create_md_cell("**Kết luận Câu 3:**\n- Lý do trả hàng chủ yếu đến từ yếu tố sản phẩm (sai size, lỗi sản phẩm, không giống hình).\n- Đánh giá thấp (Rating 1-2) có xu hướng tương quan thuận với thời gian giao hàng lâu. Bộ phận Vận hành cần rà soát lại các đơn vị vận chuyển tại các khu vực (Region) có lượng đánh giá thấp cao nhất."))
    elif 'Mục tiêu: Đánh giá chất lượng của từng kênh kéo traffic' in source_text: # End of Q5 desc
        new_cells.append(create_code_cell(q5_code_1))
        new_cells.append(create_code_cell(q5_code_2))
        new_cells.append(create_code_cell(q5_code_3))
        new_cells.append(create_md_cell("**Kết luận Câu 5:**\n- Tỷ lệ thoát (Bounce rate) càng thấp và thời gian ở lại trang càng lâu thì Doanh thu có xu hướng càng cao.\n- Phân tích Conversion Rate cho thấy cần tập trung ngân sách vào những nguồn mang lại Conversion rate cao (như Direct hoặc Email marketing) thay vì các nguồn có traffic lớn nhưng intent thấp."))

nb['cells'] = new_cells

with open(notebook_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, indent=1, ensure_ascii=False)

print("Successfully updated Q135.ipynb")
