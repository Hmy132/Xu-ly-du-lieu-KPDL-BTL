from pathlib import Path
import hashlib
import json
import platform
import zipfile
import urllib.request
import shutil
import pandas as pd

ROOT = Path(__file__).resolve().parent
COT_GOC = ['InvoiceNo', 'StockCode', 'Description', 'Quantity',
           'InvoiceDate', 'UnitPrice', 'CustomerID', 'Country']
TEN_COT = {
    'SourceExcelRow': 'DongExcelGoc', 'InvoiceNo': 'MaHoaDon',
    'StockCode': 'MaSanPham', 'Description': 'TenSanPham',
    'Quantity': 'SoLuong', 'InvoiceDate': 'NgayMua',
    'UnitPrice': 'DonGiaGBP', 'CustomerID': 'MaKhachHang',
    'Country': 'QuocGia', 'LineAmountGBP': 'ThanhTienGBP',
}

MA_LOAI = {
    'POST': 'Phí bưu điện', 'DOT': 'Phí bưu điện online',
    'C2': 'Phí vận chuyển', 'D': 'Chiết khấu', 'M': 'Điều chỉnh thủ công',
    'BANK CHARGES': 'Phí ngân hàng', 'AMAZONFEE': 'Phí Amazon',
    'CRUK': 'Khoản hoa hồng', 'B': 'Điều chỉnh nợ', 'S': 'Hàng mẫu',
}


def doc_du_lieu():

    tep = ROOT / 'raw' / 'Online Retail.xlsx'
    tep.parent.mkdir(exist_ok=True)
    if not tep.exists():
        tep_zip = tep.parent / 'online_retail_uci.zip'
        if not tep_zip.exists():
            print('Đang tải dữ liệu gốc từ UCI. Bước này cần Internet, chỉ tải lần đầu.')
            tep_tam = tep.parent / 'online_retail_uci.dang_tai'
            try:
                with urllib.request.urlopen(
                    'https://archive.ics.uci.edu/static/public/352/online%2Bretail.zip',
                    timeout=60) as nguon, tep_tam.open('wb') as dich:
                    shutil.copyfileobj(nguon, dich)
                with zipfile.ZipFile(tep_tam) as z:
                    if z.testzip() is not None or 'Online Retail.xlsx' not in z.namelist():
                        raise ValueError('Dữ liệu gốc tải về chưa đầy đủ.')
                tep_tam.replace(tep_zip)
            except Exception as loi:
                tep_tam.unlink(missing_ok=True)
                raise RuntimeError(
                    'Chưa tải được dữ liệu gốc. Kiểm tra Internet rồi chạy lại, '
                    'hoặc tải Online Retail.xlsx từ UCI và đặt vào thư mục raw. '
                    'Các bảng đã làm sạch trong Ket-qua vẫn có thể mở bình thường.') from loi
        with zipfile.ZipFile(tep_zip) as z:
            tep.write_bytes(z.read('Online Retail.xlsx'))
    ma_kiem_tra = hashlib.sha256(tep.read_bytes()).hexdigest()
    if ma_kiem_tra != '43465a06f2ccf7c8b5bd2892bc7defb52f97487934fe93b16ae4c3936424676d':
        raise ValueError('File Excel không khớp bản nguồn đã kiểm tra. Cần kiểm tra lại trước khi chạy.')
    bang = pd.read_excel(tep, dtype={
        'InvoiceNo': 'string', 'StockCode': 'string', 'CustomerID': 'string'})
    if list(bang.columns) != COT_GOC:
        raise ValueError('File nguồn không có đúng 8 cột dự kiến. Cần kiểm tra lại.')
    return bang


def thong_nhat_cach_viet(bang_goc):

    bang = bang_goc.copy()
    bang.insert(0, 'SourceExcelRow', range(2, len(bang) + 2))
    for cot in ['InvoiceNo', 'StockCode', 'CustomerID', 'Description', 'Country']:
        bang[cot] = bang[cot].astype('string').str.strip().replace('', pd.NA)
    for cot in ['InvoiceNo', 'StockCode']:
        bang[cot] = bang[cot].str.upper()
    bang['Description'] = bang.Description.str.replace(r'\s+', ' ', regex=True).str.upper()
    bang['InvoiceDate'] = pd.to_datetime(bang.InvoiceDate, errors='coerce')
    for cot in ['Quantity', 'UnitPrice']:
        bang[cot] = pd.to_numeric(bang[cot], errors='coerce')
    return bang


