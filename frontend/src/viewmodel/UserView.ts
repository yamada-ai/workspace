export type UserView = {
    id: string;
    comment: string | null;
    commentUntil?: number; // UNIX msでの期限
  };
  