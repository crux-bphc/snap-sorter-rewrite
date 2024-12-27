import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <p className="text-3xl">SNAP SORTER</p>
    </QueryClientProvider>
  );
}

export default App;
