// src/domain/ws/WsEventType.ts
export enum WsEventType {
  SessionStart = "session_start",
  SessionEnd = "session_end",
  SessionExtend = "session_extend",
  // …将来増えるイベントをここに追加
}

export interface BaseWsEvent {
  type: WsEventType;
}

export interface SessionStartEvent extends BaseWsEvent {
  type: WsEventType.SessionStart;
  id: number;
  user_name: string;
  work_name: string;
  start_time: string;
  planned_end: string;
}

export interface SessionEndEvent extends BaseWsEvent {
  type: WsEventType.SessionEnd;
  id: number;
}

// 全体のユニオン
export type WsEvent = SessionStartEvent | SessionEndEvent /* | … */;
