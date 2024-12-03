```bash
frontend/
├── public/
│   ├── index.html
├── src/
│   ├── App.js
│   ├── Upload.js
│   ├── index.js
│   ├── App.css (tuỳ chọn)
└── package.json
```

```bash
backend/
├── app.py                    # File chính khởi chạy Flask API
├── requirements.txt          # Danh sách các thư viện cần cài đặt
├── uploads/                  # Thư mục lưu trữ file người dùng tải lên
├── output/                   # Thư mục lưu trữ file kết quả sau khi xử lý
├── utils/                    # Thư mục chứa các tiện ích và hàm phụ trợ
│   ├── file_processing.py    # Xử lý file Excel và tạo dữ liệu JSON
│   ├── data_processing.py    # Các hàm để xử lý dữ liệu
│   └── s3_upload.py          # Hàm upload file lên AWS S3 (tùy chọn)
└── scripts/                  # Thư mục chứa các script Python bạn đã có
    ├── generate_meaning_exercise.py
    ├── gen_answer_pic.py
    ├── generate_audio_conversation.py
    └── ipa_generate.py
```

-------------------------
Update 
```bash
frontend/
├── src/
│   ├── components/
│   │   ├── FileUploader.js
│   │   ├── DataTable.js
│   │   └── ActionButtons.js
│   ├── services/
│   │   └── api.js
│   ├── utils/
│   │   └── dataProcessing.js
│   ├── Upload.js
│   ├── App.js
│   └── styles.css
```

hoặc là backend
```bash
backend/
├── .env                     # File chứa các biến môi trường
├── app.py                   # File chính
├── api/                     # Thư mục chứa các API endpoints
│   ├── __init__.py
│   ├── ipa.py              # API cho IPA generation
│   ├── meaning.py          # API cho meaning exercises
│   ├── story.py            # API cho story generation
│   └── image.py            # API cho image generation
├── services/               # Business logic
│   ├── __init__.py
│   ├── openai_service.py   # OpenAI integration
│   ├── tts_service.py      # Text-to-speech service
│   └── image_service.py    # Image generation service
└── utils/                  # Utilities remain unchanged
```

Đơn giản nên tôi dùng 
```bash
backend/
---api
    --- scripts.py
---scripts
    --- generate_meaning_exercise.py
    --- gen_answer_pic.py
    --- generate_audio_conversation.py
    --- ipa_generate.py
```


-------------------
Update: 
```bash
project/
backend/
|   ├── api/
|   │   ├── __pycache__/
|   │   ├── files/
|   │   │   ├── __pycache__/
|   │   │   ├── __init__.py
|   │   │   ├── routes.py
|   │   │   └── scripts.py
|   │   ├── data/
|   │   └── output/
|   ├── scripts/
|   │   ├── generate_ipa.py
|   │   ├── generate_meaning.py
|   │   └── generate_story.py
|   ├── uploads/
|   │   ├── data_-_Copy.xlsx
|   │   └── data.xlsx
|   ├── .env
|   ├── .gitignore
|   ├── api.md
|   ├── app.py
|   └── config.py
└── frontend/
    ├── public/
    │   ├── index.html
    │   └── favicon.ico
    ├── src/
    │   ├── components/
    │   │   ├── FileUploader.js
    │   │   └── ActionButtons.js
    │   ├── services/
    │   │   └── api.js
    │   ├── utils/
    │   │   └── dataProcessing.js
    │   ├── App.js
    │   ├── Upload.js
    │   └── index.js
    └── package.json

```



project/
backend/
|   ├── api/
|   │   ├── __pycache__/
|   │   ├── files/
|   │   │   ├── __pycache__/
|   │   │   ├── __init__.py
|   │   │   ├── routes.py
|   │   │   └── scripts.py
|   │   ├── data/
|   │   └── output/
|   ├── scripts/
|   │   ├── generate_ipa.py
|   │   ├── generate_meaning.py
|   │   └── generate_story.py
|   ├── uploads/
|   │   ├── data_-_Copy.xlsx
|   │   └── data.xlsx
|   ├── .env
|   ├── .gitignore
|   ├── api.md
|   ├── app.py
|   └── config.py
└── frontend/
    ├── public/
    │   ├── index.html
    │   └── favicon.ico
    ├── src/
    │   ├── components/
    │   │   ├── FileUploader.js
    │   │   └── ActionButtons.js
    │   ├── services/
    │   │   └── api.js
    │   ├── utils/
    │   │   └── dataProcessing.js
    │   ├── App.js
    │   ├── ContentGenerator.js
    │   ├── FileUpload.js
    │   └── index.js
    └── package.json
```


Cấu trúc mới: 
```
frontend/
  ├── src/
  │   ├── services/
  │   │   └── api.js
  │   ├── components/
  │   │   ├── FileUploader.js
  │   │   └── UploadMessage.js
  │   ├── features/
  │   │   ├── ContentGenerator.js
  │   │   └── FileUpload.js
  │   └── App.js
```

