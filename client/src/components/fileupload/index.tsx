import React, { ChangeEvent, useContext, useRef } from "react";
import { AppContext } from "../../context/AppContext";

import "./fileupload.css";

const FileUpload: React.FC = () => {
  const {
    addFiles,
    removeFile,
    uploadedFiles,
    setIsFileUploaded,
    setFileUploadInProgress,
    fileUploadInProgress,
  } = useContext(AppContext);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileUpload = async (event: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(event.target.files || []);

    // Filter allowed file types (PDF, TXT, DOCX)
    const allowedTypes = [
      "application/pdf",
      "text/plain",
      "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    ];
    const validFiles = files.filter((file) => allowedTypes.includes(file.type));

    if (validFiles.length > 0) {
      addFiles(validFiles);
    }
  };

  const uploadFilesToApi = async (files: File[]) => {
    const uploadApiUrl = "http://localhost:8000/api/file";

    const formData = new FormData();
    files.forEach((file) => {
      formData.append("files", file);
    });
    setFileUploadInProgress(true);
    try {
      const response = await fetch(uploadApiUrl, {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Handle the response data as needed (e.g., updating state, showing notifications, etc.)
      const responseData = await response.json();
      console.log("File upload successful:", responseData);
      setIsFileUploaded(true);
    } catch (error) {
      console.error("Error uploading files:", error);
      setIsFileUploaded(false);
    } finally {
      setFileUploadInProgress(false);
    }
  };

  const triggerFileInputClick = () => {
    if (fileInputRef.current) {
      fileInputRef.current.click();
    }
  };

  return (
    <div className="file-upload-container">
      {/* Hidden file input with ref */}
      <input
        type="file"
        multiple
        accept=".pdf, .txt, .docx"
        onChange={handleFileUpload}
        className="file-upload-input"
        ref={fileInputRef}
        style={{ display: "none" }}
      />
      {/* Custom upload button */}
      <button className="upload-button" onClick={triggerFileInputClick}>
        Add File(s)
      </button>
      {/* Display the list of uploaded files */}
      <div className="file-list">
        {uploadedFiles.map((file, index) => (
          <div key={index} className="file-list-item">
            <span>{file.name}</span>
            <button
              onClick={() => removeFile(index)}
              className="file-remove-button"
            >
              &times;
            </button>
          </div>
        ))}
      </div>

      {uploadedFiles.length > 0 && (
        <div className="upload-button-container">
          {/* Upload button with loader */}
          <button
            disabled={fileUploadInProgress}
            className="upload-button"
            onClick={() => uploadFilesToApi(uploadedFiles)}
          >
            {fileUploadInProgress ? (
              <div style={{ display: "flex", paddingRight: 5 }}>
                <span style={{ paddingRight: "10px" }}>Uploading</span>
                <div className="loader">{/* Loader CSS */}</div>
              </div>
            ) : (
              "Upload"
            )}
          </button>
        </div>
      )}
    </div>
  );
};

export default FileUpload;
