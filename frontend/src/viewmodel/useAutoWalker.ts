// src/viewmodel/useAutoWalker.ts
import { useEffect } from 'react';
import { useUserStore } from '../infra/cache/useUserStore';
import { useUserViewStore } from '../infra/cache/UserViewStore';
import { moveUser } from '../app/MoveUser';
import { Direction } from '../domain/user/Direction';
import { ID } from '../domain/ID';
import { UserModel } from '../domain/user/UserModel';

export const useAutoWalker = () => {
  const { getAllUsers, updateUser } = useUserStore();
  const { getView, setDirection } = useUserViewStore();

  useEffect(() => {
    const interval = setInterval(() => {
      const users = getAllUsers();

      users.forEach((user: UserModel) => {
        const view = getView(user.id as ID<UserModel>);

        // 歩ける状態で、かつ view 情報があるときだけ処理
        if (!view || !user.canWalk()) return;

        if (Math.random() < 0.4) {
          const dirs: Direction[] = [
            Direction.Up,
            Direction.Down,
            Direction.Left,
            Direction.Right,
          ];
          // 現在と違う方向をランダム選択
          const choices = dirs.filter((d) => d !== view.direction);
          const newDir = choices[Math.floor(Math.random() * choices.length)];

          // View側の向きを更新
          setDirection(user.id as ID<UserModel>, newDir);

          // Model側の状態を Walking に更新
          const walked = user.walk();
          updateUser(walked);
        }

        // 現在の向きのまま一歩進む
        moveUser(user.id as ID<UserModel>);
      });
    }, 1000); // 1秒ごと

    return () => clearInterval(interval);
  }, [getAllUsers, getView, setDirection, updateUser]);
};
