import { UserView } from "./UserView";

export type UserViewState = {
    views: Record<string, UserView>;
    setComment: (userId: string, comment: string) => void;
    clearExpiredComments: () => void;
    getView: (userId: string) => UserView | undefined;
  };