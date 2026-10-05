# Tiền xử lý dữ liệu cho bài phân tích sản phẩm mua cùng

Bản nháp nội dung báo cáo - cập nhật ngày 05/10/2026.

**Phạm vi bản nháp:** sử dụng bộ Online Retail đang có. Đây là nguồn đề xuất; nhóm cần xác nhận sử dụng trước khi chốt báo cáo. Phần này chỉ trình bày việc chuẩn bị dữ liệu đã thực hiện, chưa phải kết quả chạy Apriori.

## 1. Mục đích

Đề tài hướng tới việc tìm các sản phẩm thường xuất hiện trong cùng một lần mua, từ đó hỗ trợ đề xuất bố trí hàng hóa. Trước khi phân tích, dữ liệu cần được kiểm tra và sắp xếp lại để xác định đúng sản phẩm trong từng hóa đơn. Vì vậy, phần tiền xử lý tập trung vào mã hóa đơn, mã sản phẩm và thông tin của các dòng mua hàng.

Một hóa đơn có thể gồm nhiều dòng. Mỗi dòng ghi một loại sản phẩm cùng số lượng mua, không đại diện cho một lần mua riêng biệt. Các dòng có cùng mã hóa đơn được xem là thuộc cùng một giỏ hàng.

## 2. Nguồn dữ liệu và phạm vi sử dụng

Bộ Online Retail của UCI gồm 541.909 dòng và 8 cột, ghi nhận giao dịch từ ngày 01/12/2010 đến ngày 09/12/2011. Dữ liệu thuộc một đơn vị bán quà tặng trực tuyến ở Anh, trong đó có khách bán buôn. Các thông tin chính gồm mã hóa đơn, mã và tên sản phẩm, số lượng, thời gian, đơn giá, mã khách hàng và quốc gia.

Trong bản thực hành này, chỉ giữ các dòng có quốc gia là United Kingdom để phân tích trong một thị trường. Dòng thuộc quốc gia khác bị loại do phạm vi đã chọn, không phải vì dữ liệu đó sai. Đồng tiền trong nguồn là bảng Anh (GBP).

Nguồn này có thông tin sản phẩm theo hóa đơn nên dùng được để thực hành phân tích mua cùng. Tuy nhiên, đây không phải dữ liệu siêu thị Việt Nam. Việc vận dụng kết quả vào bố trí hàng hóa chỉ mang tính minh họa, chưa phản ánh hành vi mua sắm tại WinMart hoặc Circle K.

## 3. Các bước xử lý

Trước hết, giữ nguyên file gốc và tạo bản dữ liệu để xử lý. Thêm cột `DongExcelGoc` để tìm lại vị trí của mỗi dòng trong Excel; dòng dữ liệu đầu tiên là dòng 2 vì dòng 1 là tiêu đề. Các mã được đọc như văn bản. Khoảng trắng thừa được bỏ, mã hóa đơn, mã hàng và tên hàng được thống nhất chữ hoa. Tên sản phẩm không được tự dịch hoặc đoán lại.

Sau đó, kiểm tra và lọc lần lượt theo bảng sau. Số dòng bị loại ở mỗi bước chỉ tính trên những dòng còn lại từ bước trước.

| Bước | Nội dung | Trước xử lý | Bị loại | Còn lại |
|---|---|---:|---:|---:|
| 1 | Thiếu mã hóa đơn, mã hàng, ngày, số lượng, đơn giá hoặc quốc gia | 541.909 | 0 | 541.909 |
| 2 | Ngoài phạm vi Anh đã chọn cho bài thực hành | 541.909 | 46.431 | 495.478 |
| 3 | Mã hóa đơn bắt đầu bằng C: hóa đơn hủy theo mô tả nguồn | 495.478 | 7.856 | 487.622 |
| 4 | Số lượng bằng 0 hoặc âm | 487.622 | 1.336 | 486.286 |
| 5 | Đơn giá bằng 0 hoặc âm; ngoài phạm vi hàng có trả tiền | 486.286 | 1.163 | 485.123 |
| 6 | Thiếu tên sản phẩm | 485.123 | 0 | 485.123 |
| 7 | Phí, điều chỉnh, hàng mẫu hoặc phiếu quà tặng | 485.123 | 1.116 | 484.007 |
| 8 | Giữ một bản của dòng trùng đủ 8 thông tin sau thống nhất cách viết | 484.007 | 5.133 | 478.874 |

Các trường được kiểm tra là mã hóa đơn, mã sản phẩm, ngày mua, số lượng, đơn giá và quốc gia. Đây là các thông tin cần cho cách kiểm tra của bộ này; riêng việc tìm sản phẩm mua cùng chủ yếu dựa vào mã hóa đơn và mã sản phẩm.

Mã hóa đơn bắt đầu bằng C được nguồn mô tả là hóa đơn hủy nên không đưa vào bảng các lượt mua được xét. Các dòng có số lượng hoặc đơn giá bằng 0 hay âm cũng bị loại. Với đơn giá bằng 0, việc loại là để giới hạn ở hàng có trả tiền, không khẳng định tất cả đều là lỗi. Các khoản phí, điều chỉnh, hàng mẫu và phiếu quà tặng được loại do không thuộc phạm vi hàng đề xuất xếp kệ. Danh sách mã cụ thể được lưu riêng để kiểm tra.

