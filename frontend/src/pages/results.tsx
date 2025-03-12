import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";
import Gallery from "../components/gallery";
import { useQuery } from "@tanstack/react-query";
import { resultsEndpoint, eventsEndpoint } from "../utils/constants";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

type Images = Record<string, ImageProp>;

const fetchEvents = async () => {
  const res = await api.get<{ events: { event_id: number; event_name: string }[] }>(eventsEndpoint);
  return res.data.events;
};

const fetchResults = async (eventId: number) => {
  const res = await api.get<{ images: Images }>(`${resultsEndpoint}?event_id=${eventId}`);
  return res.data;
};

const Results: React.FC = () => {
  const navigate = useNavigate();
  const [eventId, setEventId] = useState<number | null>(null);

  useEffect(() => {
    const getHighestEventId = async () => {
      const events = await fetchEvents();
      if (events.length > 0) {
        const highestEventId = Math.max(...events.map((event) => event.event_id));
        setEventId(highestEventId);
      }
    };
    getHighestEventId();
  }, []);

  const { data, isLoading } = useQuery({
    queryKey: ["results", eventId],
    queryFn: () => fetchResults(eventId!),
    enabled: eventId !== null,
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
