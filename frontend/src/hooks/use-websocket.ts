import { useWebSocketContext } from "@/contexts/websocket-context";
import { useEffect } from "react";

type EventCallback = (data: any) => void;

export function useWebSocket() {
  const { socket, isConnected, connectionStatus, subscribeToSession } = useWebSocketContext();

  const on = (event: string, callback: EventCallback) => {
    if (socket) {
      socket.on(event, callback);
    }
  };

  const off = (event: string, callback: EventCallback) => {
    if (socket) {
      socket.off(event, callback);
    }
  };

  const emit = (event: string, data: any) => {
    if (socket) {
      socket.emit(event, data);
    }
  };

  return {
    socket,
    isConnected,
    connectionStatus,
    subscribeToSession,
    on,
    off,
    emit,
  };
}

// Hook for subscribing to specific events
export function useWebSocketEvent(event: string, callback: EventCallback) {
  const { socket } = useWebSocketContext();

  useEffect(() => {
    if (socket) {
      socket.on(event, callback);
      return () => {
        socket.off(event, callback);
      };
    }
  }, [socket, event, callback]);
}
