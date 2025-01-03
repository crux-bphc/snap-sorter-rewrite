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
  const { token } = useAuth();

  useEffect(() => {
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchImages = async () => {
      try {
        const data: Images = await apiFetch<Images>("/get_user_results", {
          token,
        });
        setImages(data);
        console.log("Set images", data);
      } catch (error) {
        console.error("Failed to fetch images:", error);
      }
    };

    fetchImages();
  }, [token, navigate]);

  return (
    <div className="flex w-full items-center justify-center">
      {Object.keys(images.images).length > 0 ? (
        <div className="w-[70vw]">
          <Gallery images={images.images} />
        </div>
      ) : (
        <div>No images found</div>
      )}
    </div>
  );
};

export default Results;
