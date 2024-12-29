import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Navbar from "./components/navbar";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <Navbar />
    </QueryClientProvider>
  );
}

export default App;
