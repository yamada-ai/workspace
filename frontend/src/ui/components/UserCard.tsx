import { useEffect } from 'react';

import { UserModel } from '../../domain/user/UserModel';
import { useUserViewStore } from '../../infra/cache/UserViewStore';
import { Sprite } from '../../viewmodel/Sprite';
import { CommentBubble } from './CommentBubble';
import { Direction } from '../../domain/user/Direction';
import { UserState } from '../../domain/user/UserState';
import { getRandomPositionInArea } from '../../domain/area/Area';

type Props = {
  user: UserModel;
};

export const UserCard = ({ user }: Props) => {
  const view = useUserViewStore((s) => s.getView(user.id));
  const clearExpired = useUserViewStore((s) => s.clearExpiredComments);

  useEffect(() => {
    const timer = setInterval(clearExpired, 1000);
    return () => clearInterval(timer);
  }, [clearExpired]);

  useEffect(() => {
    if (view && !view.position) {
      const pos = getRandomPositionInArea(user.area);
      useUserViewStore.getState().setPosition(user.id, pos.x, pos.y);
    }
  }, [view, user.area, user.id]);

  if (!view) return null;

  const { x, y } = view.position;

  console.log(user, x, y)

  return (
    <div className="relative w-full">
      {/* 💬 コメントは user-card の外で独立 */}
      {view.comment && (
        <div
          className="absolute"
          style={{
            left: `${x}px`,
            top: `${y - 24}px`, // スプライトの少し上
            width: '32px',       // スプライト幅と合わせる
            height: '20px',      // 高さは任意で調整
          }}
        >
          <CommentBubble comment={view.comment} />
        </div>
      )}

      {/* 🕺 スプライト */}
      <div
        className={`absolute w-8 h-8 ${user.state === 'Dancing' ? 'animate-wiggle' : ''}`}
        style={{ left: `${x}px`, top: `${y}px` }}
      >
        <Sprite direction={view.direction ?? Direction.Down} isWalking={user.state === UserState.Walking} />
      </div>

      {/* 👤 名前 + 状態 */}
      <div
        className="absolute w-16 text-center text-sm"
        style={{ left: `${x - 8}px`, top: `${y + 40}px` }}
      >
        <p>{user.name}</p>
        <p>Status: {user.state}</p>
      </div>
    </div>
  );
};

