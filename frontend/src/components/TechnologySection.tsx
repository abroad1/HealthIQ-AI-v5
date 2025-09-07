import { CheckCircle } from "lucide-react";
import ScrollReveal from "./ScrollReveal";
import aiMedical from "@/assets/ai-medical.jpg";

const TechnologySection = () => {
  const features = [
    "Advanced Pattern Recognition",
    "Predictive Health Modeling",
    "Personalized Risk Assessment",
    "Real-time Biomarker Tracking",
    "Clinical Decision Support",
    "Longitudinal Health Analysis"
  ];

  return (
    <section className="py-32 bg-muted/20">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          <ScrollReveal direction="left">
            <div>
              <h2 className="text-5xl md:text-6xl font-light mb-8">
                Powered by
                <br />
                <span className="text-gradient">Advanced AI</span>
              </h2>
              
              <p className="text-xl text-muted-foreground mb-12 leading-relaxed">
                Our proprietary artificial intelligence engine processes millions of health data points 
                to deliver insights previously only available to top medical institutions.
              </p>

              <div className="space-y-6">
                {features.map((feature, index) => (
                  <ScrollReveal
                    key={index}
                    direction="left"
                    delay={index * 0.1}
                  >
                    <div className="flex items-center gap-4">
                      <div className="w-2 h-2 rounded-full bg-primary flex-shrink-0" />
                      <span className="text-lg">{feature}</span>
                    </div>
                  </ScrollReveal>
                ))}
              </div>
            </div>
          </ScrollReveal>

          <ScrollReveal direction="right">
            <div className="relative">
              <img
                src={aiMedical}
                alt="AI-powered medical technology"
                className="w-full rounded-2xl shadow-2xl"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-primary/20 via-transparent to-transparent rounded-2xl" />
            </div>
          </ScrollReveal>
        </div>
      </div>
    </section>
  );
};

export default TechnologySection;