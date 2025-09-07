import { Upload, Brain, TrendingUp } from "lucide-react";
import ScrollReveal from "./ScrollReveal";
import { Card } from "@/components/ui/card";

const HowItWorksSection = () => {
  const steps = [
    {
      icon: Upload,
      title: "Upload Results",
      description: "Securely upload your lab results or connect directly with your healthcare provider for instant access."
    },
    {
      icon: Brain,
      title: "AI Analysis",
      description: "Our advanced AI analyzes 100+ biomarkers using machine learning models trained on millions of data points."
    },
    {
      icon: TrendingUp,
      title: "Get Insights",
      description: "Receive personalized health insights, risk predictions, and actionable recommendations for optimal wellness."
    }
  ];

  return (
    <section className="py-32">
      <div className="container mx-auto px-6">
        <ScrollReveal direction="up" className="text-center mb-16">
          <h2 className="text-5xl md:text-6xl font-light mb-6">
            How It <span className="text-gradient">Works</span>
          </h2>
          <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
            Transform your health data into actionable insights in three simple steps
          </p>
        </ScrollReveal>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => (
            <ScrollReveal
              key={index}
              direction="up"
              delay={index * 0.2}
            >
              <Card className="p-8 text-center h-full border-none bg-transparent hover:bg-card/50 transition-all duration-300">
                <div className="w-20 h-20 rounded-full bg-primary/10 flex items-center justify-center mx-auto mb-6">
                  <step.icon className="w-10 h-10 text-primary" />
                </div>
                <div className="w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center mx-auto mb-6 text-sm font-bold">
                  {index + 1}
                </div>
                <h3 className="text-2xl font-light mb-4">{step.title}</h3>
                <p className="text-muted-foreground leading-relaxed">
                  {step.description}
                </p>
              </Card>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
};

export default HowItWorksSection;