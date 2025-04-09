import { useEffect } from 'react';
import { useUserStore } from '../infra/cache/useUserStore';
import { useUserViewStore } from '../infra/cache/UserViewStore';
import { UserModel } from '../domain/user/UserModel';
import { ID } from '../domain/ID';
import { Direction } from '../domain/user/Direction';
import { UserState } from '../domain/user/UserState';
import { registerUser } from '../app/registerUser';
import { moveUser } from './MoveUser';

import './App.css';
import { Area } from '../domain/area/Area';
import { AreaField } from '../ui/components/AreaField';


export const App = () => {
  const { updateUser, getUser } = useUserStore();

  useEffect(() => {
    const user = new UserModel(1 as ID<UserModel>, 'raziii_03', 'princess.png', UserState.Idle, Area.Tier1);
    registerUser(user);
  }, []);

  const user = getUser(1 as ID<UserModel>);
  if (!user) return <p>Loading...</p>;

  const walk = () => {
    updateUser(user.walk());

    let step = 0;
    const interval = setInterval(() => {
      
      if (step++ > 30) {
        clearInterval(interval);
        return;
      }
      moveUser(user.id);
    }, 100);
  };

  const idle = () => updateUser(user.reset());
  const dance = () => updateUser(user.dance());
  const comment = () => useUserViewStore.getState().setComment(user.id, '動いてます！');
  const changeDirection = (dir: Direction) =>
    useUserViewStore.getState().setDirection(user.id, dir);

  return (
    <div style={{ textAlign: 'center' }}>
      {/* <UserCard user={user} /> */}
      <AreaField />

      <div style={{ marginTop: '1rem' }}>
        <button onClick={walk}>🚶‍♂️ 歩く</button>
        <button onClick={dance}>💃 踊る</button>
        <button onClick={idle}>🛑 止まる</button>
        <button onClick={comment}>💬 コメント</button>
      </div>

      <div style={{ marginTop: '0.5rem' }}>
        <button onClick={() => changeDirection(Direction.Up)}>↑</button>
        <button onClick={() => changeDirection(Direction.Down)}>↓</button>
        <button onClick={() => changeDirection(Direction.Left)}>←</button>
        <button onClick={() => changeDirection(Direction.Right)}>→</button>
      </div>
    </div>
  );
};
