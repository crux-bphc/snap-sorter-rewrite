import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/auth-context";

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
      <header className="mb-6 text-center">
        <h1 className="text-3xl">UPLOAD YOUR IMAGE</h1>
        <p className="mt-2 max-w-md">
          Select an image to identify your cluster of photos.
        </p>
      </header>
      <div className="relative mb-4">
        <div
          className="relative flex h-48 w-48 cursor-pointer items-center justify-center border-2 border-dashed border-foreground hover:border-gray-700"
          onClick={() => document.getElementById("fileInput")?.click()}
          style={{
            backgroundImage: preview ? `url(${preview})` : undefined,
            backgroundSize: "cover",
            backgroundPosition: "center",
          }}
        >
          {!preview && (
            <span className="text-sm text-foreground">SELECT IMAGE</span>
          )}
        </div>
        <input
          type="file"
          id="fileInput"
          accept="image/*"
          onChange={handleFileSelect}
          className="hidden"
        />
      </div>
      <button
        onClick={handleUpload}
        className="bg-foreground px-8 py-2 text-lg font-semibold text-background shadow transition-colors hover:bg-gray-400 disabled:bg-red-400"
        disabled={!file}
        hidden={!file}
      >
        UPLOAD
      </button>
    </div>
  );
};

export default Upload;
