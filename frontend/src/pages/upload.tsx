import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/auth-context";
import { Upload as UploadIcon } from "lucide-react";

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const { token, isLoading } = useAuth();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);

  useEffect(() => {
    if (!isLoading && !token) {
      navigate("/login");
    }
  }, [isLoading, token, navigate]);

  useEffect(() => {
    if (file) {
      const objectUrl = URL.createObjectURL(file);
      setPreview(objectUrl);

      return () => URL.revokeObjectURL(objectUrl);
    }
    setPreview(null);
  }, [file]);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files && event.target.files[0]) {
      setFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!file) {
      alert("Please select a file to upload.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch("http://127.0.0.1:8000/upload", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: formData,
      });

      if (response.ok) {
        const data = await response.json();

        if (Object.keys(data.intermediate_confidence).length === 0) {
          navigate("/results");
        } else {
          localStorage.setItem(
            "intermediateConfidence",
            JSON.stringify(data.intermediate_confidence),
          );
          navigate("/select");
        }
      } else {
        const error = await response.json();
        alert(`Error: ${error.detail || "Upload failed"}`);
      }
    } catch (err) {
      console.error(err);
      alert("An error occurred. Please try again.");
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  return (
    <div className="flex min-h-[calc(100vh-6rem)] flex-col items-center justify-center bg-background p-4 text-foreground">
      <fieldset className="flex w-4/5 flex-col items-center justify-center border border-foreground p-8 md:w-2/5 lg:w-2/5">
        <legend className="m-auto flex flex-col items-center justify-center">
          <h1 className="text-md mt-6 text-center md:text-4xl">
            UPLOAD YOUR IMAGE
          </h1>
          <p className="flex text-center text-sm md:text-lg">
            Select an image to identify your cluster of photos.
          </p>
        </legend>
      </fieldset>

      <div className="flex w-4/5 flex-col items-center justify-center gap-4 border-x-[1px] border-b-[1px] border-foreground px-16 py-12 md:w-2/5 lg:w-2/5">
        <input
          type="file"
          id="fileInput"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
        {!preview ? (
          <button onClick={() => document.getElementById("fileInput")?.click()}>
            <UploadIcon size={48} />
          </button>
        ) : (
          <div>
            <img src={preview} alt="preview" className="mb-2 h-48 w-48" />
          </div>
        )}
        {file ? (
          <div className="flex flex-col gap-8 md:flex-row">
            <button
              onClick={() => {
                setFile(null);
                setPreview(null);
              }}
              className="text-xl hover:text-red-500"
            >
              Remove
            </button>
            <button
              onClick={handleUpload}
              className="text-xl hover:text-green-500"
            >
              Upload
            </button>
          </div>
        ) : (
          <p className="mt-2 text-center text-sm md:text-lg">
            Upload an image from your computer
          </p>
        )}
      </div>
    </div>
  );
};

export default Upload;
