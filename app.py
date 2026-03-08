from src.app import create_app

app = create_app()

if __name__ == '__main__':
    print("\n✅ YT Downloader başlatıldı!")
    print("🌐 Tarayıcında aç: http://localhost:5000\n")
    app.run(debug=False, port=5000)