def lam_sach_du_lieu(bang):

    bang = bang.copy()
    nhat_ky, cac_dong_loai = [], []

    def loai_dong(dieu_kien, ma_ly_do, ly_do):
        nonlocal bang
        dieu_kien = dieu_kien.fillna(True)
        so_dong_truoc = len(bang)
        bi_loai = bang.loc[dieu_kien, ['SourceExcelRow']].copy()
        bi_loai.columns = ['DongExcelGoc']
        bi_loai['MaLyDo'] = ma_ly_do
        bi_loai['LyDo'] = ly_do
        cac_dong_loai.append(bi_loai)
        bang = bang.loc[~dieu_kien].copy()
        nhat_ky.append({
            'Buoc': len(nhat_ky) + 1, 'NoiDung': ly_do,
            'SoDongTruoc': so_dong_truoc,
            'SoDongLoai': so_dong_truoc - len(bang), 'SoDongConLai': len(bang),
        })

    cot_can_co = ['InvoiceNo', 'StockCode', 'InvoiceDate', 'Quantity', 'UnitPrice', 'Country']
    loai_dong(bang[cot_can_co].isna().any(axis=1), 'thieu_thong_tin',
              'Thiếu mã hóa đơn, mã hàng, ngày, số lượng, đơn giá hoặc quốc gia')
    loai_dong(bang.Country.ne('United Kingdom'), 'ngoai_pham_vi',
              'Ngoài phạm vi Anh đã chọn cho bài thực hành')
    loai_dong(bang.InvoiceNo.str.startswith('C'), 'hoa_don_huy',
              'Mã hóa đơn bắt đầu bằng C: hóa đơn hủy theo mô tả nguồn')
    loai_dong(bang.Quantity.le(0), 'so_luong_khong_duong', 'Số lượng bằng 0 hoặc âm')
    loai_dong(bang.UnitPrice.le(0), 'gia_khong_duong',
              'Đơn giá bằng 0 hoặc âm; ngoài phạm vi hàng có trả tiền')
    loai_dong(bang.Description.isna(), 'thieu_ten_hang', 'Thiếu tên sản phẩm')
    loai_dong(bang.StockCode.isin(MA_LOAI) | bang.StockCode.str.startswith('GIFT_'),
              'khong_xep_ke', 'Phí, điều chỉnh, hàng mẫu hoặc phiếu quà tặng')


    loai_dong(bang.duplicated(COT_GOC, keep='first'), 'dong_lap',
              'Giữ một bản của dòng trùng đủ 8 thông tin sau thống nhất cách viết')
    bang['LineAmountGBP'] = bang.Quantity * bang.UnitPrice
    bang = bang.sort_values(['InvoiceDate', 'InvoiceNo', 'StockCode', 'SourceExcelRow'])
    return bang.reset_index(drop=True), pd.DataFrame(nhat_ky), pd.concat(cac_dong_loai, ignore_index=True)


def tao_bang_gio_hang(bang_sach):

    if bang_sach.empty:
        raise ValueError('Không còn dòng mua hàng nào sau lọc. Cần kiểm tra nguồn.')
    cach_viet_ten = (bang_sach.groupby(['StockCode', 'Description']).size()
                    .reset_index(name='SoDong'))
    cach_viet_ten = cach_viet_ten.sort_values(
        ['StockCode', 'SoDong', 'Description'], ascending=[True, False, True])


    ten_hang = cach_viet_ten.drop_duplicates('StockCode')[['StockCode', 'Description']]
    cap_hoa_don_hang = bang_sach[['InvoiceNo', 'StockCode']].drop_duplicates()
    gio_hang = cap_hoa_don_hang.merge(ten_hang, on='StockCode', validate='many_to_one')
    gio_hang = gio_hang.sort_values(['InvoiceNo', 'StockCode']).reset_index(drop=True)
    return gio_hang.rename(columns=TEN_COT), cach_viet_ten.rename(columns=TEN_COT)


