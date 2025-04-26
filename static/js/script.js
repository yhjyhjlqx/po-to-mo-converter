document.getElementById('convert-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('po-file');
    const file = fileInput.files[0];
    
    if (!file) {
        alert('请先选择 PO 文件！');
        return;
    }
    
    const formData = new FormData();
    formData.append('po-file', file);
    
    try {
        const response = await fetch('/convert', {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            throw new Error('转换失败！');
        }
        
        const blob = await response.blob();
        const downloadUrl = URL.createObjectURL(blob);
        
        const downloadLink = document.getElementById('download-link');
        downloadLink.href = downloadUrl;
        
        document.getElementById('result').classList.remove('hidden');
    } catch (error) {
        alert(error.message);
    }
});
