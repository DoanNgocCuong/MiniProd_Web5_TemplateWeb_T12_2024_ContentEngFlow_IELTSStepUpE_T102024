import React from 'react';

function ActionButtons({ onSave, loading, filename }) {
    return (
        <div className="action-buttons">
            <button 
                onClick={onSave}
                disabled={loading}
                className="save-button"
            >
                {loading ? 'Saving...' : 'Save Changes'}
            </button>
            <a 
                href={`http://localhost:5000/download/${filename}`}
                download
                className="download-link"
                onClick={(e) => loading && e.preventDefault()}
            >
                Download File
            </a>
        </div>
    );
}

export default ActionButtons; 