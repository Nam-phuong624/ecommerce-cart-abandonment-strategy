import os
import subprocess
import urllib.request
import sys

def install_kaggle():
    try:
        import kaggle
    except ImportError:
        print("Installing Kaggle CLI...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "kaggle", "--user"])

def download_kaggle(dataset, target_dir):
    print(f"[{dataset}] Bắt đầu tải từ Kaggle (có thể mất vài phút cho file lớn)...")
    import kaggle
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(dataset, path=target_dir, unzip=True)
    print(f"[{dataset}] Tải và giải nén thành công!")

def download_file(url, target_path):
    print(f"Downloading từ {url}...")
    urllib.request.urlretrieve(url, target_path)
    print(f"Đã lưu tại {target_path}")

def main():
    install_kaggle()
    
    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    raw_data_dir = os.path.join(base_dir, 'data', 'raw')
    os.makedirs(raw_data_dir, exist_ok=True)
    
    # 1. MMM Dataset (Figshare)
    mmm_data_url = "https://ndownloader.figshare.com/files/46779652"
    mmm_dict_url = "https://ndownloader.figshare.com/files/44743624"
    download_file(mmm_data_url, os.path.join(raw_data_dir, "conjura_mmm_data.csv"))
    download_file(mmm_dict_url, os.path.join(raw_data_dir, "conjura_mmm_data_dictionary.xlsx"))
    
    # 2. Kaggle Datasets
    os.environ['KAGGLE_CONFIG_DIR'] = os.path.expanduser('~/.kaggle')
    
    rees46_dataset = "mkechinov/ecommerce-behavior-data-from-multi-category-store"
    amazon_dataset = "thedevastator/amazon-customer-reviews-with-2013-2019-sentiment"
    
    download_kaggle(amazon_dataset, raw_data_dir)
    download_kaggle(rees46_dataset, raw_data_dir)
    
    print("\nHOÀN TẤT TẢI DỮ LIỆU! Các file đã nằm trong thư mục data/raw/")

if __name__ == "__main__":
    main()
