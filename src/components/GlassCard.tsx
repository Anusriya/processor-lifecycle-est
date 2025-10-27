import { motion } from "framer-motion";
import { ReactNode } from "react";

interface GlassCardProps {
  children: ReactNode;
  className?: string;
  hover?: boolean;
  delay?: number;
}

export const GlassCard = ({ children, className = "", hover = false, delay = 0 }: GlassCardProps) => {
  const baseClass = hover ? "glass-card-hover" : "glass-card";
  
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay }}
      className={`${baseClass} ${className}`}
    >
      {children}
    </motion.div>
  );
};
