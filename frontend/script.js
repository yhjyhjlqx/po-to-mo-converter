document.getElementById('converter-form').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const fileInput = document.getElementById('po-file');
    const resultDiv = document.getElementById('result');
    const errorDiv = document.getElementById('error');
    
    // 隐藏之前的结果和错误
    resultDiv.classList.add('hidden');
    errorDiv.classList.add('hidden');
    
    if (fileInput.files.length === 0) {
        showError('请选择一个 PO 文件');
        return;
    }
    
    const file = fileInput.files[0];
    const formData = new FormData();
    formData.append('po_file', file);
    
    try {
        const response = await fetch('/api/convert/', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || '转换失败');
        }
        
        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);
        const downloadLink = document.getElementById('download-link');
        
        // 设置下载文件名
        const moFileName = file.name.replace(/\.po$/, '.mo');
        downloadLink.href = downloadUrl;
        downloadLink.download = moFileName;
        
        resultDiv.classList.remove('hidden');
    } catch (error) {
        showError(error.message);
    }
});

function showError(message) {
    const errorDiv = document.getElementById('error');
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}
