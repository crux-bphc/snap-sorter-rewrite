import { useMutation, useQueryClient } from "@tanstack/react-query";
import React, { useEffect, useState } from "react";
import Masonry from "react-responsive-masonry";
import api from "../utils/api";
import { falsePositiveEndpoint } from "../utils/constants";
import { AxiosError, isAxiosError } from "axios";

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
  const queryClient = useQueryClient();

  const falsePositiveMutation = useMutation({
    mutationFn: async (image_name: string) =>
      (await api.post<string>(falsePositiveEndpoint + `/${image_name}`)).data,
    onSuccess(_, image_name) {
      queryClient.setQueryData<ImagesProps>(["results"], (prev) => {
        if (!prev) return prev;
        return {
          images: Object.fromEntries(
            Object.entries(prev.images).filter(([key]) => key !== image_name),
          ),
        };
      });
    },
    onError: (e) => {
      let errorMsg = "Upload failed";
      if (isAxiosError(e)) {
        const err: AxiosError<{ detail: string }> = e;
        if (err.response?.data) {
          errorMsg = err.response.data.detail;
        }
      }
      alert(`Error: ${errorMsg}`);
    },
  });

  const handleFalsePositive = (image_name: string) => {
    const res = confirm("Mark image as false positive?");
    if (res) falsePositiveMutation.mutate(image_name);
  };

  const columns = width < 768 ? 1 : width < 1024 ? 2 : 3;
  return (
    <div className="w-full">
      <Masonry columnsCount={columns} gutter="1em">
        {Object.entries(images).map(
          ([image_name, { image_url, image_drive_id }]) => (
            <a
              className="group relative max-h-80 cursor-pointer"
              key={image_name}
              href={image_drive_id}
              target="_blank"
            >
              <img
                src={image_url}
                style={{ width: "100%", display: "block" }}
                className="h-full w-full object-contain transition-opacity duration-300 group-hover:opacity-40"
                alt=""
              />
              <div className="absolute inset-0 flex flex-col justify-center text-center">
                <div className="opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                  Click to view on google drive
                </div>
                <button
                  title="False positive?"
                  onClick={(e) => {
                    e.preventDefault();
                    handleFalsePositive(image_name);
                  }}
                  className="absolute right-2 top-2 z-10 flex h-6 w-6 items-center justify-center rounded-full bg-background/60 opacity-0 transition-opacity duration-300 group-hover:opacity-100"
                >
                  <svg
                    width="1em"
                    height="1em"
                    fill="currentColor"
                    viewBox="0 0 16 16"
                  >
                    <path d="M0 1.75C0 .784.784 0 1.75 0h12.5C15.216 0 16 .784 16 1.75v9.5A1.75 1.75 0 0 1 14.25 13H8.06l-2.573 2.573A1.458 1.458 0 0 1 3 14.543V13H1.75A1.75 1.75 0 0 1 0 11.25zm1.75-.25a.25.25 0 0 0-.25.25v9.5c0 .138.112.25.25.25h2a.75.75 0 0 1 .75.75v2.19l2.72-2.72a.749.749 0 0 1 .53-.22h6.5a.25.25 0 0 0 .25-.25v-9.5a.25.25 0 0 0-.25-.25zm7 2.25v2.5a.75.75 0 0 1-1.5 0v-2.5a.75.75 0 0 1 1.5 0zM9 9a1 1 0 1 1-2 0 1 1 0 0 1 2 0z" />
                  </svg>
                </button>
              </div>
            </a>
          ),
        )}
      </Masonry>
    </div>
  );
};

export default Gallery;
