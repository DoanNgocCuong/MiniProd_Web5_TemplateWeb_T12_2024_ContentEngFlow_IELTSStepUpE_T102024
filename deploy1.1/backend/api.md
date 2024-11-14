```bash
input: daily activity
=> 3topic: chị Nhung input 
=> mỗi cái topic theme 6 cụm, 
- Mỗi cụm IPA, meaning English, ảnh cụm, audio cụm, 

- situation -> gen hội thoại 4-6 câu có chứa 1 cụm. 
=> 6 cuộc hội thoại. 
+, situation (output_story): chạy đầu tiên
+, Chọn ảnh 
+, IPA (output_ipa): chạy độc lập 
+, Câu hỏi yes, no ((output_meaning)
- 2 ảnh đối lập thể hiện cụm đấy. 
- IPA cụm 
- 1 câu hỏi về meaning trả về Yes, No, ....(hỏi về nghĩa/fact)
````


Upload

```
curl --location 'http://localhost:5000/upload' \
--form 'file=@"data.xlsx"' \
--form 'file=@"/D:/OneDrive - Hanoi University of Science and Technology/GIT/BÀI-TẬP-IELTS/MiniProd_ContentEngFlow_IELTSStepUpE_T102024/CheckPoint/data - Copy.xlsx"'

```


Dựa vào code trong `backend/api/scripts.py`, đây là các curl commands để test các API scripts:
1. Test chạy script generate_story:
```bash
curl -X POST http://localhost:4999/api/scripts/run/generate_story
```


1. Test chạy script generate_ipa:
```bash
curl -X POST http://localhost:5000/api/scripts/run/generate_ipa
```

2. Test chạy script generate_meaning:
```bash
curl -X POST http://localhost:5000/api/scripts/run/generate_meaning
```



4. Test chạy script generate_pic_answer:
```bash
curl -X POST http://localhost:5000/api/scripts/run/generate_pic_answer
```
5. Test chạy script generate_img_thumbnail:
```bash
curl -X POST http://localhost:5000/api/scripts/run/generate_img_thumbnail
```

Các API này được định nghĩa trong blueprint `scripts` tại:

```13:15:backend/api/scripts.py
SCRIPTS_FOLDER = Path(__file__).parent.parent / 'scripts'

@bp.route('/run/<script_name>', methods=['POST'])
```


Và route handler tại:

```17:46:backend/api/scripts.py
    script_path = SCRIPTS_FOLDER / f'{script_name}.py'
    
    if not script_path.exists():
        logger.error(f'Script not found: {script_name}')
        return jsonify({'error': f'Script {script_name} not found'}), 404
        
    try:
        logger.info(f'Running script: {script_name}')
        result = subprocess.run(
            ['python', str(script_path)],
            capture_output=True,
            text=True,
            cwd=str(SCRIPTS_FOLDER)  # Set working directory to scripts folder
        )
        
        if result.returncode == 0:
            logger.info(f'Script {script_name} completed successfully')
            return jsonify({
                'success': True,
                'message': f'Script {script_name} executed successfully',
                'output': result.stdout
            })
        else:
            logger.error(f'Script {script_name} failed: {result.stderr}')
            return jsonify({
                'success': False,
                'error': result.stderr
            }), 500
            
    except Exception as e:
```


Mỗi request sẽ trả về JSON response với format:
- Success case:
```json
{
    "success": true,
    "message": "Script {script_name} executed successfully",
    "output": "script output here"
}
```

- Error case:
```json
{
    "success": false,
    "error": "error message here"
}

```