import { Direction } from "../domain/user/Direction";

export type UserView = {
    id: string;
    direction: Direction;
    position: { x: number; y: number }; // ←追加！
    comment: string | null;
    commentUntil?: number; // UNIX msでの期限
  };

