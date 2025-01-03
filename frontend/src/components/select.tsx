import React, { useEffect, useState } from "react";
import Masonry from "react-responsive-masonry";
import "~/styles/gallery.css";

function getWindowDimensions() {
  const { innerWidth: width, innerHeight: height } = window;
  return {
    width,
    height,
  };
}

function useWindowDimensions() {
  const [windowDimensions, setWindowDimensions] = useState(
    getWindowDimensions(),
  );

  useEffect(() => {
    function handleResize() {
      setWindowDimensions(getWindowDimensions());
    }

    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return windowDimensions;
}

const Select: React.FC<{
  images: Record<
    string,
    {
      sample_url: string;
    }
  >;
}> = ({ images }) => {
  const { width } = useWindowDimensions();
  const [selected, setSelected] = useState<Record<string, boolean>>({});

  const columns = width < 768 ? 1 : width < 1024 ? 2 : 3;
  return (
    <div className="w-full">
      <Masonry columnsCount={columns} gutter="1.5rem">
        {Object.entries(images).map(([i, { sample_url }]) => (
          <div
            key={i}
            onClick={() => {
              setSelected((prev) =>
                Object.fromEntries([...Object.entries(prev), [i, !prev[i]]]),
              );
              setTimeout(() => console.log(selected), 100);
            }}
          >
            <div className="group relative">
              <img
                src={sample_url}
                className={
                  "h-auto w-full transition-opacity duration-300 group-hover:opacity-40 " +
                  (selected[i] ? "opacity-40" : "")
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
          </div>
        ))}
      </Masonry>
    </div>
  );
};

export default Select;
