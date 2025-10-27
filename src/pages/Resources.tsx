import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { GlassCard } from "@/components/GlassCard";
import { BookOpen, Building2, Brain } from "lucide-react";
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription } from "@/components/ui/dialog";
import { motion } from "framer-motion";

interface Resource {
  icon: typeof BookOpen;
  title: string;
  description: string;
  content: string;
  delay: number;
}

const resources: Resource[] = [
  {
    icon: BookOpen,
    title: "Understanding GPU Aging",
    description: "Learn about the factors that affect GPU lifespan and performance degradation.",
    content:
      "GPU aging is influenced by multiple factors including thermal stress, power cycling, utilization patterns, and manufacturing quality. Over time, transistors can degrade, thermal paste can dry out, and capacitors can lose efficiency. Understanding these patterns helps in predicting when a GPU might fail or experience significant performance loss. Modern GPUs include sensors that track temperature, power consumption, and error rates—all crucial data points for lifecycle analysis.",
    delay: 0.1,
  },
  {
    icon: Building2,
    title: "Sustainable Data Center Planning",
    description: "Best practices for eco-friendly GPU infrastructure management.",
    content:
      "Sustainable data center planning involves balancing performance needs with environmental impact. Key strategies include: extending GPU operational life through optimal cooling and workload distribution, implementing predictive maintenance to prevent premature failures, recycling and refurbishing hardware when possible, and accurately planning replacement cycles to avoid both premature disposal and unexpected failures. ReCore's predictions enable data-driven decisions that align operational efficiency with sustainability goals.",
    delay: 0.2,
  },
  {
    icon: Brain,
    title: "How Lifecycle Prediction Works",
    description: "Technical overview of our AI-powered prediction methodology.",
    content:
      "Our lifecycle prediction system uses machine learning models trained on historical GPU operational data. The model analyzes patterns in temperature fluctuations, memory errors, clock speed variations, power draw trends, and utilization metrics. By comparing current GPU behavior against known failure patterns, the system can estimate remaining useful life with high accuracy. The model is continuously refined as more data becomes available, improving prediction reliability over time. Key inputs include thermal history, workload intensity, age, and error correction statistics.",
    delay: 0.3,
  },
];

const Resources = () => {
  const [selectedResource, setSelectedResource] = useState<Resource | null>(null);

  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-5xl mx-auto"
          >
            <div className="text-center mb-12">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Resources</h1>
              <p className="text-lg text-muted-foreground">
                Learn more about GPU lifecycle management and sustainability
              </p>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {resources.map((resource, index) => (
                <GlassCard key={index} hover delay={resource.delay}>
                  <div
                    className="p-6 space-y-4 cursor-pointer h-full flex flex-col"
                    onClick={() => setSelectedResource(resource)}
                  >
                    <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center glow-effect">
                      <resource.icon className="h-6 w-6 text-primary" />
                    </div>
                    <h3 className="text-xl font-semibold">{resource.title}</h3>
                    <p className="text-sm text-muted-foreground leading-relaxed flex-1">
                      {resource.description}
                    </p>
                    <div className="text-sm text-primary font-medium">Learn more →</div>
                  </div>
                </GlassCard>
              ))}
            </div>
          </motion.div>
        </div>
      </main>
      <Footer />

      {/* Resource Modal */}
      <Dialog open={!!selectedResource} onOpenChange={() => setSelectedResource(null)}>
        <DialogContent className="glass-card border-glass-border max-w-2xl">
          <DialogHeader>
            <DialogTitle className="text-2xl font-bold flex items-center gap-3">
              {selectedResource && (
                <>
                  <div className="w-10 h-10 rounded-lg bg-primary/10 flex items-center justify-center">
                    <selectedResource.icon className="h-5 w-5 text-primary" />
                  </div>
                  {selectedResource.title}
                </>
              )}
            </DialogTitle>
            <DialogDescription className="text-base text-muted-foreground leading-relaxed mt-4">
              {selectedResource?.content}
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  );
};

export default Resources;
