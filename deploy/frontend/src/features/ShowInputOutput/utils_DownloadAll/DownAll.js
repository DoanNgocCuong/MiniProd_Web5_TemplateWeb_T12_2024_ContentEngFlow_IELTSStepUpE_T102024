import React, { useState } from 'react';
import { downloadAllAsZip } from '../../../services/api';
import '../ShowOutput.css';

function DownAll() {
    const [downloading, setDownloading] = useState(false);
    const [error, setError] = useState(null);

    const handleDownloadAll = async () => {
        try {
            setDownloading(true);
            setError(null);
            downloadAllAsZip();
        } catch (err) {
            setError('Failed to download files: ' + err.message);
            console.error('Error downloading files:', err);
        } finally {
            setDownloading(false);
        }
    };

    return (
        <div className="download-all-container">
            <button
                onClick={handleDownloadAll}
                disabled={downloading}
                className="download-all-button"
            >
                {downloading ? 'Downloading...' : 'Download All Files'}
            </button>
            {error && <div className="error-message">{error}</div>}
        </div>
    );
}

export default DownAll;