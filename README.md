# DATATHON 2026 - THE GRIDBREAKER

## Tổng quan

Repository này chứa giải pháp cho cuộc thi Datathon 2026 - thử thách **Sales Forecasting** (Dự báo doanh thu). Dự án sử dụng phương pháp feature-based time series modeling với LightGBM để dự báo Revenue và COGS hàng ngày cho giai đoạn 2023-01-01 đến 2024-07-01.

## Cấu trúc thư mục

```
DATATHON-2026-THE-GRIDBREAKER/
├── README.md                    # File này
├── requirements.txt             # Các thư viện Python cần thiết
├── data/                        # Thư mục chứa dữ liệu thô
│   ├── sales.csv                # Dữ liệu bán hàng lịch sử (dùng để train)
│   ├── sample_submission.csv    # Template định dạng nộp bài
│   └── ...                      # Các file dữ liệu khác
├── Part 1/                      # Bài tập cơ bản
│   ├── ex1.ipynb
│   └── ex1.md
├── Part 2 - Visualize & Analyse/ # Khám phá và phân tích dữ liệu
│   ├── Q123.ipynb
│   └── Q456.ipynb
└── Part 3 - Revenue Prediction Model/ # Model chính
    ├── baseline.ipynb           # Model baseline
    ├── sales-forecasting-model.ipynb # Model dự báo nâng cao
    └── submission.csv          # Kết quả dự báo (output)
```

## Mô tả dữ liệu

| File | Mô tả |
|------|-------|
| `sales.csv` | Dữ liệu bán hàng hàng ngày với các cột Date, Revenue, và COGS |
| `sample_submission.csv` | Template định dạng cho file nộp bài |

## Phương pháp Model

Model dự báo doanh thu sử dụng chiến lược sau:

1. **Data inspection & regime detection**: Khám phá dữ liệu lịch sử để xác định các thay đổi cấu trúc
2. **Feature engineering**: Tạo các features về calendar, cyclical encodings, trend features, và regime indicators
3. **Historical & seasonal profiles**: Tính toán rolling statistics và seasonal patterns
4. **Model training**: LightGBM regressor với target transformations (sqrt/log)
5. **Time-based validation**: Đánh giá trên dữ liệu 2021-2022
6. **Forecasting**: Tạo predictions cho giai đoạn 2023-01-01 đến 2024-07-01

## Cách chạy lại kết quả

### Yêu cầu

Cài đặt các thư viện cần thiết:
```bash
pip install -r requirements.txt
```

### Các bước tạo file submission.csv

1. Di chuyển đến thư mục project:
   ```bash
   cd DATATHON-2026-THE-GRIDBREAKER
   ```

2. Mở file ```sales-forecasting-model.ipynb``` trong thư mục ```Part 3 - Revenue Prediction Model```.

3. Chạy toàn bộ notebook, notebook sẽ thực hiện:
   - Load và inspect dữ liệu bán hàng từ `data/sales.csv`
   - Engineer features (calendar, trend, seasonality)
   - Train model LightGBM
   - Validate trên dữ liệu 2021-2022
   - Generate predictions cho 2023-2024
   - Export kết quả ra `submission.csv`

5. File output: `Part 3 - Revenue Prediction Model/submission.csv`

### Kết quả mong đợi

File `submission.csv` sẽ chứa các predictions với các cột:
- **Date**: Ngày từ 2023-01-01 đến 2024-07-01
- **Revenue**: Doanh thu dự báo hàng ngày
- **COGS**: Chi phí hàng bán dự báo hàng ngày

## Các thông số quan trọng

| Thông số | Giá trị |
|----------|---------|
| Giai đoạn train | Đến 2022-12-31 |
| Giai đoạn dự báo | 2023-01-01 đến 2024-07-01 |
| Giai đoạn validation | 2021-01-01 đến 2022-12-31 |
| Model | LightGBM Regressor |

## Thành viên nhóm

| STT | Họ và tên              | Email                            |
|-----|------------------------|----------------------------------|
| 1   | Nguyễn Lê Tấn Phát     | phatle1578@gmail.com             |
| 2   | Nguyễn Nhật Trường     | truong.nhat3040@gmail.com        |
| 3   | Dương Ngọc Kiều Trinh  | duongngockieutrinh0303@gmail.com |
| 4   | Nguyễn Phạm Tú Uyên    | nguyenphamtuuyen0101@gmail.com   |
