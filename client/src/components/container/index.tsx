import React, { useContext, useState } from "react";
import ReactMarkdown from "react-markdown";

import { AppContext } from "../../context/AppContext";
import FileUpload from "../fileupload";
import { assets } from "../../assets/assets";
import "./container.css";

const Container: React.FC = () => {
  const { handleSendPrompt, chatHistory, isFileUploaded, loading } =
    useContext(AppContext);
  const [prompt, setPrompt] = useState("");

  const handleInputChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setPrompt(event.target.value);
  };

  const handleSendClick = () => {
    handleSendPrompt(prompt);
    setPrompt(""); // Clear prompt input after sending
  };

  const handleKeyDown = (event: React.KeyboardEvent<HTMLInputElement>) => {
    if (event.key === "Enter") {
      event.preventDefault(); 
      handleSendClick(); 
    }
  };

  return (
    <div className="main">
      <div className="nav">
        <p>VigneshDevelops</p>
        <img src={assets.user} alt="" />
      </div>
      <div className="main-container">
        {!isFileUploaded || !chatHistory.length ? (
          <>
            {!isFileUploaded ? (
              <div className="greet">
                <p>
                  <span>Hello, Dev</span>
                </p>
                <p>How can I help you today?</p>
              </div>
            ) : (
              <div className="greet">Start Chat with your docs</div>
            )}
            {!isFileUploaded && <FileUpload />}
          </>
        ) : (
          <>
            {chatHistory.map((chat, index) => (
              <div className="result" key={index}>
                {chat.type === "user_prompt" ? (
                  <div className="result-title">
                    <img src={assets.user_icon} alt="" />
                    <p>{chat.message}</p>
                  </div>
                ) : (
                  <div className="result-data">
                    <img src={assets.gemini_icon} alt="" />
                    {chat.isLoading ? (
                      <div className="loader">
                        <hr />
                        <hr />
                        <hr />
                      </div>
                    ) : (
                      <ReactMarkdown>{chat.message}</ReactMarkdown>
                    )}
                  </div>
                )}
              </div>
            ))}
          </>
        )}

        {/* Input field and button for entering and sending prompts */}
     { isFileUploaded &&  <div className="main-bottom">
          <div className="search-box">
            <input
              type="text"
              placeholder="Enter the prompt here"
              value={prompt}
              onChange={handleInputChange}
              onKeyDown={handleKeyDown}
              disabled={loading} // Disable prompt input during streaming
            />
            <div onClick={handleSendClick} style={{ cursor: "pointer" }}>
              <img src={assets.send_icon} alt="Send" />
            </div>
          </div>
          <div className="bottom-info">
            <p>Ask questions related to the docs you uploaded.</p>
          </div>
        </div>}
      </div>
    </div>
  );
};

export default Container;
