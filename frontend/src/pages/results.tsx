import React from "react";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";
import Gallery from "../components/gallery";
import { useQuery } from "@tanstack/react-query";
import { resultsEndpoint } from "../utils/constants";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

type Images = Record<string, ImageProp>;

const fetchResults = async () => {
  const res = await api.get<{ images: Images }>(resultsEndpoint);
  return res.data;
};

const Results: React.FC = () => {
  const navigate = useNavigate();

  const { data, isLoading } = useQuery({
    queryKey: ["results"],
    queryFn: fetchResults,
    refetchOnWindowFocus: false,
  });

  return (
    <div className="flex w-full flex-1 items-center justify-center">
      {!isLoading ? (
        Object.keys(data?.images ?? {}).length > 0 ? (
          <div className="w-[70vw]">
            <Gallery images={data?.images ?? {}} />
          </div>
        ) : (
          <div
            className="flex w-full cursor-pointer items-center justify-center text-xl"
            onClick={() => navigate("/upload")}
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
