import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/auth-context";
import api from "../utils/api";
import "~/styles/gallery.css";
import Gallery from "../components/gallery";
import { useQuery } from "@tanstack/react-query";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

interface Images {
  images: {
    [key: string]: ImageProp;
  };
}

const fetchResults = async () => {
  const res = await api.get<Images>("/get_user_results");
  return res.data;
};

const Results: React.FC = () => {
  const navigate = useNavigate();
  const [images, setImages] = useState<Images>({ images: {} });

  const { data, isLoading } = useQuery({
    queryKey: ["results"],
    queryFn: fetchResults,
    refetchOnMount: false,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    if (data) {
      setImages(data);
    }
  }, [data]);

  return (
    <div className="flex w-full flex-1 items-center justify-center">
      {!isLoading ? (
        Object.keys(images.images).length > 0 ? (
          <div className="w-[70vw]">
            <Gallery images={images.images} />
          </div>
        ) : (
          <div
            className="flex w-full items-center justify-center text-xl"
            onClick={() => navigate("/upload")}
            style={{ cursor: "pointer" }}
          >
            {document.referrer.includes("/redirect")
              ? "No images found, please upload your image (click here)"
              : "No images match, please upload a different image (click here)"}
          </div>
        )
      ) : (
        "Loading..."
      )}
    </div>
  );
};

export default Results;