Với dòng trùng cả 8 thông tin sau khi thống nhất cách viết, chỉ giữ một bản. Đây là giả định thực hành vì nguồn không có mã riêng cho từng dòng hàng để xác nhận tất cả bản lặp đều do nhập sai. Không loại dòng chỉ vì trùng mã hóa đơn hoặc mã sản phẩm. Việc bỏ bản lặp có thể thay đổi tổng số lượng và tiền, nhưng không làm thay đổi sản phẩm có mặt trong từng giỏ hàng.

Các dòng thiếu mã khách vẫn được giữ nếu đáp ứng các điều kiện còn lại, vì bài này cần biết sản phẩm thuộc hóa đơn nào, không cần xác định danh tính người mua. Không điền mã khách giả. Với tên hàng bị thiếu, không tự đoán tên; trong lần chạy này, các dòng thiếu tên đã bị loại bởi những điều kiện trước nên bước lọc thiếu tên không loại thêm dòng nào.

## 4. Tạo bảng sản phẩm theo hóa đơn

Từ dữ liệu đã làm sạch, lấy mã hóa đơn và mã sản phẩm. Mỗi cặp hóa đơn - sản phẩm chỉ giữ một lần. Ví dụ, một hóa đơn mua 3 chiếc cùng mã hàng vẫn chỉ ghi nhận rằng hóa đơn đó có sản phẩm này; số lượng gốc vẫn được lưu trong bảng chi tiết.

Tên hàng được thêm vào để dễ đọc. Khi một mã có nhiều cách viết tên, chọn tên xuất hiện nhiều nhất trong bảng sạch; nếu bằng nhau thì chọn theo thứ tự chữ. Việc nhận diện sản phẩm vẫn dựa trên mã. Không gộp các mã khác nhau chỉ vì tên giống nhau.

Giữ cả hóa đơn chỉ có một loại hàng. Các hóa đơn này vẫn là một phần của tổng số lần mua được xét. Nếu bỏ chúng, tỷ lệ hóa đơn có một nhóm sản phẩm có thể bị tăng lên do mẫu tính bị thu hẹp.

Bảng dùng cho bước tiếp theo có ba cột: `MaHoaDon`, `MaSanPham`, `TenSanPham`. Một dòng là một sản phẩm trong một hóa đơn, không phải toàn bộ giỏ. Người làm thuật toán cần gom theo `MaHoaDon` để lấy danh sách `MaSanPham` trong mỗi giỏ.

## 5. Kết quả và kiểm tra

Sau xử lý còn **478.874 dòng hàng**, thuộc **17.901 hóa đơn**, với **3.793 mã sản phẩm**. Bảng sản phẩm theo hóa đơn có 473.727 cặp hóa đơn - sản phẩm khác nhau. Trong đó có 1.395 hóa đơn chỉ có một loại hàng. Bảng sạch vẫn giữ 129.999 dòng thiếu mã khách, và có 197 mã hàng mang nhiều cách viết tên.

Chương trình đã đối chiếu tổng số dòng bị loại cộng số dòng giữ lại với số dòng nguồn; kiểm tra không đếm một dòng loại hai lần; kiểm tra số lượng và giá đều lớn hơn 0. Toàn bộ cặp hóa đơn - sản phẩm trong bảng dùng phân tích đã được đối chiếu với bảng sạch để bảo đảm không bị mất hoặc thêm sản phẩm khi gom.

Kết quả được lưu thành ba bảng chính: dữ liệu đã làm sạch, sản phẩm trong từng hóa đơn và nhật ký xử lý. Các dòng bị loại có số dòng Excel gốc và lý do để tra lại.

## 6. Giới hạn và công việc tiếp theo

Bộ xử lý chưa ghép từng lượt hoàn hoặc hủy với hóa đơn mua ban đầu. Vì vậy, dữ liệu mô tả các dòng đặt mua có số lượng và giá dương được giữ lại theo quy tắc trên; không nên gọi là toàn bộ giao dịch đã hoàn tất sau hoàn trả.

Bước tiếp theo là dùng Apriori để tìm nhóm sản phẩm xuất hiện cùng nhau đủ thường xuyên, rồi đánh giá các quan hệ mua kèm. Bản này chưa chạy thuật toán, chưa đưa ra cặp sản phẩm cụ thể và chưa chứng minh thay đổi bố trí sẽ làm tăng doanh thu. Khi đề xuất bố trí, cần xét thêm kích thước sản phẩm, điều kiện bảo quản và không gian thực tế.

## Tài liệu tham khảo

Chen, D. (2015). Online Retail [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5BW33

Trang nguồn: https://archive.ics.uci.edu/dataset/352/online+retail . Giấy phép CC BY 4.0: https://creativecommons.org/licenses/by/4.0/ . Bộ kết quả đã được xử lý từ dữ liệu gốc.
