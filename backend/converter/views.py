from django.http import FileResponse, JsonResponse
from django.views.decorators.http import require_POST
import gettext
import os
import tempfile
import magic

@require_POST
def convert_po_to_mo(request):
    if 'po_file' not in request.FILES:
        return JsonResponse({'error': 'No PO file provided'}, status=400)
    
    po_file = request.FILES['po_file']
    
    # 验证文件类型
    file_type = magic.from_buffer(po_file.read(1024), mime=True)
    po_file.seek(0)
    
    if file_type not in ['text/plain', 'application/x-gettext', 'text/x-po']:
        return JsonResponse({'error': 'Invalid file type. Please upload a PO file.'}, status=400)
    
    try:
        # 创建临时目录
        with tempfile.TemporaryDirectory() as temp_dir:
            po_path = os.path.join(temp_dir, 'temp.po')
            mo_path = os.path.join(temp_dir, 'temp.mo')
            
            # 保存上传的PO文件
            with open(po_path, 'wb+') as destination:
                for chunk in po_file.chunks():
                    destination.write(chunk)
            
            # 转换PO到MO
            with open(po_path, 'rb') as po_file_obj:
                po = gettext.GNUTranslations(po_file_obj)
            
            with open(mo_path, 'wb') as mo_file_obj:
                po._output(mo_file_obj)
            
            # 返回MO文件
            response = FileResponse(open(mo_path, 'rb'), content_type='application/x-gettext')
            response['Content-Disposition'] = 'attachment; filename="converted.mo"'
            return response
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
