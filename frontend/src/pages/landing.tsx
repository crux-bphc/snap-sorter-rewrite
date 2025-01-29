import React, { useEffect, useRef } from "react";
import "~/styles/landing.css";
import LandingPic from "~/assets/landing.webp";
import { Link } from "react-router-dom";

const Landing: React.FC = () => {
  const mainRef = useRef<HTMLDivElement>(null);
  useEffect(() => {
    const curDiv = mainRef.current;
    if (!curDiv) return;
    const handleScroll = () => {
      const scroll = window.scrollY;
      const scrollHeight =
        document.documentElement.scrollHeight -
        document.documentElement.clientHeight;
      const percent = (scroll / scrollHeight) * 100;
      curDiv.style.setProperty("--divscroll", `${percent / 2}%`);
      curDiv.style.setProperty("--mpos", `${90 - percent / 4}%`);
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, [mainRef]);

  return (
    <main
      className="container relative mx-auto flex px-4 max-lg:flex-col max-lg:items-center"
      ref={mainRef}
    >
      <div className="left-0 top-[68px] flex w-2/3 lg:sticky lg:h-[calc(100dvh-68px)]">
        <div className="image-container relative aspect-square max-h-full max-w-full select-none self-end">
          <img
            className="landing-image h-full w-full object-contain opacity-[var(--op)]"
            src={LandingPic}
          />
        </div>
      </div>

      <div className="w-full overflow-x-clip max-lg:py-4 lg:h-[200vh] lg:w-1/3">
        <div className="top-[68px] flex grid-cols-2 flex-col lg:sticky lg:grid lg:h-[calc(100dvh-68px)] lg:w-[200%] lg:translate-x-[calc(var(--divscroll)*-1)]">
          <div className="flex flex-col justify-center gap-10 max-lg:items-center max-lg:text-center">
            <div className="text-lg"> 
              Upload your photo and instantly find yourself in your batch snaps
              with SnapSorter!
            </div>
            <div className="flex gap-6">
              <Link to="/upload" className="underline underline-offset-4 hover:cursor-pointer">
                Get started
              </Link>
              <button
                className="underline underline-offset-4"
                onClick={() =>
                  window.scroll({
                    top: document.body.scrollHeight,
                    left: 0,
                    behavior: "smooth",
                  })
                }
              >
                How to use?
              </button>
            </div>
            <div className="h-12 lg:h-56" />
          </div>
          <div className="flex flex-col items-center justify-center gap-10 text-center">
            <p>
              1. Upload a high quality image of yourself{" "}
              <Link to="/upload" className="underline underline-offset-4">
                here
              </Link>
            </p>
            <p>
              2. Wait for SnapSnorter to work its magic!
            </p>
            <p>
              3. Now you don't need to ask "bhai woh pictures bhej de na"
            </p>
          </div>
        </div>
      </div>

      <div className="bottom-4 right-4 self-end max-lg:py-4 max-lg:pt-20 lg:fixed">
        brought to you by cruX
      </div>
    </main>
  );
};

export default Landing;
