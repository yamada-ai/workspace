import { create } from 'zustand';
import { UserModel } from '../../domain/user/UserModel';

interface UserState {
  users: Record<string, UserModel>;
  updateUser: (user: UserModel) => void;
  getUser: (id: string) => UserModel | undefined;
}

export const useUserStore = create<UserState>((set, get) => ({
  users: {},
  updateUser: (user) =>
    set((state) => ({
      users: {
        ...state.users,
        [user.id]: user,
      },
    })),
  getUser: (id) => get().users[id],
}));
