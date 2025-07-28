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

  return (
    <div className="relative w-full h-full pointer-events-none">
      {/* 💬 コメント */}
      {view.comment && (
        <div
          className="absolute z-20"
          style={{
            left: `${x}px`,
            top: `${y - 24}px`,
            width: 'auto',
            maxWidth: '120px',
          }}
        >
          <CommentBubble comment={view.comment} />
        </div>
      )}

      {/* 🃏 カード（スプライト＋情報） */}
      <div
        className="absolute flex items-center space-x-2 bg-white bg-opacity-90 p-1 rounded-lg shadow-md z-10"
        style={{
          left: `${x + 12}px`,   // スプライト右横に少しオフセット
          top:  `${y}px`,
        }}
      >
        {/* スプライト */}
        <div className={`w-8 h-8 ${user.state === UserState.Dancing ? 'animate-wiggle' : ''}`}>
          <Sprite
            direction={view.direction ?? Direction.Down}
            isWalking={user.state === UserState.Walking}
          />
        </div>
        {/* ユーザー情報 */}
        <div className="text-sm text-gray-800">
          <p className="font-medium truncate" style={{ maxWidth: '80px' }}>
            {user.name}
          </p>
          <p className="text-xs">{user.work_name}</p>
        </div>
      </div>
    </div>
  );
};
