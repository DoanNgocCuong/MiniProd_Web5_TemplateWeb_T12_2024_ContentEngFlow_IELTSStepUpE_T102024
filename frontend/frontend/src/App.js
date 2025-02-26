// App.js
import React from 'react';
import FileUpload from './features/FileUpload/FileUpload';
import ContentGenerator from './features/ContentGenerator/ContentGenerator';
import ShowOutput from './features/ShowDownloadOutput/ShowOutput';
import ShowExampleData from './features/ShowInputOutput/ShowExampleData';

function App() {
    return (
        <div className="page-container">
            <h2>Content Generation Tool</h2>
            <FileUpload />
            <ShowExampleData />
            <ContentGenerator />
            <ShowOutput />
        </div>
    );
}

export default App;