// src/infra/socket/useSocket.ts
import { useEffect } from "react";
import { useUserStore } from "../cache/useUserStore";
import { WsEvent, WsEventType } from "../../domain/ws/WsEvent";
import { registerUser } from "../../app/registerUser";
import { handleSessionStart, handleSessionEnd } from "./handlers";

export const useSocket = () => {
  const { updateUser } = useUserStore();

  useEffect(() => {
    const socket = new WebSocket("wss://localhost/ws");

    socket.onopen = () => {
      console.log("✅ WebSocket接続成功");
    };

    socket.onmessage = (e) => {
        const msg = JSON.parse(e.data) as WsEvent;
        console.log("📩 WebSocket受信:", msg);
  
        switch (msg.type) {
          case WsEventType.SessionStart:
            handleSessionStart(msg);
            break;
          case WsEventType.SessionEnd:
            handleSessionEnd(msg);
            break;
          default:
            // 型が足りているかコンパイル時にチェック
            const _exhaustive: never = msg;
            return _exhaustive;
        }
      };

    socket.onerror = (err) => {
      console.error("❌ WebSocketエラー:", err);
    };

    socket.onclose = () => {
      console.warn("⚠️ WebSocket切断");
    };

    return () => {
      socket.close();
    };
  }, [registerUser, updateUser]);
};
