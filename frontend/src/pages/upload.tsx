import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useMutation } from "@tanstack/react-query";
import api from "../utils/api";
import { clusterSamplesEndpoint, uploadEndpoint } from "../utils/constants";
import { AxiosError, isAxiosError } from "axios";
import Select from "../components/select";
import { UploadIcon } from "lucide-react";

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
  detail: string;
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
          errorMsg = err.response.data.detail;
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
          errorMsg = err.response.data.detail;
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
          <fieldset className="flex w-4/5 flex-col items-center justify-center border border-foreground p-8 md:w-2/5 lg:w-2/5">
            <legend className="m-auto flex flex-col items-center justify-center">
              <h1 className="text-lg mt-6 text-center sm:text-4xl">
                UPLOAD YOUR IMAGE
              </h1>
              <p className="flex text-center text-sm md:text-lg">
                Select an image to identify your cluster of photos.
              </p>
            </legend>
          </fieldset>

          <div
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
            className="flex w-4/5 flex-col items-center justify-center gap-4 border-x-[1px] border-b-[1px] border-foreground px-16 py-12 md:w-2/5 lg:w-2/5"
          >
            <input
              type="file"
              id="fileInput"
              accept="image/*"
              onChange={handleFileSelect}
              className="hidden"
            />
            {!preview ? (
              <button
                onClick={() => document.getElementById("fileInput")?.click()}
              >
                <UploadIcon size={48} />
              </button>
            ) : (
              <div>
                <img src={preview} alt="preview" className="mb-2 h-48 w-48" />
              </div>
            )}
            {file ? (
              <div className="flex flex-col gap-7 md:flex-row">
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
        </>
      ) : (
        // <>
        //   <header className="text-center">
        //     <h1 className="text-3xl">UPLOAD YOUR IMAGE</h1>
        //     <p className="mt-2 max-w-md">
        //       Select an image to identify your cluster of photos.
        //     </p>
        //   </header>
        //   <div className="relative">
        //     <label
        //       htmlFor="fileInput"
        //       className="relative flex h-48 w-48 cursor-pointer items-center justify-center border-2 border-dashed border-foreground text-sm text-foreground hover:border-gray-700"
        //       style={{
        //         backgroundImage: preview ? `url(${preview})` : undefined,
        //         backgroundSize: "cover",
        //         backgroundPosition: "center",
        //       }}
        //       onDrop={(event) => {
        //         event.preventDefault();
        //         if (event.dataTransfer.files[0]) {
        //           setFile(event.dataTransfer.files[0]);
        //         }
        //       }}
        //       onDragOver={(event) => {
        //         console.log("hereee :3");
        //         event.preventDefault();
        //       }}
        //       onDragEnter={(event) => {
        //         event.preventDefault();
        //       }}
        //     >
        //       {!preview && "SELECT IMAGE"}
        //     </label>
        //     <input
        //       type="file"
        //       id="fileInput"
        //       accept="image/*"
        //       onChange={handleFileSelect}
        //       className="hidden"
        //     />
        //   </div>
        //   <button
        //     onClick={handleUpload}
        //     className="bg-foreground px-8 py-2 text-lg font-semibold text-background shadow transition-colors hover:bg-gray-400 disabled:bg-red-400"
        //     disabled={!file}
        //     hidden={!file}
        //   >
        //     UPLOAD
        //   </button>
        // </>
        <Select samples={clusterSamples} />
      )}
    </div>
  );
};

export default Upload;
