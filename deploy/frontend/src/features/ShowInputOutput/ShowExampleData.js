import React, { useState, useEffect } from 'react';
import { getExampleFiles, downloadExampleFile } from '../../services/api';

function ShowExampleData() {
    const [files, setFiles] = useState([]);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchExampleFiles();
    }, []);

    const fetchExampleFiles = async () => {
        try {
            setLoading(true);
            const exampleFiles = await getExampleFiles();
            setFiles(exampleFiles);
        } catch (err) {
            console.error('Error fetching example files:', err);
        } finally {
            setLoading(false);
        }
    };

    const handleDownload = (filename) => {
        try {
            downloadExampleFile(filename);
        } catch (err) {
            console.error('Error downloading file:', err);
        }
    };

    if (loading) {
        return <div className="example-corner">Loading...</div>;
    }

    return (
        <div className="example-corner">
            <div className="example-header">
                <h4>Example Files</h4>
                <button 
                    onClick={fetchExampleFiles}
                    className="example-download"
                    style={{ fontSize: '0.7rem' }}
                >
                    ↻
                </button>
            </div>
            <div className="example-list">
                {files.length === 0 ? (
                    <div style={{ fontSize: '0.8rem', textAlign: 'center' }}>
                        No examples available
                    </div>
                ) : (
                    files.map((file) => (
                        <div key={file.name} className="example-item">
                            <span className="example-name">{file.name}</span>
                            <button
                                onClick={() => handleDownload(file.name)}
                                className="example-download"
                            >
                                ↓
                            </button>
                        </div>
                    ))
                )}
            </div>
        </div>
    );
}

export default ShowExampleData;
