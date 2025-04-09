// src/app/registerUser.ts
import { UserModel } from '../domain/user/UserModel';
import { useUserStore } from '../infra/cache/useUserStore';
import { useUserViewStore } from '../infra/cache/UserViewStore';
import { Direction } from '../domain/user/Direction';
import { getRandomPositionInArea } from '../domain/area/Area';

export const registerUser = (user: UserModel) => {
  useUserStore.getState().updateUser(user);
  useUserViewStore.getState().setDirection(
    user.id, Direction.Down
  );
  const { x, y } = getRandomPositionInArea(user.area);
  useUserViewStore.getState().setPosition(user.id, x, y);
};
