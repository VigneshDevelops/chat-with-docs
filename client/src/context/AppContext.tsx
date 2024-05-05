import { createContext, useState, ReactNode, FC } from "react";

// Define the shape of the context state and actions
interface AppContextProps {
  showResults: boolean;
  setShowResults: (value: boolean) => void;
  loading: boolean;
  setLoading: (value: boolean) => void;
  uploadedFiles: File[];
  addFiles: (files: File[]) => void;
  removeFile: (index: number) => void;
  handleSendPrompt: (prompt: string) => void;
  chatHistory: {
    message: string;
    type: "user_prompt" | "ai_response";
    isLoading: boolean;
  }[];
  isFileUploaded: boolean;
  setIsFileUploaded: (value: boolean) => void;
  fileUploadInProgress: boolean;
  setFileUploadInProgress: (value: boolean) => void;
}

const AppContext = createContext<AppContextProps>({
  showResults: false,
  setShowResults: () => {},
  loading: false,
  setLoading: () => {},
  uploadedFiles: [],
  addFiles: () => {},
  removeFile: () => {},
  handleSendPrompt: () => {},
  chatHistory: [],
  isFileUploaded: false,
  setIsFileUploaded: () => {},
  fileUploadInProgress: false,
  setFileUploadInProgress: () => {},
});

const AppProvider: FC<{ children: ReactNode }> = ({ children }) => {
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [chatHistory, setChatHistory] = useState<
    { message: string; type: "user_prompt" | "ai_response", isLoading: boolean; }[]
  >([]);

  const [isFileUploaded, setIsFileUploaded] = useState(false);
  const [fileUploadInProgress, setFileUploadInProgress] = useState(false);

  // Add files to the uploaded files state
  const addFiles = (files: File[]) => {
    setUploadedFiles((prevFiles) => [...prevFiles, ...files]);
  };

  // Remove a file from the uploaded files state
  const removeFile = (index: number) => {
    setUploadedFiles((prevFiles) =>
      prevFiles.filter((_, idx) => idx !== index)
    );
  };

  const handleSendPrompt = async (prompt: string) => {
    setLoading(true);
    setShowResults(true);

    // Add the user's prompt to chat history
    setChatHistory((prevHistory) => [
      ...prevHistory,
      { message: prompt, type: "user_prompt", isLoading: false },
      { message: "", type: "ai_response", isLoading: true },
    ]);

    const chatApiUrl = "http://localhost:8000/api/chat/stream";

    try {
      const response = await fetch(chatApiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ prompt, history: chatHistory }),
      });

      // Check if the response is not OK
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      // Stream the text from the response
      const reader = response.body?.getReader();
      if (reader) {
        let done = false;
        let textData = "";

        while (!done) {
          const { done: readerDone, value } = await reader.read();
          done = readerDone;
          if (value) {
            // Convert the Uint8Array to a string
            const textChunk = new TextDecoder().decode(value);
            textData += textChunk;

            // Update the result data in context

            // Update chat history with streaming AI response
            setChatHistory((prevHistory) => {
              // Find the last entry that is an AI response and update it
              const lastEntryIndex = prevHistory.length - 1;
              const lastEntry = prevHistory[lastEntryIndex];

              if (lastEntry && lastEntry.type === "ai_response") {
                prevHistory[lastEntryIndex] = {
                  message: textData,
                  type: "ai_response",
                  isLoading: false,
                };
                return [...prevHistory];
              }

              // If there is no last AI response entry, add a new one
              return [
                ...prevHistory,
                { message: textData, type: "ai_response", isLoading: false },
              ];
            });
          }
        }
      }
    } catch (error) {
      console.error("Error calling chat API:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AppContext.Provider
      value={{
        showResults,
        setShowResults,
        loading,
        setLoading,
        uploadedFiles,
        addFiles,
        removeFile,
        handleSendPrompt,
        chatHistory,
        isFileUploaded,
        setIsFileUploaded,
        fileUploadInProgress,
        setFileUploadInProgress
      }}
    >
      {children}
    </AppContext.Provider>
  );
};

export { AppContext, AppProvider };
