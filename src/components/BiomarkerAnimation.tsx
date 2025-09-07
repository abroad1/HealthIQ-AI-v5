import { motion, useScroll, useTransform } from "framer-motion";
import { useRef } from "react";

const biomarkers = [
  // Heart & Cardiovascular
  "HEART", "Apolipoprotein B", "HDL Cholesterol", "LDL Cholesterol", "Total Cholesterol", 
  "Triglycerides", "Lipoprotein(a)", "hsCRP", "Homocysteine", "TMAO",
  
  // Thyroid
  "THYROID", "TSH", "Free T4", "Free T3", "Reverse T3", "TPO Antibodies", 
  "Thyroglobulin Antibodies",
  
  // Metabolic
  "METABOLIC", "Glucose", "HbA1c", "Insulin", "HOMA-IR", "Fructosamine", 
  "Advanced Glycation End Products",
  
  // Inflammation
  "INFLAMMATION", "ESR", "Fibrinogen", "Ferritin", "IL-6", "TNF-alpha", 
  "Complement C3", "Complement C4",
  
  // Liver
  "LIVER", "ALT", "AST", "GGT", "Alkaline Phosphatase", "Total Bilirubin", 
  "Direct Bilirubin", "Albumin",
  
  // Kidney
  "KIDNEY", "Creatinine", "BUN", "eGFR", "Cystatin C", "Microalbumin", 
  "Uric Acid",
  
  // Vitamins
  "VITAMINS", "Vitamin D", "Vitamin B12", "Folate", "Vitamin B6", 
  "Magnesium", "Zinc", "Selenium",
  
  // Hormones
  "HORMONES", "Cortisol", "DHEA-S", "Testosterone", "Estradiol", 
  "Progesterone", "IGF-1", "Growth Hormone",
  
  // Blood
  "BLOOD", "Complete Blood Count", "Hemoglobin", "Hematocrit", "RBC", 
  "WBC", "Platelets", "Iron", "TIBC",
  
  // Cancer Markers
  "CANCER", "PSA", "CEA", "CA 19-9", "CA 125", "AFP", "Beta-hCG",
  
  // Advanced
  "ADVANCED", "Omega-3 Index", "CoQ10", "Glutathione", "8-OHdG", 
  "Telomere Length", "Methylation Status"
];

const BiomarkerAnimation = () => {
  const containerRef = useRef(null);
  const { scrollYProgress } = useScroll({
    target: containerRef,
    offset: ["start end", "end start"]
  });

  return (
    <section ref={containerRef} className="relative min-h-[150vh] py-32 bg-muted/20">
      <div className="container mx-auto px-6">
        <div className="text-center mb-16">
          <h2 className="text-5xl font-light mb-6 text-gradient">
            Comprehensive Biomarker Analysis
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Our AI analyzes 100+ biomarkers to provide unprecedented insights into your health
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 max-w-6xl mx-auto">
          {biomarkers.map((marker, index) => {
            const isCategory = marker === marker.toUpperCase() && !marker.includes(" ");
            const delay = index * 0.05;
            
            const opacity = useTransform(
              scrollYProgress,
              [delay / biomarkers.length, (delay + 0.2) / biomarkers.length],
              [0, 1]
            );
            
            const filter = useTransform(
              scrollYProgress,
              [delay / biomarkers.length, (delay + 0.2) / biomarkers.length],
              ["blur(4px)", "blur(0px)"]
            );

            return (
              <motion.div
                key={index}
                style={{ opacity, filter }}
                className={`p-4 rounded-lg transition-all duration-300 ${
                  isCategory 
                    ? "text-primary font-bold text-lg bg-primary/10" 
                    : "text-muted-foreground font-light bg-card/50"
                }`}
              >
                {marker}
              </motion.div>
            );
          })}
        </div>
      </div>
    </section>
  );
};

export default BiomarkerAnimation;