import React from "react";

import Gallery from "../components/gallery";
const images = {
  image1: {
    image_url: "https://picsum.photos/200/300?image=1050",
    image_drive_id: "z6b8l72fm3r1",
  },
  image2: {
    image_url: "https://picsum.photos/300/300?image=1060",
    image_drive_id: "g5u9b4n6d1h3",
  },
  image3: {
    image_url: "https://picsum.photos/300/300?image=1061",
    image_drive_id: "j3k2t9l1q5z8",
  },
  image4: {
    image_url: "https://picsum.photos/300/300?image=1062",
    image_drive_id: "w8c1p3d4j9u2",
  },
  image5: {
    image_url: "https://picsum.photos/300/300?image=1063",
    image_drive_id: "m4h5r7d3l8o2",
  },
  image6: {
    image_url: "https://picsum.photos/300/300?image=1064",
    image_drive_id: "t2x9s5f7v3k1",
  },
  image7: {
    image_url: "https://picsum.photos/300/300?image=1065",
    image_drive_id: "p5a4l2o3e8r6",
  },
  image8: {
    image_url: "https://picsum.photos/300/300?image=1066",
    image_drive_id: "i1y6n4d9q2m5",
  },
  image9: {
    image_url: "https://picsum.photos/300/300?image=1067",
    image_drive_id: "k8u7p2j3z1t0",
  },
  image10: {
    image_url: "https://picsum.photos/300/300?image=206",
    image_drive_id: "b5v2h9g6s7o1",
  },
};

const Test: React.FC = () => {
  return (
    <div className="flex w-full items-center justify-center">
      <div className="w-[70vw]">
        <Gallery images={images} />
      </div>
    </div>
  );
};

export default Test;
