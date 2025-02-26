import React, { useState, useEffect } from 'react';
import { getOutputFiles, downloadFile } from '../../services/api';
import DownAll from './utils_DownloadAll/DownAll';
import './ShowOutput.css';

function ShowOutput() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // Fetch output files when component mounts
    useEffect(() => {
        fetchOutputFiles();
    }, []);

    const fetchOutputFiles = async () => {
        try {
            setLoading(true);
            setError(null);
            const outputFiles = await getOutputFiles();
            setFiles(outputFiles);
        } catch (err) {
            setError('Failed to load output files: ' + err.message);
            console.error('Error fetching output files:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = (filename) => {
        try {
            downloadFile(filename);
        } catch (err) {
            setError('Failed to download file: ' + err.message);
            console.error('Error downloading file:', err);
        }
    };

    const formatFileSize = (bytes) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    };

    const formatDate = (timestamp) => {
        return new Date(timestamp * 1000).toLocaleString();
    };

    return (
        <div className="output-container">
            <div className="output-header">
                <h3>Output Files</h3>
                <div className="button-group">
                    <button 
                        onClick={fetchOutputFiles} 
                        disabled={loading}
                        className="refresh-button"
                    >
                        {loading ? 'Refreshing...' : 'Refresh'}
                    </button>
                    <DownAll />
                </div>
            </div>

            {error && <div className="error-message">{error}</div>}

            {loading ? (
                <div className="loading-message">Loading files...</div>
            ) : (
                <div className="files-list">
                    {files.length === 0 ? (
                        <div className="no-files">No output files available</div>
                    ) : (
                        files.map((file) => (
                            <div key={file.name} className="file-item">
                                <div className="file-info">
                                    <span className="file-name">{file.name}</span>
                                    <span className="file-size">
                                        {formatFileSize(file.size)}
                                    </span>
                                    <span className="file-date">
                                        {formatDate(file.modified)}
                                    </span>
                                </div>
                                <button
                                    onClick={() => handleDownload(file.name)}
                                    className="download-button"
                                >
                                    Download
                                </button>
                            </div>
                        ))
                    )}
                </div>
            )}
        </div>
    );
}

export default ShowOutput; 