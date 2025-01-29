import type React from "react";
import { deleteCookie } from "../utils/cookieUtils";
const Profile: React.FC = () => {

  const handleLogout = () => {
    deleteCookie("token");
    window.location.href = "/";
  };

  return (
    <div className="flex min-h-screen justify-center py-4 px-20">
      <fieldset className="flex w-full p-4 border border-white h-fit">
        <legend className="text-2xl uppercase">Profile</legend>
        <button onClick={handleLogout} className="text-xl uppercase border border-white p-4 hover:bg-gray-600">
          Logout
        </button>
      </fieldset>
    </div>
  );
};

export default Profile;
