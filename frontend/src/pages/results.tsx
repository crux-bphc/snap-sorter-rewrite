import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../components/auth-context";
import { apiFetch } from "../utils/fetch";
import "~/styles/gallery.css";
import Gallery from "../components/gallery";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

interface Images {
  images: {
    [key: string]: ImageProp;
  };
}

const Results: React.FC = () => {
  const navigate = useNavigate();
  const [images, setImages] = useState<Images>({ images: {} });
  const [loaded, setLoaded] = useState(false);
  const { token, isLoading } = useAuth();

  useEffect(() => {
    if (!token) {
      if (!isLoading) {
        navigate("/login");
      }
      return;
    }

    const fetchImages = async () => {
      try {
        const data: Images = await apiFetch<Images>("/get_user_results", {
          token,
        });
        setImages(data);
        setLoaded(true);
        console.log("Set images", data);
      } catch (error) {
        console.error("Failed to fetch images:", error);
      }
    };

    fetchImages();
  }, [token, isLoading, navigate]);

  if (!loaded) {
    return <div>Loading ...</div>;
  }

  return (
    <div className="flex w-full items-center justify-center">
      {Object.keys(images.images).length > 0 ? (
        <div className="w-[70vw]">
          <Gallery images={images.images} />
        </div>
      ) : (
        <div
          className="flex min-h-[calc(100vh-6rem)] w-full items-center justify-center text-xl"
          onClick={() => navigate("/upload")}
          style={{ cursor: "pointer" }}
        >
          {document.referrer.includes("/redirect")
            ? "No images found, please upload your image (click here)"
            : "No images match, please upload a different image (click here)"}
        </div>
      )}
    </div>
  );
};

export default Results;
