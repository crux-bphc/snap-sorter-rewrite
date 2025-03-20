import React from "react";
import { useQuery } from "@tanstack/react-query";
import api from "../utils/api";
import { deleteCookie } from "../utils/cookieUtils";

const fetchProfile = async () => {
  const res = await api.get("/profile");
  return res.data;
};

const Profile: React.FC = () => {
  const { data, isLoading, error } = useQuery({
    queryKey: ["profile"],
    queryFn: fetchProfile,
  });

  const handleLogout = () => {
    deleteCookie("token");
    window.location.href = "/";
  };

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
        <div className="text-lg">Email: {data.email}</div>
        <div className="text-lg">First Name: {data.first_name}</div>
        <div className="text-lg">Last Name: {data.last_name}</div>
        <div className="text-lg">
          Download Available: {data.download_available ? "Yes" : "No"}
        </div>
        <button
          onClick={handleLogout}
          className="border border-white p-4 text-xl uppercase hover:bg-[#1E1E1E]"
        >
          Logout
        </button>
      </fieldset>
    </div>
  );
};

export default Profile;
