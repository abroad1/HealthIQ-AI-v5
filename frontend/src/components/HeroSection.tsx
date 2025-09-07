import { motion } from "framer-motion";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Activity, Check, ChevronRight } from "lucide-react";
import ScrollReveal from "./ScrollReveal";
import AnimatedCounter from "./AnimatedCounter";

const HeroSection = () => {
  return (
    <section className="relative min-h-screen flex items-center justify-center overflow-hidden">
      {/* Floating counter */}
      <motion.div
        className="absolute right-8 top-1/2 transform -translate-y-1/2 text-9xl font-black opacity-5 select-none"
        animate={{
          y: [0, -20, 0],
        }}
        transition={{
          duration: 4,
          ease: "easeInOut",
          repeat: Infinity,
        }}
      >
        <AnimatedCounter value={100} suffix="+" className="text-primary" />
      </motion.div>

      <div className="container mx-auto px-6 text-center z-10">
        <ScrollReveal direction="down" delay={0.2}>
          <Badge variant="secondary" className="mb-8 px-6 py-2 text-sm animate-float">
            <Activity className="w-4 h-4 mr-2" />
            Medical Grade Analytics
          </Badge>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.4}>
          <h1 className="text-6xl md:text-8xl font-light mb-8 leading-tight">
            Decode Your
            <br />
            <span className="text-gradient font-extralight">Health Story</span>
          </h1>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.6}>
          <p className="text-xl md:text-2xl text-muted-foreground mb-12 max-w-3xl mx-auto font-light">
            Advanced AI analyzes your biomarkers to predict health risks and optimize your wellness journey with unprecedented precision.
          </p>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={0.8}>
          <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
            <Button size="lg" className="rounded-full px-8 py-6 text-lg shadow-medical">
              Start Your Analysis
              <ChevronRight className="w-5 h-5 ml-2" />
            </Button>
            <Button variant="outline" size="lg" className="rounded-full px-8 py-6 text-lg">
              View Sample Report
            </Button>
          </div>
        </ScrollReveal>

        <ScrollReveal direction="up" delay={1}>
          <div className="flex flex-col sm:flex-row items-center justify-center gap-8 text-muted-foreground">
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-medical-success" />
              <span>10,000+ analyses completed</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-medical-success" />
              <span>Results in 24 hours</span>
            </div>
            <div className="flex items-center gap-2">
              <Check className="w-5 h-5 text-medical-success" />
              <span>Medical grade accuracy</span>
            </div>
          </div>
        </ScrollReveal>
      </div>

      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-br from-primary/5 via-transparent to-accent/5 -z-10" />
    </section>
  );
};

export default HeroSection;