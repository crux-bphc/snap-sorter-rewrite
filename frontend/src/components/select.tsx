import { useMutation } from "@tanstack/react-query";
import React, { useState } from "react";
import { submitSamplesEndpoint } from "../utils/constants";
import api from "../utils/api";
import { useNavigate } from "react-router-dom";
import { Check } from "lucide-react";

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
    <div className="flex w-[80vw] w-full flex-col gap-8">
      <div className="flex w-full flex-row">
        <p className="flex h-full flex-col items-baseline gap-2 text-xl md:flex-row">
          <h1 className="h-full text-4xl">SELECT</h1>
          <div className="">all images with your face</div>
        </p>
        <button
          onClick={() =>
            submitMutation.mutate(
              Object.entries(samples)
                .filter(([i]) => selected[i])
                .flatMap((v) => v[1].images),
            )
          }
          className="mb-auto ml-auto mt-auto h-1/2 border border-foreground px-8 py-2 text-lg font-semibold text-background text-white shadow transition-colors hover:bg-gray-400 disabled:bg-red-400"
          disabled={submitMutation.isPending}
        >
          Submit
        </button>
      </div>
      <div className="row-auto grid grid-flow-row grid-cols-2 justify-center gap-4 border border-foreground p-8 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5">
        {Object.entries(samples).map(([i, { sample_url }]) => (
          <div
            className="group relative z-0 max-h-80 cursor-pointer"
            key={i}
            onClick={() =>
              setSelected((prev) =>
                Object.fromEntries([...Object.entries(prev), [i, !prev[i]]]),
              )
            }
          >
            <div
              className={
                "absolute z-10 -left-[5px] -top-[5px] bg-black flex h-5 w-5 items-center justify-center rounded-full border border-foreground " +
                (selected[i] ? "" : "hidden border-none")
              }
            >
              <Check
                size={20}
                className={
                  "h-4 w-4 text-foreground " +
                  (selected[i] ? "" : "hidden border-none")
                }
              />
            </div>
            <img
              src={sample_url}
              className={
                "h-full w-full object-contain duration-300 group-hover:opacity-40 " +
                (selected[i] ? "border border-foreground" : "")
              }
              alt=""
            />

            <div className="absolute inset-0 flex flex-col justify-center text-center">
              {selected[i] ? (
                <div></div>
              ) : (
                <div className="flex flex-1 items-center justify-center opacity-0 transition-opacity duration-300 group-hover:opacity-100">
                  Click to select
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
      <div>Submit without selecting any if there are no matches.</div>
    </div>
  );
};

export default Select;
