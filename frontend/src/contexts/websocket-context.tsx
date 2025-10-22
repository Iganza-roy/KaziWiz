"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { io, Socket } from "socket.io-client";

type WebSocketContextType = {
  socket: Socket | null;
  isConnected: boolean;
  connectionStatus: string;
  subscribeToSession: (sessionId: string) => void;
};

const WebSocketContext = createContext<WebSocketContextType | undefined>(undefined);

export function WebSocketProvider({ children }: { children: ReactNode }) {
  const [socket, setSocket] = useState<Socket | null>(null);
  const [isConnected, setIsConnected] = useState(false);
  const [connectionStatus, setConnectionStatus] = useState("Disconnected");

  useEffect(() => {
    // Connect to WebSocket server
    const socketInstance = io("http://localhost:8000", {
      transports: ["websocket"],
      reconnection: true,
      reconnectionDelay: 1000,
      reconnectionAttempts: 5,
    });

    socketInstance.on("connect", () => {
      console.log("✅ WebSocket connected");
      setIsConnected(true);
      setConnectionStatus("Connected");
    });

    socketInstance.on("disconnect", () => {
      console.log("❌ WebSocket disconnected");
      setIsConnected(false);
      setConnectionStatus("Disconnected");
    });

    // Log ALL incoming events for debugging
    socketInstance.onAny((eventName, ...args) => {
      console.log(`🔔 Socket event received: ${eventName}`, args);
    });

    socketInstance.on("connect_error", (error) => {
      console.error("WebSocket connection error:", error);
      setConnectionStatus("Connection Error");
    });

    socketInstance.on("reconnecting", (attemptNumber) => {
      console.log(`🔄 Reconnecting... (attempt ${attemptNumber})`);
      setConnectionStatus(`Reconnecting (${attemptNumber})`);
    });

    setSocket(socketInstance);

    return () => {
      socketInstance.disconnect();
    };
  }, []);

  const subscribeToSession = (sessionId: string) => {
    if (socket && isConnected) {
      console.log(`📡 Attempting to subscribe to session: ${sessionId}`);
      socket.emit("subscribe_session", { session_id: sessionId });
      
      // Listen for subscription confirmation
      socket.once("subscribed", (data) => {
        console.log(`✅ Successfully subscribed to session:`, data);
      });
    } else {
      console.warn(`⚠️ Cannot subscribe - Socket connected: ${!!socket}, Is connected: ${isConnected}`);
    }
  };

  return (
    <WebSocketContext.Provider
      value={{
        socket,
        isConnected,
        connectionStatus,
        subscribeToSession,
      }}
    >
      {children}
    </WebSocketContext.Provider>
  );
}

export function useWebSocketContext() {
  const context = useContext(WebSocketContext);
  if (context === undefined) {
    throw new Error("useWebSocketContext must be used within a WebSocketProvider");
  }
  return context;
}
