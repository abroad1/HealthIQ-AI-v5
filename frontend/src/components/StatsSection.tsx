import ScrollReveal from "./ScrollReveal";
import AnimatedCounter from "./AnimatedCounter";

const StatsSection = () => {
  const stats = [
    {
      value: 100,
      suffix: "+",
      label: "Biomarkers Analyzed",
      description: "Comprehensive health assessment"
    },
    {
      value: 98.7,
      suffix: "%",
      label: "Accuracy Rate",
      description: "Medical grade precision"
    },
    {
      value: 24,
      suffix: "/7",
      label: "AI Monitoring",
      description: "Continuous health insights"
    }
  ];

  return (
    <section className="py-32 bg-muted/30">
      <div className="container mx-auto px-6">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-16">
          {stats.map((stat, index) => (
            <ScrollReveal
              key={index}
              direction="up"
              delay={index * 0.2}
              className="text-center"
            >
              <div className="text-6xl md:text-7xl font-black text-primary mb-4">
                <AnimatedCounter
                  value={stat.value}
                  suffix={stat.suffix}
                  duration={2 + index * 0.5}
                />
              </div>
              <h3 className="text-2xl font-light mb-2">{stat.label}</h3>
              <p className="text-muted-foreground">{stat.description}</p>
            </ScrollReveal>
          ))}
        </div>
      </div>
    </section>
  );
};

export default StatsSection;