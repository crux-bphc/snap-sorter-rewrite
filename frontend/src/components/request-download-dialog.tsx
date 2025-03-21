import { useState } from "react";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "./dialog";
import type { Event } from "./event-dropdown";
import { useMutation } from "@tanstack/react-query";
import api from "../utils/api";
import { requestDownloadEndpoint } from "../utils/constants";

const RequestDownloadDialog = ({ events }: { events: Event[] }) => {
  const [selectedEventIds, setSelectedEventIds] = useState<number[]>([]);
  const [dialogOpen, setIsDialogOpen] = useState(false);

  const toggleEventSelection = (eventId: number) => {
    setSelectedEventIds((prev) =>
      prev.includes(eventId)
        ? prev.filter((id) => id !== eventId)
        : [...prev, eventId],
    );
  };

  const requestDownloadMutation = useMutation({
    mutationFn: async () => {
      return (
        await api.post<{
          message: string;
        }>(requestDownloadEndpoint, selectedEventIds)
      ).data;
    },
    onError: () => {
      alert("An error occurred while requesting download");
    },
    onSuccess: (data) => {
      setIsDialogOpen(false);
      alert(data.message ?? "Success");
    },
  });

  const requestDownload = () => {
    if (selectedEventIds.length === 0) {
      alert("Please select at least one event");
      return;
    }
    requestDownloadMutation.mutate();
  };

  return (
    <Dialog open={dialogOpen} onOpenChange={setIsDialogOpen}>
      <DialogTrigger className="rounded-lg border-2 p-2">
        Download images
      </DialogTrigger>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Download images</DialogTitle>
          <DialogDescription>
            Select all the events you want to download images from
          </DialogDescription>
        </DialogHeader>
        <div className="grid grid-cols-2 gap-4">
          {events.map((event) => (
            <label
              key={event.event_id}
              className="flex cursor-pointer items-center space-x-2"
            >
              <input
                type="checkbox"
                checked={selectedEventIds.includes(event.event_id)}
                onChange={() => toggleEventSelection(event.event_id)}
                className="hidden"
              />
              <div className="flex h-5 w-5 items-center justify-center rounded-md border-2 border-gray-400 transition-all group-hover:border-blue-500 group-hover:shadow-md">
                {selectedEventIds.includes(event.event_id) && (
                  <svg
                    className="h-4 w-4 text-red-500"
                    xmlns="http://www.w3.org/2000/svg"
                    viewBox="0 0 24 24"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M4.293 12.293a1 1 0 011.414 0L10 16.586l8.293-8.293a1 1 0 111.414 1.414l-9 9a1 1 0 01-1.414 0l-5-5a1 1 0 010-1.414z"
                      clipRule="evenodd"
                    />
                  </svg>
                )}
              </div>
              <span className="">{event.event_name}</span>
            </label>
          ))}
        </div>
        <DialogFooter>
          <button className="rounded-lg border-2 p-2" onClick={requestDownload}>
            Download
          </button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default RequestDownloadDialog;
