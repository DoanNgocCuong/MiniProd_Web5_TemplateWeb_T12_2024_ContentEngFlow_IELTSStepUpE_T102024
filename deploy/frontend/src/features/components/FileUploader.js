// frontend/src/components/FileUploader.js
import React from 'react';

// Component cho phép chọn và upload file
function FileUploader({ onFileChange, onUpload, loading, file }) {
    return (
        <div className="upload-section">
            {/* Input cho phép chọn file Excel */}
            <input 
                type="file" 
                onChange={onFileChange}
                accept=".xlsx,.xls"
                disabled={loading}
            />
            
            {/* Nút upload */}
            <button 
                onClick={onUpload}
                disabled={loading || !file}
                className="upload-button"
            >
                {loading ? 'Uploading...' : 'Upload'}
            </button>
        </div>
    );
}

export default FileUploader;