from flask import Flask, request, render_template
import os
from datetime import datetime
#图标
app = Flask(__name__, template_folder='.')
UPLOAD_FOLDER = './Upload'

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Home route with form
@app.route('/')
def index():
    return render_template('MainPage.html')

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
    return render_template('UploadSuccess.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
