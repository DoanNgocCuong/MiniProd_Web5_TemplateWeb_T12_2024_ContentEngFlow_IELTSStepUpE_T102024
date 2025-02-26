import React, { useState } from 'react';
import axios from 'axios';
import FileUploader from './components/FileUploader';
import ActionButtons from './components/ActionButtons';
import { uploadFile, saveData, runScriptApi } from './services/api';
import { processUploadResponse } from './utils/dataProcessing';
import './styles.css';

function Upload() {
    const [file, setFile] = useState(null);
    const [data, setData] = useState([]);
    const [filename, setFilename] = useState('');
    const [columns, setColumns] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [scriptStatus, setScriptStatus] = useState({});

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        try {
            console.log('Starting upload process...');
            setLoading(true);
            setError(null);
            
            console.log('Calling uploadFile with:', file);
            const response = await uploadFile(file);
            console.log('Upload response:', response);
            
            console.log('Processing upload response...');
            const { processedData, cols, filename } = processUploadResponse(response);
            console.log('Processed data:', processedData);
            console.log('Columns:', cols);
            console.log('Filename:', filename);
            
            setData(processedData);
            setColumns(cols);
            setFilename(filename);
            console.log('Upload completed successfully');
        } catch (error) {
            console.error('Upload error details:', {
                message: error.message,
                response: error.response,
                stack: error.stack
            });
            setError(error.message);
        } finally {
            setLoading(false);
        }
    };

    const handleSave = async () => {
        try {
            console.log('Starting save process...');
            console.log('Data to save:', data);
            console.log('Filename:', filename);
            
            setLoading(true);
            setError(null);
            const response = await saveData(data, filename);
            console.log('Save response:', response);
            
            alert('File updated successfully!');
        } catch (error) {
            console.error('Save error:', error);
            setError('Error saving changes: ' + error.message);
        } finally {
            setLoading(false);
        }
    };

    const runScript = async (scriptName) => {
        try {
            console.log(`Starting script: ${scriptName}`);
            setLoading(true);
            setError(null);
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'running' }));
            
            const response = await runScriptApi(scriptName);
            console.log(`Script ${scriptName} response:`, response);
            
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'completed' }));
            alert(`${scriptName} executed successfully!`);
        } catch (error) {
            console.error(`Script ${scriptName} error:`, error);
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'error' }));
            setError(`Error running ${scriptName}: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    console.log('Current state:', {
        hasFile: !!file,
        dataLength: data.length,
        filename,
        columnsLength: columns.length,
        loading,
        error,
        scriptStatus
    });

    return (
        <div className="container">
            <FileUploader 
                onFileChange={handleFileChange}
                onUpload={handleUpload}
                loading={loading}
                file={file}
            />

            {error && <div className="error-message">{error}</div>}

            <div className="script-buttons">
                <h3>Generate Content</h3>
                {['generate_story', 'ipa_generate', 'generate_meaning_exercise', 'gen_answer_pic']
                    .map(script => (
                        <button
                            key={script}
                            onClick={() => runScript(script)}
                            disabled={loading}
                            className={`script-button ${scriptStatus[script] || ''}`}
                        >
                            {script.replace(/_/g, ' ').toUpperCase()}
                            {scriptStatus[script] === 'running' && 
                                <span className="loading">...</span>}
                        </button>
                    ))}
            </div>
        </div>
    );
}

export default Upload;
