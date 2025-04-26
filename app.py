import os
from flask import Flask, request, send_file, render_template
import polib
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert_po_to_mo():
    if 'po-file' not in request.files:
        return '未上传文件', 400
    
    po_file = request.files['po-file']
    if po_file.filename == '':
        return '未选择文件', 400
    
    # 读取 PO 文件并转换为 MO
    po_content = po_file.read().decode('utf-8')
    po = polib.pofile(po_content)
    
    # 生成 MO 文件
    mo_buffer = BytesIO()
    po.save_as_mofile(mo_buffer)
    mo_buffer.seek(0)
    
    return send_file(
        mo_buffer,
        as_attachment=True,
        download_name='output.mo',
        mimetype='application/octet-stream'
    )

if __name__ == '__main__':
    app.run(debug=True)
