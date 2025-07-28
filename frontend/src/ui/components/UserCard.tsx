import { useEffect } from 'react';
import { ellipsis } from '../../domain/utils/string'; 
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

  // コメントの期限クリア
  useEffect(() => {
    const timer = setInterval(clearExpired, 1000);
    return () => clearInterval(timer);
  }, [clearExpired]);

  // 初期位置がなければエリア内ランダム配置
  useEffect(() => {
    if (view && !view.position) {
      const pos = getRandomPositionInArea(user.area);
      useUserViewStore.getState().setPosition(user.id, pos.x, pos.y);
    }
  }, [view, user.area, user.id]);

  if (!view) return null;
  const { x, y } = view.position;

  return (
    <>
      {/* 💬 コメントバブル */}
      {view.comment && (
        <div
          className="absolute z-20 pointer-events-none"
          style={{
            left: x,
            top: y - 24,
            maxWidth: '120px',
          }}
        >
          <CommentBubble comment={view.comment} />
        </div>
      )}

      {/* 🃏 スプライト＋情報カード */}
      <div
        className="absolute flex items-center space-x-2 bg-white bg-opacity-90 p-1 rounded-lg shadow-md z-10 pointer-events-none max-w-max"
        style={{
          left: x + 12, // スプライト右横
          top: y,
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
        <div className="text-sm text-gray-800 whitespace-nowrap">
          <p className="font-medium">{ellipsis(user.name)}</p>
          <p className="text-xs">{ellipsis(user.work_name ?? '')}</p>
        </div>
      </div>
    </>
  );
};
