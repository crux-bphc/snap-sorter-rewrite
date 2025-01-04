import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/navbar";
import { AuthProvider } from "./components/auth-context";
import LoginPage from "./pages/login";
import RedirectHandler from "./components/redirect-handler";
import Landing from "./pages/landing";
import Test from "./pages/test";
import Upload from "./pages/upload";
import Results from "./pages/results";
import Protected from "./components/protected";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Router>
          <Navbar />
          <Routes>
            <Route path="/" element={<Landing />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/test" element={<Test />} />
            <Route path="/redirect" element={<RedirectHandler />} />
            <Route path="/" element={<Protected />}>
              <Route path="/upload" element={<Upload />} />
              <Route path="/results" element={<Results />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App;
