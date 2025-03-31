import { useEffect } from 'react';
import { UserModel } from '../../domain/user/UserModel';
import { CommentBubble } from './CommentBubble';
import { useUserStore } from '../../infra/cache/useUserStore';

type Props = {
  user: UserModel;
};

export const UserCard = ({ user }: Props) => {

  useEffect(() => {
    const getUser = useUserStore((s) => s.getUser);
    const updateUser = useUserStore((s) => s.updateUser);

    useEffect(() => {
      const interval = setInterval(() => {
        const now = Date.now();
        const u = getUser(user.id);
        if (u?.commentUntil && u.commentUntil < now) {
          updateUser(u.withoutComment()); // イミュータブルに消す
        }
      }, 500);
  
      return () => clearInterval(interval);
    }, [getUser, updateUser, user.id]);
  

  return (
    <div className={`user-card ${user.state === 'Dancing' ? 'dancing' : ''}`}>
      {user.comment && <CommentBubble comment={user.comment} />}
      <img src={`/icons/${user.icon}`} alt="icon" width={64} height={64} />
      <p>{user.name}</p>
      <p>Status: {user.state}</p>
    </div>
  );
};
