import {
  QueryClient,
  QueryClientProvider,
} from '@tanstack/react-query'

function App() {
  const queryClient = new QueryClient();

  return (
    <>
      <QueryClientProvider client={queryClient}>
        <p className="bg-black texSSt-3xl font-gfs text-foreground">
          SNAP SORTER
        </p>
      </QueryClientProvider>
    </>
  );
}

export default App;
