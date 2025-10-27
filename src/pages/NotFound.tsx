import { useLocation, Link } from "react-router-dom";
import { useEffect } from "react";
import { motion } from "framer-motion";
import { Home } from "lucide-react";
import { Button } from "@/components/ui/button";
import { GlassCard } from "@/components/GlassCard";

const NotFound = () => {
  const location = useLocation();

  useEffect(() => {
    console.error("404 Error: User attempted to access non-existent route:", location.pathname);
  }, [location.pathname]);

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ duration: 0.5 }}
      >
        <GlassCard className="max-w-md">
          <div className="p-8 text-center space-y-6">
            <motion.div
              initial={{ y: -20 }}
              animate={{ y: 0 }}
              transition={{ delay: 0.2, type: "spring" }}
              className="text-8xl font-bold bg-gradient-to-r from-primary to-accent bg-clip-text text-transparent"
            >
              404
            </motion.div>
            
            <div className="space-y-2">
              <h1 className="text-2xl font-bold">Page Not Found</h1>
              <p className="text-muted-foreground">
                The page you're looking for doesn't exist or has been moved.
              </p>
            </div>

            <Link to="/">
              <Button size="lg" className="glow-effect">
                <Home className="mr-2 h-5 w-5" />
                Return to Home
              </Button>
            </Link>
          </div>
        </GlassCard>
      </motion.div>
    </div>
  );
};

export default NotFound;
