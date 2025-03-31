import { useEffect } from 'react';
import { useUserStore } from '../infra/cache/useUserStore';
import { UserModel } from '../domain/user/UserModel';
import { UserCard } from '../ui/components/UserCard';

import './App.css';


export const App = () => {
  const { updateUser, getUser } = useUserStore();

  // モックユーザを登録
  useEffect(() => {
    const user = new UserModel('1', 'raziii_03', 'princess.png');
    updateUser(user);

    setTimeout(() => {
      updateUser(user.dance());
    }, 1000);

    setTimeout(() => {
      updateUser(user.reset());
    }, 6000);
  }, []);

  const user = getUser('1');
  if (!user) return <p>Loading...</p>;

  return <UserCard user={user} />;
};
