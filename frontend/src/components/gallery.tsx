import React, { useEffect, useState } from "react";
import Masonry from "react-responsive-masonry";
import "~/styles/gallery.css";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

interface ImagesProps {
  images: Record<string, ImageProp>;
}

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height,
  };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(
    getWindowDimensions(),
  );

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowDimensions;
}

const Gallery: React.FC<ImagesProps> = ({ images }) => {
  const { width } = useWindowDimensions();

  const columns = width < 768 ? 1 : width < 1024 ? 2 : 3;
  return (
    <div className="w-full">
      <Masonry columnsCount={columns}>
        {Object.entries(images).map(([i, { image_url, image_drive_id }]) => (
          <a key={i} href={image_drive_id}>
            <div className="img-container">
              <img
                src={image_url}
                style={{ width: "100%", display: "block" }}
                className="display-image p-1"
                alt=""
              />
              <div className="middle">
                <div className="text">Click to view on google drive</div>
              </div>
            </div>
          </a>
        ))}
      </Masonry>
    </div>
  );
};

export default Gallery;
