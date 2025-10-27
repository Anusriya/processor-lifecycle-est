import { Navbar } from "@/components/Navbar";
import { Hero } from "@/components/Hero";
import { FeatureCards } from "@/components/FeatureCards";
import { Footer } from "@/components/Footer";

const Landing = () => {
  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-16">
        <Hero />
        <FeatureCards />
      </main>
      <Footer />
    </div>
  );
};

export default Landing;
