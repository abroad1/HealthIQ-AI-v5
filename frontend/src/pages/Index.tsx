import HeroSection from "@/components/HeroSection";
import ImageCarousel from "@/components/ImageCarousel";
import StatsSection from "@/components/StatsSection";
import BiomarkerAnimation from "@/components/BiomarkerAnimation";
import HowItWorksSection from "@/components/HowItWorksSection";
import TechnologySection from "@/components/TechnologySection";
import FinalCTASection from "@/components/FinalCTASection";

const Index = () => {
  return (
    <div className="min-h-screen">
      <HeroSection />
      <ImageCarousel />
      <StatsSection />
      <BiomarkerAnimation />
      <HowItWorksSection />
      <TechnologySection />
      <FinalCTASection />
    </div>
  );
};

export default Index;
