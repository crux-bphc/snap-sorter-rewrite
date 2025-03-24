import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../utils/api";
import Gallery from "../components/gallery";
import { useQuery } from "@tanstack/react-query";
import { resultsEndpoint, eventsEndpoint } from "../utils/constants";
import EventDropdown, { Event } from "../components/event-dropdown";
import { useEffect } from "react";
import RequestDownloadDialog from "../components/request-download-dialog";

interface ImageProp {
  image_url: string;
  image_drive_id: string;
}

export type Images = Record<string, ImageProp>;

const fetchEvents = async () => {
  const res = await api.get<{
    events: Event[];
  }>(eventsEndpoint);
  return res.data.events;
};

const fetchResults = async (eventId: number) => {
  const res = await api.get<{ images: Images }>(
    `${resultsEndpoint}?event_id=${eventId}`,
  );
  return res.data;
};

const Results: React.FC = () => {
  const navigate = useNavigate();
  const { data: events, isLoading: isEventsLoading } = useQuery({
    queryKey: ["events"],
    queryFn: fetchEvents,
  });
  const [selectedEvent, setSelectedEvent] = useState<Event | null>(
    events?.[0] ?? null,
  );

  const { data, isLoading } = useQuery({
    queryKey: ["results", selectedEvent?.event_id ?? null],
    queryFn: () => fetchResults(selectedEvent!.event_id),
    enabled: !!selectedEvent?.event_id,
    refetchOnWindowFocus: false,
  });

  useEffect(() => {
    if (!selectedEvent && events?.[0]) setSelectedEvent(events?.[0]);
  }, [events, selectedEvent]);

  return (
    <div className="flex w-full flex-1 items-center justify-center">
      {isEventsLoading || isLoading ? (
        "Loading..."
      ) : events?.length ? (
        <div className="flex flex-col items-center gap-6">
          <div className="flex w-full items-center justify-between">
            <div className="flex items-center gap-4">
              Select event:
              <EventDropdown
                events={events}
                selected={selectedEvent}
                setSelected={setSelectedEvent}
              />
            </div>
            {events.length && <RequestDownloadDialog events={events} />}
          </div>
          {Object.keys(data?.images ?? {}).length > 0 ? (
            <div className="w-[70vw]">
              <Gallery
                images={data?.images ?? {}}
                selectedEventId={selectedEvent?.event_id ?? null}
              />
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
          )}
        </div>
      ) : (
        <div className="flex w-full cursor-pointer items-center justify-center text-xl">
          No events found
        </div>
      )}
    </div>
  );
};

export default Results;
