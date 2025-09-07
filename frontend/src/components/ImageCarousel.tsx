import { motion } from "framer-motion";
import medicalLab from "@/assets/medical-lab.jpg";
import healthAnalytics from "@/assets/health-analytics.jpg";
import aiMedical from "@/assets/ai-medical.jpg";
import bloodResearch from "@/assets/blood-research.jpg";
import heartTech from "@/assets/heart-tech.jpg";
import consultation from "@/assets/consultation.jpg";

const images = [
  { src: medicalLab, caption: "Advanced Medical Technology" },
  { src: healthAnalytics, caption: "Precision Health Analytics" },
  { src: aiMedical, caption: "AI-Powered Diagnostics" },
  { src: bloodResearch, caption: "Biomarker Research" },
  { src: heartTech, caption: "Cardiovascular Monitoring" },
  { src: consultation, caption: "Personalized Healthcare" },
];

const ImageCarousel = () => {
  // Duplicate images for seamless loop
  const duplicatedImages = [...images, ...images];

  return (
    <section className="relative h-[60vh] overflow-hidden bg-muted/30">
      <div className="absolute inset-0 bg-gradient-to-r from-background via-transparent to-background z-10" />
      
      <motion.div
        className="flex h-full"
        animate={{
          x: [0, -50 * duplicatedImages.length + "%"],
        }}
        transition={{
          duration: 80,
          ease: "linear",
          repeat: Infinity,
        }}
      >
        {duplicatedImages.map((image, index) => (
          <div
            key={index}
            className="relative min-w-[400px] h-full"
          >
            <img
              src={image.src}
              alt={image.caption}
              className="w-full h-full object-cover"
            />
            <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent" />
            <div className="absolute bottom-8 left-8 text-white">
              <h3 className="text-xl font-light">{image.caption}</h3>
            </div>
          </div>
        ))}
      </motion.div>
    </section>
  );
};

export default ImageCarousel;