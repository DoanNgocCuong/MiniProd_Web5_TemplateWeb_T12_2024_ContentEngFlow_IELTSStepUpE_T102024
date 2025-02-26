// ContentGenerator.js - Component for generating different types of content through scripts
import React, { useState } from 'react';
import { runScriptApi } from '../../services/api';
import './ContentGenerator.css';

function ContentGenerator() {
    // States for managing script execution
    const [loading, setLoading] = useState(false); // Tracks if any script is running
    const [error, setError] = useState(null); // Stores any error messages
    const [scriptStatus, setScriptStatus] = useState({}); // Tracks status of each script

    // List of available scripts that can be run
    const scripts = ['generate_story', 'generate_ipa', 'generate_meaning'];

    // Function to run a single script
    // Takes scriptName as parameter and executes the corresponding script
    const runScript = async (scriptName) => {
        try {
            console.log(`Starting script: ${scriptName}`);
            setLoading(true);
            setError(null);
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'running' }));
            
            // Call API to run the script
            const response = await runScriptApi(scriptName);
            console.log(`Script ${scriptName} response:`, response);
            
            // Update status on successful completion
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'completed' }));
            alert(`${scriptName} executed successfully!`);
        } catch (error) {
            console.error(`Script ${scriptName} error:`, error);
            setScriptStatus(prev => ({ ...prev, [scriptName]: 'error' }));
            setError(`Error running ${scriptName}: ${error.message}`);
            throw new Error(`Error running ${scriptName}: ${error.message}`);
        } finally {
            setLoading(false);
        }
    };

    // Function to run all scripts at once
    // Uses Promise.all to run scripts in parallel
    // Nếu có 1 script bị lỗi, các script khác vẫn tiếp tục chạy
    // Vì Promise.all không bị hủy khi có lỗi
    const runAll = async () => {
        setError(null);

        try {
            await Promise.all(scripts.map(script => runScript(script)));
        } catch (error) {
            console.error('Error running scripts:', error);
            setError('Error running scripts: ' + error.message);
        }
    };

    // Render the component UI
    return (
        <div className="generator-container">
            <h3>Generate Content</h3>
            <div className="script-buttons">
                {/* Button to run all scripts */}
                <button
                    onClick={runAll}
                    disabled={loading}
                    className="run-all-button"
                >
                    RUN ALL
                    {loading && <span className="loading">...</span>}
                </button>
                {/* Create buttons for each individual script */}
                {scripts.map(script => (
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
            {/* Display any error messages */}
            {error && <div className="error-message">{error}</div>}
        </div>
    );
}

export default ContentGenerator;