import React from "react";
import { useQuery } from "@tanstack/react-query";
import api from "../utils/api";
import { announcementsEndpoint } from "../utils/constants";

const fetchAnnouncements = async () => {
  const res = await api.get<{ announcements: string[] }>(announcementsEndpoint);
  return res.data.announcements;
};

const Dashboard: React.FC = () => {
  const { data: announcements, isLoading } = useQuery({
    queryKey: ["announcements"],
    queryFn: fetchAnnouncements,
  });

  return (
    <div className="flex flex-col items-center">
      <h1 className="mb-16 text-4xl tracking-widest">D A S H B O A R D</h1>

      <div className="m-auto w-full max-w-[90%] md:max-w-4xl">
        <div className="mb-8">
          <h2 className="mb-4 text-right text-2xl">Announcements</h2>
          <div className="border border-white p-4">
            {isLoading ? (
              <p>Loading...</p>
            ) : announcements?.length ? (
              announcements.map((announcement, index) => (
                <div key={index} className="mb-2 flex items-center justify-end">
                  {index === 0 && (
                    <span className="mr-8 hidden text-sm md:inline-block">
                      NEW
                    </span>
                  )}

                  <div
                    className={`w-full p-4 md:max-w-[60%] ${index === 0 ? "bg-[#4A4A4A]" : "bg-[#1E1E1E]"}`}
                  >
                    {announcement}
                  </div>
                </div>
              ))
            ) : (
              <p>No announcements available.</p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
