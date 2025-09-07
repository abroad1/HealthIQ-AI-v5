import { Button } from "@/components/ui/button";
import { ChevronRight, Shield, Clock, Award } from "lucide-react";
import ScrollReveal from "./ScrollReveal";

const FinalCTASection = () => {
  return (
    <section className="py-32 bg-gradient-to-br from-primary/10 via-background to-accent/10">
      <div className="container mx-auto px-6 text-center">
        <ScrollReveal direction="up">
          <h2 className="text-5xl md:text-6xl font-light mb-8">
            Ready to Unlock Your
            <br />
            <span className="text-gradient">Health Potential?</span>
          </h2>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.2}>
          <p className="text-xl text-muted-foreground mb-12 max-w-3xl mx-auto">
            Join thousands who have transformed their health journey with AI-powered insights. 
            Start your comprehensive health analysis today.
          </p>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.4}>
          <div className="flex flex-col sm:flex-row gap-6 justify-center mb-16">
            <Button size="lg" className="rounded-full px-12 py-6 text-lg shadow-float">
              Begin Your Analysis
              <ChevronRight className="w-5 h-5 ml-2" />
            </Button>
            <Button variant="outline" size="lg" className="rounded-full px-12 py-6 text-lg">
              Schedule Consultation
            </Button>
          </div>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.6}>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="flex flex-col items-center text-center">
              <Shield className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-lg font-semibold mb-2">HIPAA Compliant</h3>
              <p className="text-muted-foreground">Your health data is always secure and private</p>
            </div>
            <div className="flex flex-col items-center text-center">
              <Clock className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-lg font-semibold mb-2">24-Hour Results</h3>
              <p className="text-muted-foreground">Get your comprehensive health report fast</p>
            </div>
            <div className="flex flex-col items-center text-center">
              <Award className="w-12 h-12 text-primary mb-4" />
              <h3 className="text-lg font-semibold mb-2">Medical Grade</h3>
              <p className="text-muted-foreground">Clinically validated analysis and insights</p>
            </div>
          </div>
        </ScrollReveal>
      </div>
    </section>
  );
};

export default FinalCTASection;