# Đọc phần này trước

**Đề tài:** Phân tích các sản phẩm thường được mua cùng để hỗ trợ bố trí hàng hóa.

Bộ này làm phần **tiền xử lý**: kiểm tra dữ liệu, xử lý các dòng không phù hợp, gom sản phẩm theo hóa đơn và ghi lại cách làm. Chưa chạy Apriori và chưa có kết luận món nào nên đặt cạnh nhau.

## Thứ tự mở file

1. **`docs/Huong_dan_tien_xu_ly.pdf`**: đọc trang 1-2 trước để hiểu bài; trang 3-4 giải thích việc đã làm; trang 5 chỉ cách xem kết quả; trang 6 chỉ cách chạy lại.
2. **`ket_qua/02_san_pham_trong_tung_hoa_don.csv`**: bảng chính để người làm thuật toán tiếp tục. Cùng mã hóa đơn nghĩa là mua cùng lần.
3. **`docs/Noi_dung_tien_xu_ly_cho_bao_cao.md`**: phần trình bày phương pháp và kết quả, có thể dùng làm bản nháp cho báo cáo nhóm.
4. Khi cần chạy lại, mở **`Tien_xu_ly_Online_Retail.ipynb`**. Notebook là tài liệu có các ô giải thích và các ô lệnh để chạy lần lượt.

## Ba bảng trong thư mục ket_qua

| File | Dùng để làm gì? |
|---|---|
| 01_du_lieu_da_lam_sach.csv | Xem từng dòng hàng, số lượng, ngày mua và giá sau xử lý |
| 02_san_pham_trong_tung_hoa_don.csv | Xem mỗi hóa đơn có những sản phẩm nào; dùng cho bước tìm món mua cùng |
| 03_nhat_ky_xu_ly.csv | Xem từng bước đã loại bao nhiêu dòng và còn lại bao nhiêu |

CSV là dạng bảng, mở được bằng Excel. Các file đã có sẵn kết quả; không phải chạy code mới xem được.

## Nguồn đang sử dụng

Vẫn là **UCI Online Retail**, dữ liệu bán quà tặng trực tuyến ở Anh năm 2010-2011, có khách bán buôn. Đây là nguồn thực hành đề xuất, **không phải dữ liệu WinMart, Circle K hay siêu thị Việt Nam**. Nhóm chưa xác nhận nguồn thay thế trong cuộc trao đổi này. Nếu đổi dữ liệu, phải kiểm tra và xử lý lại, không dùng nguyên các số liệu dưới đây.

Kết quả hiện tại: **478.874 dòng hàng, 17.901 hóa đơn, 3.793 mã sản phẩm**.

## Những file còn lại

- `raw/`: nơi chương trình lưu nguồn gốc. Để bản bàn giao nhẹ hơn, Excel gốc không nằm trong ZIP này. Lần đầu chạy lại, chương trình tự tải từ UCI và kiểm tra file; cần Internet. Ba bảng kết quả đã có sẵn, xem chúng không cần tải thêm.
- `preprocess.py`: chương trình thực hiện việc tiền xử lý; có chú thích bằng tiếng Việt.
- `requirements.txt`: danh sách hai thư viện cần cài khi chạy trên máy.
- `chi_tiet_kiem_tra/`: thông tin để kiểm tra lại khi cần, chưa cần đọc ngay. `dong_da_loai.csv` chỉ vị trí dòng Excel và lý do loại; `cac_cach_viet_ten_hang.csv` ghi các tên theo từng mã hàng; `cac_ma_khong_xep_ke.csv` ghi mã bị loại theo phạm vi; `so_lieu_kiem_tra.json` lưu tổng số liệu cho chương trình.

## Nếu chạy bằng Python trên máy

Giải nén toàn bộ ZIP. Mở Terminal tại thư mục có `preprocess.py`, chạy hai dòng lần lượt:

```bash
python -m pip install -r requirements.txt
python preprocess.py
```

Dùng Python 3.11 trở lên. Lần đầu chạy cần Internet để tải dữ liệu gốc. Sau đó chương trình chỉ đọc file gốc và ghi lại kết quả trong `ket_qua` cùng `chi_tiet_kiem_tra`. Không sửa bằng tay các bảng kết quả rồi chạy lại, vì các thay đổi đó sẽ bị ghi đè.

## Lưu ý khi mở bằng Excel

Nếu toàn bộ dữ liệu dồn vào một cột hoặc chữ bị lỗi: chọn Data (Dữ liệu) > From Text/CSV (Từ văn bản/CSV), chọn mã UTF-8 và dấu phân cách là dấu phẩy. Khi nhập, giữ cột mã hóa đơn và mã sản phẩm ở dạng Text (Văn bản). Không lưu đè file dữ liệu chỉ vì đã lọc để xem.

## Điều đã đổi so với bản trước

Tập trung vào hóa đơn và sản phẩm mua cùng; bỏ phần phân nhóm khách khỏi bộ bàn giao. Tên file, cột dữ liệu và chú thích được viết lại dễ đọc hơn. Giữ cách lọc nguồn để số liệu có thể đối chiếu với bản trước. Bản sửa ngày 05/10/2026.

## Nguồn trích dẫn

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

Trang dữ liệu: https://archive.ics.uci.edu/dataset/352/online+retail

Giấy phép: CC BY 4.0, https://creativecommons.org/licenses/by/4.0/ . Các bảng kết quả trong bộ này đã được xử lý từ bản gốc; cần ghi công nguồn khi đưa vào báo cáo.

## Kiểm tra bản ZIP sửa lỗi

Bản này không kèm file nguồn lớn để giảm dung lượng tải. Đã kiểm tra tải nguồn từ UCI và đọc đủ 541.909 dòng, 8 cột. Các kết quả tiền xử lý giữ nguyên. Bảy ô notebook của bản trước đã chạy và lưu đầu ra; thao tác trực tiếp trên giao diện Colab chưa được kiểm thử.
