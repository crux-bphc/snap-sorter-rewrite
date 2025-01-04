import { useMutation } from "@tanstack/react-query";
import React, { useState } from "react";
import { submitSamplesEndpoint } from "../utils/constants";
import api from "../utils/api";
import { useNavigate } from "react-router-dom";

const Select: React.FC<{
  samples: Record<
    string,
    {
      cluster: number;
      sample_url: string;
      images: string[];
    }
  >;
}> = ({ samples }) => {
  const [selected, setSelected] = useState<Record<string, boolean>>({});
  const navigate = useNavigate();

  const submitMutation = useMutation({
    mutationFn: async (body: string[]) => {
      return await api.post<string>(submitSamplesEndpoint, body);
    },
    onSuccess: () => navigate("/results"),
    onError: () => {
      alert("Submission failed");
    },
  });

  return (
    <div className="flex w-full flex-col gap-8">
      <p className="text-center text-xl">Select all images with your face</p>
      <div className="row-auto grid grid-flow-row grid-cols-2 justify-center gap-4 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        {Object.entries(samples).map(([i, { sample_url }]) => (
          <div
            className="group relative max-h-80 cursor-pointer"
            key={i}
            onClick={() =>
              setSelected((prev) =>
                Object.fromEntries([...Object.entries(prev), [i, !prev[i]]]),
              )
            }
          >
            <img
              src={sample_url}
              className={
                "h-full w-full object-contain transition-opacity duration-300 group-hover:opacity-40 " +
                (selected[i] ? "opacity-40 contrast-75" : "")
              }
              alt=""
            />
            <div className="absolute inset-0 flex flex-col justify-center text-center">
              {selected[i] ? (
                <div>Selected</div>
              ) : (
                <div className="flex flex-1 items-center justify-center opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                  Click to select
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <button
        onClick={() =>
          submitMutation.mutate(
            Object.entries(samples)
              .filter(([i]) => selected[i])
              .flatMap((v) => v[1].images),
          )
        }
        className="self-center bg-foreground px-8 py-2 text-lg font-semibold text-background shadow transition-colors hover:bg-gray-400 disabled:bg-red-400"
        disabled={submitMutation.isPending}
      >
        Submit
      </button>
    </div>
  );
};

export default Select;