def kiem_tra_va_luu(bang_goc, bang_sach, nhat_ky, dong_loai, gio_hang, cach_viet_ten):

    assert nhat_ky.SoDongLoai.sum() + len(bang_sach) == len(bang_goc)
    assert dong_loai.DongExcelGoc.is_unique
    assert bang_sach.SourceExcelRow.is_unique
    assert set(dong_loai.DongExcelGoc).isdisjoint(set(bang_sach.SourceExcelRow))
    assert set(dong_loai.DongExcelGoc) | set(bang_sach.SourceExcelRow) == set(range(2, len(bang_goc) + 2))
    assert not bang_sach.duplicated(COT_GOC).any()
    assert (bang_sach.Quantity > 0).all() and (bang_sach.UnitPrice > 0).all()
    assert not gio_hang.duplicated(['MaHoaDon', 'MaSanPham']).any()

    cap_goc = set(zip(bang_sach.InvoiceNo, bang_sach.StockCode))
    cap_gio = set(zip(gio_hang.MaHoaDon, gio_hang.MaSanPham))
    assert cap_goc == cap_gio
    so_mon = gio_hang.groupby('MaHoaDon').size()
    tom_tat = {
        'ngay_sua': '2026-10-05', 'so_dong_goc': len(bang_goc),
        'so_dong_sach': len(bang_sach), 'so_dong_loai': len(dong_loai),
        'so_hoa_don': int(gio_hang.MaHoaDon.nunique()),
        'so_san_pham': int(gio_hang.MaSanPham.nunique()),
        'so_cap_hoa_don_san_pham': len(gio_hang),
        'so_hoa_don_mot_loai_hang': int(so_mon.eq(1).sum()),
        'so_dong_sach_thieu_ma_khach': int(bang_sach.CustomerID.isna().sum()),
        'so_ma_hang_nhieu_cach_viet_ten': int(bang_sach.groupby('StockCode').Description.nunique().gt(1).sum()),
        'o_trong_trong_nguon': bang_goc.isna().sum().astype(int).to_dict(),
        'ngay_dau_nguon': str(bang_goc.InvoiceDate.min()),
        'ngay_cuoi_nguon': str(bang_goc.InvoiceDate.max()),
        'nguon': 'https://doi.org/10.24432/C5BW33', 'giay_phep': 'CC BY 4.0',
        'pham_vi': 'United Kingdom; số lượng > 0 và đơn giá > 0; bỏ các mã đã nêu',
        'chu_y': [
            'Dữ liệu mua quà tặng trực tuyến tại Anh năm 2010-2011; không phải siêu thị Việt Nam.',
            'Bỏ bản lặp đủ 8 thông tin là giả định thực hành, không khẳng định tất cả là lỗi nguồn.',
            'Chưa ghép các lượt trả hàng với hóa đơn mua ban đầu.',
            'Chỉ chuẩn bị dữ liệu, chưa chạy Apriori và chưa đề xuất vị trí cụ thể.',
        ],
        'sha256_file_excel': hashlib.sha256((ROOT/'raw'/'Online Retail.xlsx').read_bytes()).hexdigest(),
        'phien_ban': {'python': platform.python_version(), 'pandas': pd.__version__},
        'kiem_tra': 'Đạt: tổng dòng, dòng loại, toàn bộ cặp hóa đơn - sản phẩm, số lượng và giá.',
    }
    ket_qua, chi_tiet = ROOT/'Ket-qua', ROOT/'chi_tiet_kiem_tra'
    ket_qua.mkdir(exist_ok=True)
    chi_tiet.mkdir(exist_ok=True)

    def luu_csv(bang, duong_dan):
        bang.to_csv(duong_dan, index=False, encoding='utf-8-sig', date_format='%Y-%m-%d %H:%M:%S')

    luu_csv(bang_sach.rename(columns=TEN_COT), ket_qua/'01_du_lieu_da_lam_sach.csv')
    luu_csv(gio_hang, ket_qua/'02_san_pham_trong_tung_hoa_don.csv')
    luu_csv(nhat_ky, ket_qua/'03_nhat_ky_xu_ly.csv')
    luu_csv(dong_loai, chi_tiet/'dong_da_loai.csv')
    luu_csv(cach_viet_ten, chi_tiet/'cac_cach_viet_ten_hang.csv')
    danh_sach_loai = pd.DataFrame(list(MA_LOAI.items()) + [('GIFT_*', 'Mọi mã bắt đầu bằng GIFT_: phiếu quà tặng')],
                                 columns=['MaSanPham', 'LyDo'])
    luu_csv(danh_sach_loai, chi_tiet/'cac_ma_khong_xep_ke.csv')
    (chi_tiet/'so_lieu_kiem_tra.json').write_text(json.dumps(tom_tat, ensure_ascii=False, indent=2), encoding='utf-8')
    return tom_tat


def main():
    print('1/4 - Đọc file gốc. Có thể mất khoảng một phút hoặc lâu hơn tùy máy.')
    goc = doc_du_lieu()
    print('2/4 - Thống nhất cách viết và lọc dữ liệu.')
    sach, nhat_ky, dong_loai = lam_sach_du_lieu(thong_nhat_cach_viet(goc))
    print('3/4 - Gom các sản phẩm theo hóa đơn.')
    gio, ten = tao_bang_gio_hang(sach)
    print('4/4 - Kiểm tra và lưu kết quả.')
    kq = kiem_tra_va_luu(goc, sach, nhat_ky, dong_loai, gio, ten)
    print(f"Hoàn thành: {kq['so_dong_sach']:,} dòng hàng, {kq['so_hoa_don']:,} hóa đơn, {kq['so_san_pham']:,} sản phẩm.")
    print('Mở thư mục Ket-qua để xem 3 bảng. Chưa chạy Apriori.')


if __name__ == '__main__':
    main()
