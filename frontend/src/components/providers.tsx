"use client";

import { ReactNode } from "react";
import { WebSocketProvider } from "@/contexts/websocket-context";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

export function Providers({ children }: { children: ReactNode }) {
  return (
    <QueryClientProvider client={queryClient}>
      <WebSocketProvider>
        {children}
      </WebSocketProvider>
    </QueryClientProvider>
  );
}
