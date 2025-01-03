import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import api from "../utils/api";
import { clusterSamplesEndpoint, uploadEndpoint } from "../utils/constants";
import { AxiosError, isAxiosError } from "axios";
import Select from "../components/select";

interface Cluster {
  cluster: number;
  images: string[];
}
type IntermediateConfidence = Record<number, Cluster>;

type ClusterSamples = Record<
  string,
  {
    cluster: number;
    sample_url: string;
    images: string[];
  }
>;

interface ErrorData {
  detail: {
    loc: (string | number)[];
    msg: string;
    type: string;
  }[];
}

const Upload: React.FC = () => {
  const navigate = useNavigate();
  const [file, setFile] = useState<File | null>(null);
  const [preview, setPreview] = useState<string | null>(null);
  const [clusterSamples, setClusterSamples] = useState<ClusterSamples>();

  const uploadMutation = useMutation({
    mutationFn: async (body: FormData) => {
      return await api.post<{
        high_confidence: string[];
        intermediate_confidence: IntermediateConfidence;
      }>(uploadEndpoint, body);
    },
    onSuccess: (data) => {
      const intermediateConfidence = data.data.intermediate_confidence;
      if (!Object.keys(intermediateConfidence).length) {
        navigate("/results");
      } else {
        localStorage.setItem(
          "intermediateConfidence",
          JSON.stringify(intermediateConfidence),
        );
        getSamplesMutation.mutate(intermediateConfidence);
      }
    },
    onError: (e) => {
      let errorMsg = "Upload failed";
      if (isAxiosError(e)) {
        const err: AxiosError<ErrorData> = e;
        if (err.response?.data) {
          errorMsg = err.response.data.detail[0].msg;
        }
      }
      alert(`Error: ${errorMsg}`);
    },
  });

  const getSamplesMutation = useMutation({
    mutationFn: async (intermediateConfidence: IntermediateConfidence) => {
      const res = await api.post<ClusterSamples>(
        clusterSamplesEndpoint,
        intermediateConfidence,
      );
      return res.data;
    },
    onSuccess: (data) => {
      setClusterSamples(data);
    },
    onError: (e) => {
      let errorMsg = "Upload failed";
      if (isAxiosError(e)) {
        const err: AxiosError<ErrorData> = e;
        if (err.response?.data) {
          errorMsg = err.response.data.detail[0].msg;
        }
      }
      alert(`Error: ${errorMsg}`);
    },
  });

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

    const formData = new FormData();
    formData.append("file", file);

    uploadMutation.mutate(formData);
  };

  return (
    <div className="flex flex-1 flex-col items-center justify-center bg-background p-4 text-foreground">
      {!clusterSamples ? (
        <>
          <header className="mb-6 text-center">
            <h1 className="text-3xl">UPLOAD YOUR IMAGE</h1>
            <p className="mt-2 max-w-md">
              Select an image to identify your cluster of photos.
            </p>
          </header>
          <div className="relative mb-4">
            <label
              htmlFor="fileInput"
              className="relative flex h-48 w-48 cursor-pointer items-center justify-center border-2 border-dashed border-foreground text-sm text-foreground hover:border-gray-700"
              style={{
                backgroundImage: preview ? `url(${preview})` : undefined,
                backgroundSize: "cover",
                backgroundPosition: "center",
              }}
              onDrop={(event) => {
                event.preventDefault();
                if (event.dataTransfer.files[0]) {
                  setFile(event.dataTransfer.files[0]);
                }
              }}
              onDragOver={(event) => {
                console.log("hereee :3");
                event.preventDefault();
              }}
              onDragEnter={(event) => {
                event.preventDefault();
              }}
            >
              {!preview && "SELECT IMAGE"}
            </label>
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
        </>
      ) : (
        <Select images={clusterSamples} />
      )}
    </div>
  );
};

export default Upload;
