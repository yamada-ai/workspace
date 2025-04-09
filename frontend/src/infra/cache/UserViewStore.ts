import { create } from 'zustand';
import { ID } from '../../domain/ID';
import { UserModel } from '../../domain/user/UserModel';
import { UserView } from '../../viewmodel/UserView';
import { Direction } from '../../domain/user/Direction';

type UserViewState = {
  views: Record<string, UserView>;
  setComment: (userId: ID<UserModel>, comment: string) => void;
  setDirection: (userId: ID<UserModel>, direction: Direction) => void;
  setPosition: (id: ID<UserModel>, x: number, y: number) => void
  clearExpiredComments: () => void;
  getView: (userId: ID<UserModel>) => UserView | undefined;
};

export const useUserViewStore = create<UserViewState>((set, get) => ({
  views: {},
  setComment: (id, comment) => {
    const now = Date.now();
    const until = now + 5000;
    set((state) => {
      const prev = state.views[id] ?? {
        id,
        direction: 'down',
        comment: null,
      };
      return {
        views: {
          ...state.views,
          [id]: {
            ...prev,
            comment,
            commentUntil: until,
          },
        },
      };
    });
  },

  setDirection: (id, direction) => {
    set((state) => {
      const prev = state.views[id] ?? { id, comment: null };
      return {
        views: {
          ...state.views,
          [id]: {
            ...prev,
            direction,
          },
        },
      };
    });
  },

  setPosition: (id: ID<UserModel>, x: number, y: number) => {
    set((state) => ({
      views: {
        ...state.views,
        [id]: {
          ...state.views[id],
          position: { x, y },
        },
      },
    }));
  },
  
  
  clearExpiredComments: () => {
    const now = Date.now();
    set((state) => {
      const newViews = { ...state.views };
      for (const id in newViews) {
        if (newViews[id].commentUntil && newViews[id].commentUntil! < now) {
          newViews[id] = { ...newViews[id], comment: null, commentUntil: undefined };
        }
      }
      return { views: newViews };
    });
  },
  getView: (id) => get().views[id],
}));
