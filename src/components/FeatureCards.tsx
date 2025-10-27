import { Recycle, TrendingUp, DollarSign, Globe } from "lucide-react";
import { GlassCard } from "./GlassCard";

const features = [
  {
    icon: Recycle,
    title: "Reduce E-Waste",
    description: "Make informed decisions on GPU reuse to minimize electronic waste and support circular economy principles.",
    delay: 0.1,
  },
  {
    icon: TrendingUp,
    title: "Predict Lifecycle",
    description: "Leverage AI-powered predictions to accurately forecast GPU remaining useful life and plan maintenance cycles.",
    delay: 0.2,
  },
  {
    icon: DollarSign,
    title: "Optimize Data Center Cost",
    description: "Maximize ROI by identifying optimal replacement timing and extending GPU operational lifespan where viable.",
    delay: 0.3,
  },
  {
    icon: Globe,
    title: "Support Circular Tech Economy",
    description: "Contribute to sustainable technology practices by enabling responsible GPU lifecycle management at scale.",
    delay: 0.4,
  },
];

export const FeatureCards = () => {
  return (
    <section className="py-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <GlassCard key={index} hover delay={feature.delay}>
              <div className="p-6 space-y-4">
                <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center glow-effect">
                  <feature.icon className="h-6 w-6 text-primary" />
                </div>
                <h3 className="text-xl font-semibold">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">
                  {feature.description}
                </p>
              </div>
            </GlassCard>
          ))}
        </div>
      </div>
    </section>
  );
};
