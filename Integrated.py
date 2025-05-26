from flask import Flask, request
import os
from datetime import datetime

app = Flask(__name__)
UPLOAD_FOLDER = './Upload'

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home route with form
@app.route('/')
def index():
    return '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Upload File and Text</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f4f4f4;
            }
            h1, h3 {
                text-align: center;
            }
            form {
                background: white;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                text-align: center;
            }
            textarea {
            width: 100%;   /* 设置宽度为100%（自适应宽度） */
            height: 200px; /* 设置固定高度，适合大多数设备 */
            max-width: 100%; /* 最大宽度为100%（防止超出屏幕） */
            box-sizing: border-box; /* 保证内边距也计算在宽度内 */
        }
            button {
                background-color: #4CAF50;
                color: white;
                padding: 10px 15px;
                border: none;
                border-radius: 5px;
                cursor: pointer;
                font-size: 16px;
            }
            button:hover {
                background-color: #45a049;
            }
        </style>
    </head>
    <body>
        <h1>提交助手</h1>
        <h3>选择需要提交文件或在文本框内输入文本</h3>
        <form action="/upload" method="post" enctype="multipart/form-data">
            <label for="file">请选择您想要提交的文件:</label>
            <h4>⚠️支持多选文件一起上传⚠️</h4>
            <input type="file" name="file" id="file" multiple><br><br>

            <label for="text_content">在这里输入文本👇:</label><br><br>
            <textarea name="text_content" id="text_content"></textarea><br>
            <h4>右下角的小三角可以调整文本框大小</h4>
            <br>


            <button type="submit">提交</button>
            <p>By 李浩铭<p/>
        </form>
    </body>
    </html>
    '''

# Upload route
@app.route('/upload', methods=['POST','GET'])
def upload():
    # 获取多个文件
    files = request.files.getlist('file')

    # 如果没有文件或所有文件为空，则直接返回
    if files or all(file.filename != '' for file in files):
        # 处理文件
        for file in files:
            if file.filename != '':  # 这里保留检查，确保文件有效
                file_path = os.path.join(UPLOAD_FOLDER, file.filename)
                file.save(file_path)

    # Handle text submission
    text_content = request.form.get('text_content', '')
    if text_content:
        # 获取当前时间
        current_time = datetime.now()
        # 使用当前时间生成文件名：小时小时 分钟分钟 秒秒
        file_name = current_time.strftime("%H时%M分钟%S秒%f微秒.txt")
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # 保存文本内容到文件
        with open(file_path, 'w', encoding="utf-8") as text_file:
            text_file.write(text_content)

    # 返回上传成功的页面
    return '''
    <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>提交成功</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f4f4f9;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
        }
        .container {
            text-align: center;
            background-color: #fff;
            border-radius: 10px;
            padding: 30px;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
            width: 300px;
        }
        h1 {
            color: #4CAF50;
            font-size: 40px;
            margin: 0;
            animation: fadeIn 1s ease-out;
        }
        p {
            color: #555;
            font-size: 18px;
            margin-top: 20px;
            animation: fadeIn 2s ease-out;
        }

        .check-icon {
            font-size: 60px;
            color: #4CAF50;
            margin-top: 20px;
            animation: bounce 1.5s infinite;
        }
        .button {
            display: inline-block;
            background-color: #4CAF50;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 5px;
            margin-top: 30px;
            text-decoration: none;
            transition: background-color 0.3s;
        }

        .button:hover {
            background-color: #45a049;
        }
        @keyframes fadeIn {
            0% { opacity: 0; transform: translateY(-10px); }
            100% { opacity: 1; transform: translateY(0); }
        }
        @keyframes bounce {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="check-icon">✔</div>
        <h1>提交成功！</h1>
        <p>您的文件和文本已成功上传。</p>
        <a href="/" class="button">返回首页</a>
    </div>
</body>
</html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)