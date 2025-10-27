import { Github } from "lucide-react";
import { motion } from "framer-motion";

export const Footer = () => {
  return (
    <footer className="border-t glass-card mt-20">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="flex flex-col md:flex-row justify-between items-center gap-4">
          <div className="text-sm text-muted-foreground">
            © 2025 ReCore. Built for sustainable GPU lifecycle management.
          </div>
          
          <div className="flex items-center gap-4">
            <motion.a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-foreground transition-colors flex items-center gap-2"
              whileHover={{ scale: 1.05 }}
            >
              <Github className="h-5 w-5" />
              <span className="text-sm">GitHub</span>
            </motion.a>
          </div>
        </div>
      </div>
    </footer>
  );
};
