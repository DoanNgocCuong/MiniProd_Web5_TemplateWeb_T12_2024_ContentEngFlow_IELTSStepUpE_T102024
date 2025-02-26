import axios from 'axios';
import config from '../config';

const API_BASE_URL = config.API_BASE_URL;

// APi cho Upload file

export const uploadFile = async (file) => {
    if (!file) throw new Error('Please select a file first');
    
    const formData = new FormData();
    formData.append('file', file);

    const response = await axios.post(`${API_BASE_URL}/api/files/upload`, formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
            'Accept': 'application/json'
        },
        responseType: 'json',
        timeout: 5000
    });
    
    return response;
};


// API cho run script
export const runScriptApi = async (scriptName) => {
    return axios.post(`${API_BASE_URL}/api/scripts/run/${scriptName}`);
}; 


//  API cho Output

// Lấy danh sách files từ output folder
export const getOutputFiles = async () => {
    const response = await fetch(`${API_BASE_URL}/api/files/list/output`);
    const data = await response.json();
    if (!data.success) throw new Error(data.error);
    return data.files;
};

// Download file từ output folder
export const downloadFile = (filename) => {
    window.open(`${API_BASE_URL}/api/files/download/output/${filename}`, '_blank');
};

// Download all files as zip from output folder
export const downloadAllAsZip = () => {
    window.open(`${API_BASE_URL}/api/files/download/output/all`, '_blank');
};

// API cho Example
export const getExampleFiles = async () => {
    const response = await fetch(`${API_BASE_URL}/api/files/list/example`);
    const data = await response.json();
    if (!data.success) throw new Error(data.error);
    return data.files;
};

// Download example file
export const downloadExampleFile = (filename) => {
    window.open(`${API_BASE_URL}/api/files/download/example/${filename}`, '_blank');
};