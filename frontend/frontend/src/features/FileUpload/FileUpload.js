// frontend/src/FileUpload.js
import React, { useState, useRef } from 'react';
import { uploadFile } from '../../services/api';
import ShowExampleData from '../ShowInputOutput/ShowExampleData';
import './FileUpload.css';

function FileUpload() {
    const [uploadState, setUploadState] = useState({
        file: null,
        loading: false,
        message: null,
        isError: false
    });
    
    const fileInputRef = useRef(null);

    const handleButtonClick = async () => {
        if (!uploadState.file) {
            // Nếu chưa có file, mở dialog chọn file
            fileInputRef.current.click();
        } else {
            // Nếu đã có file, tiến hành upload
            try {
                setUploadState(prev => ({ ...prev, loading: true }));
                await uploadFile(uploadState.file);
                setUploadState(prev => ({
                    ...prev,
                    loading: false,
                    message: 'File uploaded successfully!',
                    isError: false,
                    file: null // Reset file sau khi upload thành công
                }));
            } catch (error) {
                setUploadState(prev => ({
                    ...prev,
                    loading: false,
                    message: error.message,
                    isError: true
                }));
            }
        }
    };

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setUploadState(prev => ({
                ...prev,
                file: selectedFile,
                message: null
            }));
        }
    };

    return (
        <div className="upload-container">
            <ShowExampleData />
            <input 
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                style={{ display: 'none' }}
            />
            
            <button 
                className="upload-button"
                onClick={handleButtonClick}
                disabled={uploadState.loading}
            >
                {uploadState.loading ? 'Uploading...' : 
                 uploadState.file ? `Upload ${uploadState.file.name}` : 'Upload File'}
            </button>

            {uploadState.message && (
                <div className={`message ${uploadState.isError ? 'error-message' : 'success-message'}`}>
                    {uploadState.message}
                </div>
            )}
        </div>
    );
}

export default FileUpload;