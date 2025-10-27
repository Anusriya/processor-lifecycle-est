import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { GlassCard } from "@/components/GlassCard";
import { Target, Heart, Cpu } from "lucide-react";
import { motion } from "framer-motion";

const About = () => {
  const sections = [
    {
      icon: Target,
      title: "Our Mission",
      content:
        "ReCore aims to revolutionize GPU lifecycle management by providing accurate, data-driven predictions that help organizations make sustainable decisions about their hardware infrastructure.",
      delay: 0.1,
    },
    {
      icon: Heart,
      title: "Sustainability First",
      content:
        "We believe in extending the useful life of high-performance computing hardware to reduce electronic waste and support the circular economy. Every GPU that stays operational is a step towards a greener future.",
      delay: 0.2,
    },
    {
      icon: Cpu,
      title: "Advanced Analytics",
      content:
        "Our machine learning models analyze operational patterns, thermal stress, utilization metrics, and failure indicators to predict remaining GPU lifespan with high accuracy.",
      delay: 0.3,
    },
  ];

  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-4xl mx-auto"
          >
            <div className="text-center mb-12">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">About ReCore</h1>
              <p className="text-lg text-muted-foreground">
                Building a sustainable future for high-performance computing
              </p>
            </div>

            <div className="space-y-6">
              {sections.map((section, index) => (
                <GlassCard key={index} delay={section.delay}>
                  <div className="p-8">
                    <div className="flex items-start gap-4">
                      <div className="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center flex-shrink-0 glow-effect">
                        <section.icon className="h-6 w-6 text-primary" />
                      </div>
                      <div className="flex-1">
                        <h2 className="text-2xl font-bold mb-3">{section.title}</h2>
                        <p className="text-muted-foreground leading-relaxed">
                          {section.content}
                        </p>
                      </div>
                    </div>
                  </div>
                </GlassCard>
              ))}
            </div>

            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.6, duration: 0.6 }}
              className="mt-12"
            >
              <GlassCard>
                <div className="p-8 text-center">
                  <h2 className="text-2xl font-bold mb-4">Why It Matters</h2>
                  <p className="text-muted-foreground leading-relaxed max-w-2xl mx-auto">
                    Data centers consume vast amounts of energy and resources. By accurately
                    predicting GPU lifecycles, organizations can optimize replacement cycles,
                    reduce premature disposal, and contribute to a more sustainable technology
                    ecosystem. ReCore provides the tools to make these critical decisions with
                    confidence.
                  </p>
                </div>
              </GlassCard>
            </motion.div>
          </motion.div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default About;
