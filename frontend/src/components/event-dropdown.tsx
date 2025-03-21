import { useState } from "react";
import { ChevronDown } from "lucide-react";

export interface Event {
  event_id: number;
  event_name: string;
}

interface DropdownProps {
  events: Event[];
  selected: Event | null;
  setSelected: (event: Event | null) => void;
}

const EventDropdown: React.FC<DropdownProps> = ({
  events,
  selected,
  setSelected,
}) => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <div className="relative w-64">
      <button
        className="flex w-full items-center justify-between rounded-lg border bg-background px-4 py-2 shadow"
        onClick={() => setIsOpen(!isOpen)}
      >
        {selected ? selected.event_name : "No events"}
        <ChevronDown className="h-5 w-5" />
      </button>
      {isOpen && (
        <ul className="absolute z-10 mt-1 w-full rounded-lg border bg-background shadow-lg">
          {events.map((event) => (
            <li
              key={event.event_id}
              className="cursor-pointer px-4 py-2 hover:underline"
              onClick={() => {
                setSelected(event);
                setIsOpen(false);
              }}
            >
              {event.event_name}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default EventDropdown;
