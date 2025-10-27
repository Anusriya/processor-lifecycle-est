import { useState } from "react";
import { Navbar } from "@/components/Navbar";
import { Footer } from "@/components/Footer";
import { GlassCard } from "@/components/GlassCard";
import { Button } from "@/components/ui/button";
import { Upload as UploadIcon, FileCheck, ExternalLink } from "lucide-react";
import { motion } from "framer-motion";
import { useToast } from "@/hooks/use-toast";

const Upload = () => {
  const [file, setFile] = useState<File | null>(null);
  const [uploading, setUploading] = useState(false);
  const [uploadComplete, setUploadComplete] = useState(false);
  const { toast } = useToast();

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile && droppedFile.name.endsWith(".csv")) {
      setFile(droppedFile);
    } else {
      toast({
        title: "Invalid file type",
        description: "Please upload a CSV file.",
        variant: "destructive",
      });
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
    }
  };

  const handleAnalyze = () => {
    if (!file) {
      toast({
        title: "No file selected",
        description: "Please upload a CSV file first.",
        variant: "destructive",
      });
      return;
    }

    setUploading(true);
    // Simulate upload process
    setTimeout(() => {
      setUploading(false);
      setUploadComplete(true);
      toast({
        title: "Success!",
        description: "Data successfully processed.",
      });
    }, 2000);
  };

  return (
    <div className="min-h-screen">
      <Navbar />
      <main className="pt-24 pb-16">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6 }}
            className="max-w-3xl mx-auto"
          >
            <div className="text-center mb-8">
              <h1 className="text-4xl md:text-5xl font-bold mb-4">Upload GPU Data</h1>
              <p className="text-lg text-muted-foreground">
                Upload your GPU operational CSV file to begin lifecycle analysis
              </p>
            </div>

            {!uploadComplete ? (
              <GlassCard>
                <div className="p-8">
                  {/* Drag & Drop Area */}
                  <div
                    onDragOver={handleDragOver}
                    onDrop={handleDrop}
                    className="border-2 border-dashed border-primary/30 rounded-xl p-12 text-center hover:border-primary/60 transition-colors cursor-pointer"
                  >
                    <input
                      type="file"
                      accept=".csv"
                      onChange={handleFileChange}
                      className="hidden"
                      id="file-upload"
                    />
                    <label htmlFor="file-upload" className="cursor-pointer">
                      <UploadIcon className="h-16 w-16 mx-auto mb-4 text-primary animate-float" />
                      <h3 className="text-xl font-semibold mb-2">
                        {file ? file.name : "Drop your CSV file here"}
                      </h3>
                      <p className="text-muted-foreground">
                        or click to browse your files
                      </p>
                    </label>
                  </div>

                  {/* Analyze Button */}
                  <Button
                    size="lg"
                    onClick={handleAnalyze}
                    disabled={!file || uploading}
                    className="w-full mt-6 glow-effect"
                  >
                    {uploading ? "Processing..." : "Analyze and Classify"}
                  </Button>
                </div>
              </GlassCard>
            ) : (
              <GlassCard>
                <div className="p-8 text-center space-y-6">
                  <motion.div
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ type: "spring", duration: 0.6 }}
                  >
                    <FileCheck className="h-20 w-20 mx-auto text-primary glow-effect-strong" />
                  </motion.div>
                  
                  <div>
                    <h2 className="text-3xl font-bold mb-2">✅ Data Successfully Processed</h2>
                    <p className="text-muted-foreground">
                      Your GPU data has been analyzed and classified.
                    </p>
                  </div>

                  <Button
                    size="lg"
                    onClick={() => window.open("http://localhost:8501", "_blank")}
                    className="glow-effect-strong"
                  >
                    <ExternalLink className="mr-2 h-5 w-5" />
                    Open Dashboard
                  </Button>

                  <Button
                    variant="outline"
                    onClick={() => {
                      setFile(null);
                      setUploadComplete(false);
                    }}
                    className="ml-4"
                  >
                    Upload Another File
                  </Button>
                </div>
              </GlassCard>
            )}
          </motion.div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default Upload;
