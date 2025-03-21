import React from "react";
import { useMutation, useQuery } from "@tanstack/react-query";
import api from "../utils/api";
import { deleteCookie } from "../utils/cookieUtils";
import { HelpCircle } from "lucide-react";
import { downloadEndpoint } from "../utils/constants";
import { isAxiosError } from "axios";

const fetchProfile = async () => {
  const res = await api.get("/profile");
  return res.data;
};

const Profile: React.FC = () => {
  const { data, isLoading, error } = useQuery<{
    email: string;
    name: string;
    download_available: boolean;
  }>({
    queryKey: ["profile"],
    queryFn: fetchProfile,
  });

  const handleLogout = () => {
    deleteCookie("token");
    window.location.href = "/";
  };

  const downloadZipMutation = useMutation({
    mutationFn: async () => {
      return (
        await api.get<Blob>(downloadEndpoint, {
          responseType: "blob",
        })
      ).data;
    },
    onError: (err) => {
      if (isAxiosError(err) && err.response?.status === 404) {
        alert("No download request found");
      } else console.error(err);
    },
    onSuccess: (data) => {
      const url = window.URL.createObjectURL(data);
      const a = document.createElement("a");
      a.href = url;
      a.download = "snap_snorter_images.zip";
      a.click();
      window.URL.revokeObjectURL(url);
      a.remove();
    },
  });

  if (isLoading) return <div className="text-center text-xl">Loading...</div>;
  if (error)
    return (
      <div className="text-center text-xl text-red-500">
        Error loading profile.
      </div>
    );

  return (
    <div className="flex min-h-screen justify-center px-20 py-4">
      <fieldset className="flex h-fit w-full flex-col gap-4 border border-white p-4">
        <legend className="text-2xl uppercase">Profile</legend>
        {isLoading && <div>Loading...</div>}
        {error && <div>Error loading profile</div>}
        {data && (
          <>
            <div className="text-lg">Email: {data.email}</div>
            <div className="text-lg">Name: {data.name}</div>
            <div className="text-lg">
              {data.download_available ? (
                <button
                  className="border-2 p-2 disabled:opacity-50"
                  onClick={() => downloadZipMutation.mutate()}
                  disabled={downloadZipMutation.isPending}
                >
                  Download images
                </button>
              ) : (
                <div className="flex gap-2">
                  No Download Available
                  <HelpCircle
                    className="cursor-pointer text-gray-400"
                    onClick={() =>
                      alert("You can request a download from the results page")
                    }
                  />
                </div>
              )}
            </div>
            <button
              onClick={handleLogout}
              className="border border-white p-4 text-xl uppercase hover:bg-[#1E1E1E]"
            >
              Logout
            </button>
          </>
        )}
      </fieldset>
    </div>
  );
};

export default Profile;
